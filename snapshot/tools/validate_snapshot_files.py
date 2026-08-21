#!/usr/bin/env python3
"""
Validate Snapshot Flat File CSV exports against the field-level specs in snapshot/specs/.

Usage:
    python validate_snapshot_files.py <folder> [--output report.txt]

Scans <folder> for *.csv files, matches each one to a known Snapshot object
type by its header row, and checks it against that object's spec: required
headers, field formats/max-lengths, allowed enum values, and uniqueness of
key fields. When a recognized pair of related files is present together
(e.g. Subject + Subject to Course Association, or Hierarchy Node + Hierarchy
Course Association), it also checks that foreign-key references resolve.

Cross-file reference checks assume the folder holds the FULL export for each
object type. If a folder holds a partial snippet, missing references are
expected and are not necessarily a data problem -- read the finding in that
light rather than treating it as a confirmed defect.

To support another Snapshot object type, add a new entry to VALIDATORS with
its required header set and a validate_* function following the existing
pattern.
"""

import argparse
import csv
import re
from collections import Counter, defaultdict


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames or [], list(reader)


# ---------------------------------------------------------------------------
# Per-object-type validators. Each returns a list of finding strings.
# ---------------------------------------------------------------------------

SUBJECT_ID_RE = re.compile(r"^[A-Za-z0-9\-._]+__[A-Za-z0-9]+$")
NODE_KEY_RE = re.compile(r"^[A-Za-z0-9\-.]+$")


def validate_subject(rows):
    findings = []
    allowed_types = {"U", "G", "D", "N", "T", "P"}
    key_counter = Counter(r.get("external_subject_key", "") for r in rows)
    id_counter = Counter(r.get("subject_id", "") for r in rows)
    for k, c in key_counter.items():
        if c > 1:
            findings.append(f"Duplicate external_subject_key '{k}' ({c} rows)")
    for k, c in id_counter.items():
        if c > 1:
            findings.append(f"Duplicate subject_id '{k}' ({c} rows)")
    for i, row in enumerate(rows, start=2):
        key = row.get("external_subject_key", "")
        sid = row.get("subject_id", "")
        if row.get("subject_type") not in allowed_types:
            findings.append(f"Row {i}: invalid subject_type '{row.get('subject_type')}' for {key}")
        if row.get("available_ind", "") not in ("Y", "N", ""):
            findings.append(f"Row {i}: invalid available_ind '{row.get('available_ind')}' for {key}")
        if row.get("row_status", "") not in ("enabled", "disabled", "deleted", ""):
            findings.append(f"Row {i}: invalid row_status '{row.get('row_status')}' for {key}")
        if sid and not SUBJECT_ID_RE.match(sid):
            findings.append(f"Row {i}: subject_id '{sid}' does not match Title__Identifier format")
        if len(key) > 64:
            findings.append(f"Row {i}: external_subject_key exceeds 64 chars: '{key}'")
        if len(sid) > 100:
            findings.append(f"Row {i}: subject_id exceeds 100 chars: '{sid}'")
        if len(row.get("subject_name", "")) > 255:
            findings.append(f"Row {i}: subject_name exceeds 255 chars")
        if " " in key:
            findings.append(f"Row {i}: external_subject_key contains a space: '{key}'")
    return findings


def validate_subject_to_course_association(rows):
    findings = []
    assoc_counter = Counter(r.get("external_association_key", "") for r in rows)
    for k, c in assoc_counter.items():
        if c > 1:
            findings.append(f"Duplicate external_association_key '{k}' ({c} rows)")
    for i, row in enumerate(rows, start=2):
        ak = row.get("external_association_key", "")
        if len(ak) > 64:
            findings.append(f"Row {i}: external_association_key exceeds 64 chars: '{ak}'")
    return findings


def validate_hierarchy_node(rows):
    findings = []
    key_counter = Counter(r.get("external_node_key", "") for r in rows)
    for k, c in key_counter.items():
        if c > 1:
            findings.append(f"Duplicate external_node_key '{k}' ({c} rows)")

    node_keys = set(key_counter)
    seen_so_far = set()
    for i, row in enumerate(rows, start=2):
        k = row.get("external_node_key", "")
        p = row.get("parent_node_key", "")
        if not NODE_KEY_RE.match(k):
            findings.append(f"Row {i}: external_node_key '{k}' contains characters other than letters/digits/dashes/periods")
        if len(k) > 255:
            findings.append(f"Row {i}: external_node_key exceeds 255 chars: '{k}'")
        if len(row.get("name", "")) > 255:
            findings.append(f"Row {i}: name exceeds 255 chars for node '{k}'")
        if p != "0" and p not in node_keys:
            findings.append(f"Row {i}: parent_node_key '{p}' for node '{k}' does not exist in this file")
        elif p != "0" and p not in seen_so_far:
            findings.append(f"Row {i}: parent node '{p}' for node '{k}' appears LATER in the file (parents must be submitted before children)")
        seen_so_far.add(k)
    return findings


def validate_hierarchy_course_association(rows):
    findings = []
    assoc_counter = Counter(r.get("external_association_key", "") for r in rows)
    for k, c in assoc_counter.items():
        if c > 1:
            findings.append(f"Duplicate external_association_key '{k}' ({c} rows)")

    primary_counter = defaultdict(int)
    for i, row in enumerate(rows, start=2):
        ak = row.get("external_association_key", "")
        if len(ak) > 64:
            findings.append(f"Row {i}: external_association_key exceeds 64 chars: '{ak}'")
        pind = row.get("is_primary_association", "")
        if pind not in ("Y", "N", ""):
            findings.append(f"Row {i}: invalid is_primary_association '{pind}' for {ak}")
        if pind == "Y":
            primary_counter[row.get("external_course_key", "")] += 1
    for course, count in primary_counter.items():
        if count > 1:
            findings.append(f"Course '{course}' has {count} rows marked is_primary_association=Y (should be at most 1)")
    return findings


# ---------------------------------------------------------------------------
# Registry: object name -> (spec file, required headers, validator)
# ---------------------------------------------------------------------------

VALIDATORS = [
    (
        "Subject",
        "snapshot/specs/snapshot-subject.md",
        {"external_subject_key", "data_source_key", "subject_id", "subject_name", "subject_type"},
        validate_subject,
    ),
    (
        "Subject to Course Association",
        "snapshot/specs/snapshot-subject-to-course-association.md",
        {"external_association_key", "data_source_key", "external_course_key", "external_subject_key"},
        validate_subject_to_course_association,
    ),
    (
        "Hierarchy Node",
        "snapshot/specs/snapshot-hierarchy-node.md",
        {"external_node_key", "data_source_key", "parent_node_key", "name"},
        validate_hierarchy_node,
    ),
    (
        "Hierarchy Course Association",
        "snapshot/specs/snapshot-hierarchy-course-association.md",
        {"external_association_key", "data_source_key", "external_node_key", "external_course_key"},
        validate_hierarchy_course_association,
    ),
]


def match_object_type(fieldnames):
    header_set = set(fieldnames)
    for name, spec, required, validator in VALIDATORS:
        if required.issubset(header_set):
            return name, spec, validator
    return None, None, None


def cross_file_checks(loaded):
    """loaded: dict of object name -> (fieldnames, rows). Returns list of finding strings."""
    findings = []

    if "Subject" in loaded and "Subject to Course Association" in loaded:
        subject_keys = {r.get("external_subject_key", "") for r in loaded["Subject"][1]}
        for i, row in enumerate(loaded["Subject to Course Association"][1], start=2):
            sk = row.get("external_subject_key", "")
            if sk not in subject_keys:
                findings.append(
                    f"Subject to Course Association row {i} (assoc '{row.get('external_association_key')}'): "
                    f"external_subject_key '{sk}' not found in the Subject file"
                )

    if "Hierarchy Node" in loaded and "Hierarchy Course Association" in loaded:
        node_keys = {r.get("external_node_key", "") for r in loaded["Hierarchy Node"][1]}
        for i, row in enumerate(loaded["Hierarchy Course Association"][1], start=2):
            nk = row.get("external_node_key", "")
            if nk not in node_keys:
                findings.append(
                    f"Hierarchy Course Association row {i} (assoc '{row.get('external_association_key')}'): "
                    f"external_node_key '{nk}' not found in the Hierarchy Node file"
                )

    return findings


def main():
    parser = argparse.ArgumentParser(description="Validate Snapshot Flat File CSVs against the specs in snapshot/specs/.")
    parser.add_argument("folder", help="Folder containing the Snapshot flat-file CSV exports to validate")
    parser.add_argument("--output", help="Also write the report to this text file")
    args = parser.parse_args()

    import os

    csv_paths = sorted(p for p in os.listdir(args.folder) if p.lower().endswith(".csv"))

    lines = []
    loaded = {}

    for csv_name in csv_paths:
        path = os.path.join(args.folder, csv_name)
        fieldnames, rows = read_csv(path)
        obj_name, spec, validator = match_object_type(fieldnames)

        lines.append(f"{'=' * 10} {csv_name} {'=' * 10}")
        if obj_name is None:
            lines.append("Could not match this file to a known Snapshot object type by its headers.")
            lines.append(f"Headers found: {fieldnames}")
            lines.append("")
            continue

        loaded[obj_name] = (fieldnames, rows)
        lines.append(f"Matched object type: {obj_name}  (spec: {spec})")
        lines.append(f"Row count: {len(rows)}")

        findings = validator(rows)
        if findings:
            lines.append(f"Findings ({len(findings)}):")
            for f in findings:
                lines.append(f"  - {f}")
        else:
            lines.append("No issues found.")
        lines.append("")

    cross = cross_file_checks(loaded)
    lines.append(f"{'=' * 10} Cross-file reference checks {'=' * 10}")
    lines.append("(Assumes each file is a complete export. If this folder is a partial")
    lines.append(" snippet, a missing reference here may just mean the referenced row")
    lines.append(" lives outside the snippet -- verify against the full export before")
    lines.append(" treating it as a confirmed data problem.)")
    if cross:
        for f in cross:
            lines.append(f"  - {f}")
    else:
        lines.append("No issues found." if loaded else "No related file pairs present to cross-check.")
    lines.append("")

    report = "\n".join(lines)
    print(report)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)


if __name__ == "__main__":
    main()
