---
title: "Snapshot Flat File — Program"
id: snapshot-flatfile-program
categories: SIS, Snapshot Flat File
published: "2026-04-22"
edited: "2026-04-22"
author: "Jeff Kelley, Principal Solutions Engineer, Blackboard Inc."
---

# Program

**SIS Object:** Program  
**Endpoint:** `/endpoint/program/`  
**Insert/Update behavior:** Smart Insert or Update  
**Delete behavior:** Disable

The Program object creates and manages academic programs in Blackboard Learn. Programs are persisted as courses with a Program service level in the underlying data model and can be associated with Subjects via the Program to Subject Association object.

---

## Endpoints

| Operation | URL |
| :--- | :--- |
| Store | `.../endpoint/program/store` |
| Complete Refresh | `.../endpoint/program/refresh` |
| Complete Refresh by Data Source | `.../endpoint/program/refreshlegacy` |
| Delete | `.../endpoint/program/delete` |

---

## Fields

| Field | Header | Required | Unique | Format / Values / Max | Comments |
| :--- | :--- | :---: | :---: | :--- | :--- |
| Batch Uid | `external_program_key` | Yes | Yes | Max 64 | Permanent, non-changing identifier for the Program. |
| Data Source Key | `data_source_key` | Yes | No | Max 256, multi-byte | May be supplied by the integration configuration rather than the file. |
| Program ID | `program_id` | Yes | Yes | — | Short name used by the institution to uniquely identify the Program. Cannot be changed after creation. |
| Program Name | `program_name` | Yes | No | Max 255, multi-byte | Complete title of the Program used for display. |
| Program Type | `program_type` | Yes | No | See [Program Type Values](#program-type-values) | Indicates the degree-level classification of the Program. Maps to the underlying `course_type` column. |
| Available | `available_ind` | No | No | `Y` \| `N` | Establishes availability within Blackboard Learn. |
| Description | `description` | No | No | No effective limit, multi-byte | Stored in the same underlying column as course description. |
| Replacement Batch Uid | `new_external_program_key` | No | Yes | Max 64 | Use only when a Program's EXTERNAL KEY must change. |
| Replacement Data Source Batch Uid | `new_data_source_key` | No | No | — | UI mapping: `script.flatfile.ProgramReplacementDataSourceBatchUid` |
| Row Status | `row_status` | No | No | `enabled` \| `disabled` \| `deleted` | `enabled`: normal access. `disabled`: visible but not editable. `deleted`: scheduled for removal. |

---

## Program Type Values

Programs are persisted in Blackboard as courses with a Program service level. The `program_type` field maps to the underlying `course_type` column.

| Value | Description |
| :--- | :--- |
| `U` | Undergraduate |
| `G` | Graduate |

---

## Sample Feed File

Header row is required. Column order is flexible. Values are pipe-delimited.

```text
external_program_key|data_source_key|program_id|program_name|program_type|available_ind|row_status
PROG-BSCS|SIS-IMPORT-2025|PROG.BSCS|Bachelor of Science in Computer Science|U|Y|enabled
```

---

## Notes

- **Programs are persisted as courses** in Blackboard's data model with a Program service level. The `/program/` endpoint sets this automatically — do not supply `service_level` in Program feeds.
- **`program_type`** maps to the underlying `course_type` column (`U` or `G`). The stored value is the single-character code.
- **`program_id` cannot be changed** after creation.
- **Description** has no effective length limit — it is stored in the same underlying column as course description.
