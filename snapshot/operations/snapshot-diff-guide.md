---
title: "Converting Full-Load Snapshot Exports to Diffs"
id: snapshot-flatfile-diff-guide
categories: SIS, Snapshot Flat File
published: "2026-08-28"
edited: "2026-08-28"
author: "Jeff Kelley, Principal Solutions Engineer, Blackboard Inc."
---

# Converting Full-Load Snapshot Exports to Diffs

This is for institutions whose SIS (or export layer — the [generator](snapshot-automation-guide.md#in-plain-terms)) only knows how to produce a full-load export: every user, every course, every enrollment, every single run. It covers a way to stop sending that whole file to Learn every time. Instead, compare the latest export to the previous one, build a much smaller file containing only what actually changed, and post that instead.

In practice, `refresh` is most commonly used for **User**, **Course/Organization**, and **Membership** — so those three are the objects this guide is most useful for. All three also happen to use `disable` as their [delete behavior](../snapshot-flat-file-overview.md#delete-behaviors), which is why `disable` is the default removal policy recommended below.

---

## In Plain Terms

If nothing about a student changed since the last run, there's no real reason to re-send their full record this run — whether "last run" was yesterday, four hours ago, or last week. But a full-load export does that anyway. It's just a snapshot of "everything, right now" — it has no memory of what was sent before, so it can't tell what's actually different.

A **diff** step fixes that. It sits between the generator and the controller, takes the latest export and the previous one, and lines them up row by row using each record's identity (e.g. `external_person_key`). Out of that comparison, it produces three things:

1. A file of the rows that are new or changed — for `store`.
2. A file of the rows that disappeared — for `delete`, or a `row_status=disabled` update, depending on what "disappeared" should mean for that object.
3. A log of what it found — counts, and ideally which keys and which fields changed — so someone can see what actually got sent without having to read the raw files.

In short: instead of "post everything, every time," you get "post only what changed." That's a smaller file, faster for Learn to process, and much easier to reason about when something looks wrong.

---

## Why Bother

- **Processing time and size.** Learn has to process whatever file it's given. Post the whole population every time and Learn does insert-or-update work on every record, every time — even the 99% that didn't change.
- **Signal in the logs.** A delta file's row count *is* the change count for that run. A full file's row count tells you nothing — you'd have to diff it yourself just to know what happened.
- **Blast radius.** A malformed delta file can only be as wrong as the change set itself. A malformed full file can touch every record the integration manages.
- **REFRESH risk, specifically.** Many clients post full-load exports with `refresh` rather than `store`, just to get its automatic disable-what's-missing behavior. But `refresh` runs against the entire data set, and per [REFRESH Risk](snapshot-posting-guide.md#refresh-risk) in the posting guide, an interrupted or truncated file doesn't just fail — it can silently disable real, still-active records. Blackboard's own recommendation is to limit `refresh` usage and favor `store`-based, changes-only feeds wherever possible. Diffing is one way to get there: it produces a `store` file, which is safe to under-apply if something goes wrong, plus an explicit removal step you control (see [Removed Rows Need a Decision, Not Just a Mechanism](#removed-rows-need-a-decision-not-just-a-mechanism)) — instead of leaning on `refresh`'s all-or-nothing comparison.

This is a tradeoff, not a strict upgrade — see [When Not To Do This](#when-not-to-do-this).

---

## Core Approach

1. **Keep the previous export.** The diff step needs two files: the latest full export and the one before it, for the same object. It doesn't matter how often runs happen — daily, several times a day, or less often — just keep the last one (ideally a short rolling history) somewhere. This is in addition to, not instead of, whatever archiving the [controller](snapshot-automation-guide.md) already does with files it has posted.
2. **Pick the natural key for each object.** This is the column (or columns) that say "these two rows are the same record" across the two files. It's specific to the object type — `external_person_key` for [User](../specs/snapshot-user.md), `external_course_key` for [Course/Organization](../specs/snapshot-course.md). [Membership](../specs/snapshot-membership.md) doesn't have a single Batch Uid field — a membership row is identified by the *pair* of `external_course_key` and `external_person_key` together, so treat that pair as one composite key when matching rows. Without a stable key to match on, there's nothing to diff.
3. **Normalize before comparing.** Snapshot files allow columns in any order (see the [format spec](../snapshot-flat-file-overview.md#general-file-format)), and two export runs aren't guaranteed to use the same order. So compare by column name, not position. Also trim whitespace, and lowercase fields that aren't meant to be case-sensitive — otherwise formatting noise gets counted as a real change.
4. **Classify every row**, comparing the previous file to the latest:
   - **Added** — the key is in the latest file but not the previous one.
   - **Changed** — the key is in both, but at least one field is different.
   - **Removed** — the key is in the previous file but not the latest one.
   - **Unchanged** — the key is in both and every field matches. Drop these — they're exactly what diffing exists to filter out.
5. **Write the output files:**
   - Added and Changed rows go in one file, posted with `store`. Since `store` is insert-or-update, one file correctly covers both cases.
   - Removed rows need a deliberate decision, not an automatic one. `store` never removes or disables anything it isn't told about, so you have to explicitly choose what to do with a removed row:
     - Post a `delete` file for just those keys, if the object's [delete behavior](../snapshot-flat-file-overview.md#delete-behaviors) — purge or disable — is what you want, or
     - Post those keys with `row_status=disabled` (or `deleted`, per the object's Row Status values) through `store`, if you want a softer removal than the object's native delete.
   - Either way, treat this as a real decision per object — not something to translate mechanically. See the next section.
6. **Log the run**, not just the files it produced. At minimum: run timestamp, object type, source file names (ideally with a checksum of each), and the added/changed/removed/unchanged counts. Where practical, also log which keys changed and which fields changed for them — that's what lets someone answer "why did this record change in Learn?" later, without re-diffing the raw files by hand.

---

## Removed Rows Need a Decision, Not Just a Mechanism

This is the part that's easy to get wrong. A full-load `refresh` handles disappearance *for you*: Learn does the same insert/update as `store` for every record in the file, then disables or purges — per the object's [delete behavior](../snapshot-flat-file-overview.md#delete-behaviors) — any record it holds that isn't in the file. That's exactly the same compare-and-remove work a diff step has to do itself. The only difference is where it happens: native `refresh` does it server-side, against a file that has everything; a diff step does it client-side, ahead of time, against a file that has only the delta.

For that comparison to be correct, "everything Learn holds" and "everything the file should contain" need to mean the same population. So it matters what Learn considers **the data set** for a given refresh. Snapshot actually has two different scopes for this, per the [Overview](../snapshot-flat-file-overview.md#operation-types):

- **Complete Refresh** (`.../refresh`) — scoped to *this integration instance* — the specific deployed integration/building block that created the records. Records created by a different integration instance, even under the same Data Source Key, aren't touched.
- **Complete Refresh by Data Source** (`.../refreshlegacy`) — scoped to a specific **Data Source Key**, no matter which integration instance created the records. This is the broader scope, and often the more intuitive one when an institution organizes its data by Data Source Key.

These two are not interchangeable. Picking the wrong one against a partial file is exactly the mistake the [Pre-Flight Checklist](snapshot-posting-guide.md#pre-flight-checklist) warns about: submit a Complete Refresh by Data Source with a file that only covers part of that key's population, and everything else under that key gets disabled — including records another integration instance is still actively managing.

Once you're diffing and posting with `store` instead of using native `refresh`, neither of those scopes applies automatically anymore. The diff step has to decide, and act on, removals itself — using whatever scope actually matches how `previousFile` and `latestFile` were generated (by Data Source Key, by integration instance, or something else). If that scope isn't clearly defined, a diff's removal set can be just as wrong as a mis-scoped native refresh — for the same reason.

Before building this, get an explicit answer for each object — from whoever actually owns the SIS-side data, not just your own best guess:

- Does "missing from the latest export" really mean the record should be disabled or deleted in Learn? Or could the generator have simply left it out this run for some unrelated reason — a filtered extract, a partial run, a bug?
- If the generator sometimes produces a partial or filtered export, diffing against it will misread every one of those still-active records as "removed." A bad run on the generator's side becomes a bad run in Learn. Add a sanity check before trusting a diff's removals — e.g. refuse to act on a removal set that's implausibly large compared to past runs.

---

## Reference Algorithm

The steps below are written as language-agnostic pseudocode — deliberately not tied to any particular language, library, or file-size strategy (see [Comparing Large Files](#comparing-large-files) for the streaming-vs-in-memory decision; this pseudocode describes the *logic*, independent of that choice). A coder should be able to implement this directly in whatever language/stack they're already using.

### Inputs

- `previousFile` — the prior run's full-load export for one object (may not exist, on the very first run).
- `latestFile` — the current run's full-load export for the same object.
- `keyColumn` — the object's natural key, per its [spec](../specs/README.md). Specific to the object type: `external_person_key` for User, `external_course_key` for Course/Organization. For Membership, there's no single key field — use the pair `(external_course_key, external_person_key)` as one composite key (e.g. join them with a delimiter that can't appear in either value, like `external_course_key + " " + external_person_key`).
- `compareColumns` — every column in the file except `keyColumn`. This isn't something to hand-pick per object; the default is simply "everything else." The only reason to remove a column from this set is a specific, known exception — e.g. a value the generator regenerates on every run regardless of real change (see [Normalization Rules](#normalization-rules)).
- `removalPolicy` — one of `delete` | `disable` | `ignore`, decided per object per [Removed Rows Need a Decision, Not Just a Mechanism](#removed-rows-need-a-decision-not-just-a-mechanism). When diffing is standing in for `refresh` — which is the main case this guide targets — `disable` is the default: User, Course/Organization, and Membership all use `disable` as their native [delete behavior](../snapshot-flat-file-overview.md#delete-behaviors), so a diff-based replacement should match that rather than switching to a harder `delete`.

### Data Structures

- `Row` — an ordered map of `columnName -> stringValue`, one per data row. All Snapshot fields are strings (per the [format spec](../snapshot-flat-file-overview.md#general-file-format)), so no type coercion is needed for comparison.
- `RowIndex` — a map of `keyValue -> Row`, built from a file's rows, keyed by `keyColumn`.

### Step 1 — Parse a file into a RowIndex

```
function loadRowIndex(filePath, keyColumn):
    if filePath does not exist:
        return empty RowIndex          # valid on first run — see Step 5, Added-only case

    header = read first line, split on "|"
    index = new empty RowIndex

    for each subsequent line in filePath:
        fields = split line on "|"
        row = new Row, mapping header[i] -> fields[i] for each i
        key = row[keyColumn]     # for a composite key (e.g. Membership), build key from all key columns, e.g. row[external_course_key] + "::" + row[external_person_key]

        if key already in index:
            flag/log a duplicate-key warning     # malformed export — do not silently overwrite
        index[key] = row

    return index
```

### Step 2 — Normalize a value before comparing

```
function normalize(columnName, value):
    value = trim(value)
    if columnName is defined case-insensitive for this object:
        value = lowercase(value)
    return value
```

Which columns are case-insensitive is object- and field-specific — decide this per column from the object's spec, don't assume globally. See [Normalization Rules](#normalization-rules).

### Step 3 — Compare two rows

```
function rowsDiffer(previousRow, latestRow, compareColumns):
    for each column in compareColumns:
        if normalize(column, previousRow[column]) != normalize(column, latestRow[column]):
            return true
    return false
```

A variant that also returns *which* columns differed (for the [log](#step-6--log-the-run)) is worth the small extra bookkeeping:

```
function diffFields(previousRow, latestRow, compareColumns):
    changed = empty list
    for each column in compareColumns:
        if normalize(column, previousRow[column]) != normalize(column, latestRow[column]):
            append column to changed
    return changed
```

### Step 4 — Classify every row

```
function classify(previousIndex, latestIndex, compareColumns):
    added = empty list of Row
    changed = empty list of (Row, changedColumns)
    removed = empty list of Row
    unchangedCount = 0

    for each (key, latestRow) in latestIndex:
        if key not in previousIndex:
            append latestRow to added
        else:
            previousRow = previousIndex[key]
            changedColumns = diffFields(previousRow, latestRow, compareColumns)
            if changedColumns is not empty:
                append (latestRow, changedColumns) to changed
            else:
                unchangedCount += 1

    for each (key, previousRow) in previousIndex:
        if key not in latestIndex:
            append previousRow to removed

    return (added, changed, removed, unchangedCount)
```

### Step 5 — Generate the store file

```
function writeStoreFile(added, changed, header, outputPath):
    rows = added + [latestRow for (latestRow, _) in changed]
    write header line to outputPath
    for each row in rows:
        write row's fields, in header order, joined by "|"
```

On the very first run (no `previousFile`), `previousIndex` is empty, so every row in `latestIndex` classifies as Added — the store file is just the full latest export, which is the correct behavior for a first load.

### Step 6 — Generate the removal file, per `removalPolicy`

```
function writeRemovalFile(removed, removalPolicy, header, outputPath):
    if removalPolicy == "ignore":
        return   # object's data intentionally never removed via this path

    if removalPolicy == "delete":
        write that object's delete-file layout (per its spec) for each row in removed,
        containing at minimum keyColumn

    if removalPolicy == "disable":
        write header line to outputPath
        for each row in removed:
            row[row_status_column] = "disabled"   # (or "deleted", per the object's Row Status values)
            write row's fields, in header order, joined by "|"
```

Before acting on `removed` at all, apply the sanity check from [Removed Rows Need a Decision, Not Just a Mechanism](#removed-rows-need-a-decision-not-just-a-mechanism) — e.g. abort and alert instead of writing the removal file if `size(removed)` exceeds some implausible threshold relative to `size(previousIndex)`.

### Step 7 — Log the run

```
function logRun(objectType, previousFile, latestFile, added, changed, removed, unchangedCount):
    record:
        timestamp
        objectType
        previousFile name (+ checksum, if available)
        latestFile name (+ checksum, if available)
        counts: len(added), len(changed), len(removed), unchangedCount
        for each (row, changedColumns) in changed:
            record row[keyColumn] -> changedColumns
        for each row in removed:
            record row[keyColumn]
```

### Putting it together

```
function diffRun(objectType, previousFile, latestFile, keyColumn, compareColumns, removalPolicy):
    previousIndex = loadRowIndex(previousFile, keyColumn)
    latestIndex = loadRowIndex(latestFile, keyColumn)

    (added, changed, removed, unchangedCount) = classify(previousIndex, latestIndex, compareColumns)

    header = latestIndex's header (captured during Step 1)
    writeStoreFile(added, changed, header, storeOutputPath)
    writeRemovalFile(removed, removalPolicy, header, removalOutputPath)
    logRun(objectType, previousFile, latestFile, added, changed, removed, unchangedCount)
```

`storeOutputPath` is then what the [controller](snapshot-automation-guide.md) posts with `store`; `removalOutputPath` (when non-empty) is posted with `delete`, or folded into the same `store` post if `removalPolicy` is `disable`.

### Normalization Rules

Keep the per-column normalization rules (Step 2) in a config/table alongside `keyColumn` and `compareColumns` — not hardcoded in the diff logic — so tuning them for a given object doesn't require touching the algorithm itself. At minimum, decide and record, per object, per column:

- Trim whitespace? (generally yes, always)
- Case-insensitive comparison? (depends on the field — e.g. an email or username might be, a free-text name field probably shouldn't be silently normalized this way)
- Any columns to exclude from `compareColumns` entirely — e.g. a field the generator regenerates every run regardless of real change (a last-modified timestamp, a row-level checksum) would otherwise make every row look Changed.

---

## Comparing Large Files

A full export for a large institution can be a lot of rows. Here are three practical ways to compare two large files, roughly in order of how much extra infrastructure each one needs:

- **Sort-merge.** Sort both files by the key column, then walk through them side by side — like the merge step in mergesort. This streams through both files without ever loading either one fully into memory. Works well as long as your tooling can sort large text files efficiently, which most OS-level sort utilities can.
- **Hash map / keyed lookup.** Load the previous (usually smaller) file into an in-memory map, keyed on the natural key, then stream the latest file against it. Simple to build; the only limit is how much memory the previous file's data takes up.
- **Staging table.** Load both files into a scratch database table — even a local SQLite file works — and let a couple of `JOIN`/`WHERE NOT EXISTS` queries do the classifying. The most flexible option for digging into a specific run's changes later, at the cost of adding a database to the pipeline.

Pick whichever fits what the rest of the controller/generator tooling already uses. Adding a new dependency (like a database) just for diffing is a real cost, and for a smaller institution it may not be worth it.

### Real-World Example: Shell One-Liners

Chris Bray at the University of Arkansas (UARK) shared a set of shell one-liners used for a quick line-level diff between two full-load exports, ahead of building anything more structured. Working example:

```bash
# diff, formatted to show only lines added in the newer file
diff --changed-group-format='%<' --unchanged-group-format='' \
  _processed/members_student_20250817_205840.txt \
  members_student_20250818_071151.txt

# comm, sorted files only — lines unique to the second file
comm -13 _processed/members_student_20250817_205840.txt members_student_20250818_071151.txt

# awk, using the older file as a lookup set
awk 'NR==FNR{a[$0];next} ($0 in a==0)' \
  _processed/members_student_20250817_205840.txt \
  members_student_20250818_071151.txt
```

A `grep` variant was tried too (`grep -v oldfile newfile`), but as written that treats the old filename as a literal search pattern, not a file to diff against — it needs `-F` (fixed string), `-x` (whole line), and `-f` (read patterns from a file) to actually compare two files: `grep -vFxf oldfile newfile`.

**Caveats before adopting one of these directly:**

- All four only surface lines that are in the newer file but not the older one. That's Added *and* Changed rows lumped together — a changed row is, byte-for-byte, just a "new" line — with no way to tell which from the output, and no Removed output at all. Getting Removed means running the same comparison in reverse (older file against newer) and reconciling by key, which starts to reproduce the [Classify every row](#core-approach) step above rather than replace it.
- These compare whole lines, not individual fields. Any byte difference — column order, trailing whitespace, a regenerated timestamp column — counts as a change. That's the exact false-positive risk covered in [Normalize before comparing](#core-approach) and [Normalization Rules](#normalization-rules).
- `comm` needs both files sorted identically first; `diff` and `awk` don't require it, but sorting first still helps performance on very large files (see [Sort-merge](#comparing-large-files) above).

This covers a quick manual comparison between two runs. It does not implement the classify/key/removal-policy logic described in the [Reference Algorithm](#reference-algorithm) above, which is what an unattended, scheduled process needs.

---

## When Not To Do This

- **Small populations.** If a full export is already small and fast to process, diffing just adds a new moving part — and a new way for things to break — for very little benefit.
- **Generator reliability is uncertain.** Diffing trusts that the "previous" export was itself complete and correct. If the generator has a history of partial or bad runs, diffing against a bad baseline just carries that error forward — see [Removed Rows Need a Decision, Not Just a Mechanism](#removed-rows-need-a-decision-not-just-a-mechanism) above. This isn't necessarily a hard blocker, though — it can be managed with safety checks built on what a normal run looks like: an expected row-count range, an expected file-size range, a cap on what percentage of the population can plausibly change or disappear in one run. If a run falls outside those expectations, abort and alert instead of posting, rather than trusting the diff blindly. If the generator's reliability can't support even that level of expectation, that's when diffing genuinely isn't worth it yet.
- **You still need a periodic full reconciliation.** Diffing lets small drift build up over time — a missed run, a bug in the diff logic — because Learn is no longer being told "here is the full truth" on every cycle. Keep a scheduled full `refresh` as a periodic safety net even after moving routine posts to diffs (weekly is a reasonable starting point, or whatever interval makes sense relative to the regular diff cadence). This is the same store/refresh scheduling separation already covered in the [automation guide](snapshot-automation-guide.md#scheduling) — just applied at a longer interval.

---

## Notes

- The [Reference Algorithm](#reference-algorithm) section is pseudocode on purpose, not a script — a coder should be able to translate it directly into whatever language and stack they're already using.
- This sits upstream of, and feeds into, the [controller](snapshot-automation-guide.md): the diff step's output (a delta file) is just what the controller posts next, the same as any other Snapshot file.
- Not yet addressed: whether diffing `refresh` files is useful, or whether diffing only applies to `store`-oriented feeds.
