---
title: "Snapshot Flat File — Terms"
id: snapshot-flatfile-terms
categories: SIS, Snapshot Flat File
published: "2026-04-22"
edited: "2026-07-10"
author: "Jeff Kelley, Principal Solutions Engineer, Blackboard Inc."
---

# Terms

**SIS Object:** Term  
**Endpoint:** `/endpoint/term/`  
**Insert/Update behavior:** Smart Insert or Update  
**Delete behavior:** Disable

The Term object creates and manages academic terms in Blackboard Learn. Terms control course availability windows and can be associated with courses via `external_term_key`.

---

## Endpoints

| Operation | URL |
| :--- | :--- |
| Store | `.../endpoint/term/store` |
| Complete Refresh | `.../endpoint/term/refresh` |
| Complete Refresh by Data Source | `.../endpoint/term/refreshlegacy` |
| Delete | `.../endpoint/term/delete` |

---

## Fields

| Field | Header | Required | Unique | Format / Values / Max | Comments |
| :--- | :--- | :---: | :---: | :--- | :--- |
| Batch Uid | `external_term_key` | Yes | Yes | Max 256, multi-byte | Short name used to uniquely identify the Term. Letters, digits, dashes, and periods only — no spaces. |
| Data Source Key | `data_source_key` | Yes | No | Max 256, multi-byte | May be supplied by the integration configuration rather than the file. |
| Name | `name` | Yes | No | Max 333 | Name of the term as displayed to users. |
| Available | `available_ind` | No | No | `Y` \| `N` | Establishes availability within Blackboard Learn. |
| Duration | `duration` | No | No | `Continuous` \| `Range` \| `Fixed` | `Continuous`: always accessible. `Range`: between `start_date` and `end_date`. `Fixed`: set number of `days_of_use`. |
| Start Date | `start_date` | No | No | `yyyymmdd` | The date the term begins to be available. |
| End Date | `end_date` | No | No | `yyyymmdd` | The date the term stops being available. |
| Row Status | `row_status` | No | No | `enabled` \| `disabled` \| `deleted` | `enabled`: normal access. `disabled`: visible but not editable. `deleted`: scheduled for removal. |
| Days of Use | `days_of_use` | No | No | Numeric | Number of days students may access courses after enrollment. Used when `duration` is `Fixed`. |
| Description | `description` | No | No | No limit | Description of the Term. |
| Parent Term Batch Uid | `external_parent_term_key` | No | No | Max 256, multi-byte | `external_term_key` of this term's parent (e.g. Annual → Semester/Trimester/Quarter). Set to `NONE` to remove an existing parent association. |
| Replacement Batch Uid | `new_external_term_key` | No | Yes | Max 256, multi-byte | Use only when a term's EXTERNAL KEY must change. |
| Replacement Data Source Batch Uid | `new_data_source_key` | No | No | — | UI mapping: `script.flatfile.TermReplacementDataSourceBatchUid` |
| Term Type | `term_type` | No | No | `a` \| `s` \| `t` \| `q` \| `i` \| `m` \| `u` | Classifies the term: Annual, Semester, Trimester, Quarter, Intersession, Module, Unspecified. |

---

## Sample Feed File

Header row is required. Column order is flexible. Values are pipe-delimited.

```text
external_term_key|data_source_key|name|available_ind|duration|start_date|end_date|row_status
TERM-F25|SIS-IMPORT-2025|Fall 2025|Y|Range|20250825|20251215|enabled
```

---

## Notes

- **`external_term_key`** may contain only letters, digits, dashes, and periods. No spaces or other punctuation.
- **Term availability** controls associated course availability when the term's `available_ind` is set to `N`.
- **Term Type and Parent Term** (`term_type`, `external_parent_term_key`) are documented in the [official header reference](https://help.anthology.com/blackboard/administrator/en/integrations/student-information-system--sis-/snapshot-flat-file/snapshot-flat-file-header-descriptions.html) and confirmed available via the Snapshot Flat File feed.
