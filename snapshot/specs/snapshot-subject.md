---
title: "Snapshot Flat File — Subject"
id: snapshot-flatfile-subject
categories: SIS, Snapshot Flat File
published: "2026-04-22"
edited: "2026-04-22"
author: "Jeff Kelley, Principal Solutions Engineer, Blackboard Inc."
---

# Subject

**SIS Object:** Subject  
**Endpoint:** `/endpoint/subject/`  
**Insert/Update behavior:** Smart Insert or Update  
**Delete behavior:** Disable

The Subject object creates and manages curricular subjects in Blackboard Learn. Subjects represent discipline-level curriculum classifications and can be associated with Courses, Organizations, and Programs.

---

## Endpoints

| Operation | URL |
| :--- | :--- |
| Store | `.../endpoint/subject/store` |
| Complete Refresh | `.../endpoint/subject/refresh` |
| Complete Refresh by Data Source | `.../endpoint/subject/refreshlegacy` |
| Delete | `.../endpoint/subject/delete` |

---

## Fields

| Field | Header | Required | Unique | Format / Values / Max | Comments |
| :--- | :--- | :---: | :---: | :--- | :--- |
| Batch Uid | `external_subject_key` | Yes | Yes | Max 64, multi-byte | Letters, digits, dashes, and periods only — no spaces. Must be unique across all Subjects, Courses, and Organizations. |
| Data Source Key | `data_source_key` | Yes | No | Max 256, multi-byte | May be supplied by the integration configuration rather than the file. |
| Subject ID | `subject_id` | Yes | Yes | Max 100, format: `{Title}__{Identifier}` | Two consecutive underscores separate title and identifier. Title: letters, numbers, hyphens, periods, underscores only. Identifier: letters and numbers only. No spaces. Example: `CHEM__abc123`. Cannot be changed after creation. |
| Subject Name | `subject_name` | Yes | No | Max 255, multi-byte | Complete title of the Subject used for display. |
| Subject Type | `subject_type` | Yes | No | See [Subject Type Values](#subject-type-values) | Indicates the curricular classification of the Subject. |
| Available | `available_ind` | No | No | `Y` \| `N` | Establishes availability within Blackboard Learn. |
| Description | `description` | No | No | No effective limit, multi-byte | Stored in the same underlying column as course description. |
| Replacement Batch Uid | `new_external_subject_key` | No | Yes | Max 64, multi-byte | Use only when a Subject's EXTERNAL KEY must change. |
| Replacement Data Source Batch Uid | `new_data_source_key` | No | No | — | UI mapping: `script.flatfile.SubjectReplacementDataSourceBatchUid` |
| Row Status | `row_status` | No | No | `enabled` \| `disabled` \| `deleted` | `enabled`: normal access. `disabled`: visible but not editable. `deleted`: scheduled for removal. |

---

## Subject Type Values

| Value | Description |
| :--- | :--- |
| `U` | Undergraduate |
| `G` | Graduate |
| `D` | Developmental / Remedial |
| `N` | Undergraduate Non-Transferable |
| `T` | Undergraduate Transferable |
| `P` | Professional / Continuing Education |

---

## Sample Feed File

Header row is required. Column order is flexible. Values are pipe-delimited.

```text
external_subject_key|data_source_key|subject_id|subject_name|subject_type|available_ind|row_status
CHEM-SUBJ|SIS-IMPORT-2025|CHEM__abc123|Chemistry|U|Y|enabled
```

---

## Notes

- **`subject_id` cannot be changed** after creation.
- **`subject_id` format requires two consecutive underscores** separating the title portion and the identifier portion (e.g. `CHEM__abc123`).
- **`external_subject_key` must be unique** across all Subjects, Courses, and Organizations — not just within Subjects.
