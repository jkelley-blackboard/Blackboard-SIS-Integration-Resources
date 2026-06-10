# Snapshot Flat File YAML Schema

This document defines the YAML schema used for all Snapshot Flat File object spec files.
Each `.yaml` file in this directory represents one LEARN object.

---

## Top-Level Keys

```yaml
id:             string   # Unique doc identifier, e.g. snapshot-flatfile-course
title:          string   # Human-readable title
published:      string   # ISO date of first publication
edited:         string   # ISO date of last edit
author:         string   # Author attribution

sis_object:     string   # SIS layer name (e.g. "Course or Organization")
endpoint_slug:  string   # Base endpoint path (e.g. "course")
insert_update:  string   # Default insert/update behavior
delete_behavior: string  # "Disable" or "Purge"
description:    string   # One-paragraph object description

endpoints:      list     # See Endpoints schema
fields:         list     # See Fields schema
value_tables:   list     # Optional — see Value Tables schema
sample:         object   # See Sample schema
notes:          list     # Bullet-point notes (plain strings)
```

---

## Endpoints Schema

```yaml
endpoints:
  - operation: string    # e.g. "Store", "Complete Refresh", "Delete"
    path: string         # e.g. "person/store"
    variant: string      # Optional — e.g. "Course", "Organization"
```

---

## Fields Schema

```yaml
fields:
  - name: string         # UI/display name, e.g. "Batch Uid"
    header: string       # Feed column header, e.g. "external_course_key"
                         # Use "(auto-populated)" for system-generated keys
                         # Use "TBC" for headers pending confirmation
    required: bool       # true | false
    unique: bool         # true | false
    format: string       # Optional — e.g. "yyyymmdd", "Max 64", "Numeric"
    multibyte: bool      # Optional — true if multi-byte characters accepted
    values: string       # Optional — inline value list or reference to value_tables entry
                         # e.g. "'Y' | 'N'" or "See duration_values"
    deprecated: bool     # Optional — true if field is deprecated/unsupported
    comment: string      # Optional — implementation notes
    org_variant: string  # Optional — alternate header name for Organization feeds
                         # e.g. "external_organization_key"
```

---

## Value Tables Schema

Used for fields with named enumerated values (Duration, System Role, etc.).

```yaml
value_tables:
  - id: string           # Referenced from fields[].values, e.g. "duration_values"
    caption: string      # Section heading, e.g. "Duration Values"
    columns:             # List of column names
      - string
    rows:                # List of rows, each a list of cell values
      - - string
```

---

## Sample Schema

```yaml
sample:
  headers:               # Ordered list of header names for the sample feed
    - string
  rows:                  # One or more sample data rows
    - - string
  note: string           # Optional — annotation about the sample
```

---

## Conventions

- Boolean fields (`required`, `unique`, `deprecated`, `multibyte`) use `true` / `false`.
- `format` captures the primary constraint. When both a max length and multi-byte apply,
  put max length in `format` and set `multibyte: true`.
- `values` is a short inline string for simple enumerations (`"'Y' | 'N'"`).
  For longer enumerations, use `"See <value_table_id>"` and define the table in `value_tables`.
- `org_variant` is used only on fields where the Course and Organization header names differ.
  All other dual-object fields share the same header.
- `endpoint_slug` is the base slug. Dual-endpoint objects (Course/Org) list both variants
  in `endpoints` using the `variant` key.
