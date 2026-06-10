---
title: "Snapshot Flat File — Terms"
id: snapshot-flatfile-terms
categories: SIS, Snapshot Flat File
published: "2026-04-22"
edited: "2026-04-22"
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
| Days of Use | `days_of_use` | No | No | Numeric | Number of days students may access courses after enrollment. Used when `duration` is `Fixed`. |
| Description | `description` | No | No | No limit | Description of the Term. |
| Duration | `duration` | No | No | `Continuous` \| `Range` \| `Fixed` | `Continuous`: always accessible. `Range`: between `start_date` and `end_date`. `Fixed`: set number of `days_of_use`. |
| End Date | `end_date` | No | No | `yyyymmdd` | The date the term stops being available. |
| Start Date | `start_date` | No | No | `yyyymmdd` | The date the term begins to be available. |
| Replacement Batch Uid | `new_external_term_key` | No | Yes | Max 256, multi-byte | Use only when a term's EXTERNAL KEY must change. |
| Replacement Data Source Batch Uid | `new_data_source_key` | No | No | — | UI mapping: `script.flatfile.TermReplacementDataSourceBatchUid` |
| Row Status | `row_status` | No | No | `enabled` \| `disabled` \| `deleted` | `enabled`: normal access. `disabled`: visible but not editable. `deleted`: scheduled for removal. |

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
- **Term Type (shipping 4000.15, production 7 May 2026):** The 4000.15 release note confirms Term Type sync via flat file integration. As of this writing the feed header and supported values are not published and the field does not appear in the custom header override list. The underlying database field exists and is visible as a mappable target in the field mapping UI on 4000.15 staging.
- **Term Hierarchy / Parent Term (UI: 4000.8, SIS: not yet announced):** Parent-child term relationships (Annual → Semester/Trimester/Quarter) shipped as a UI-only feature in 4000.8. No release note has announced SIS or REST support. The underlying field exists in the data model but no feed header or field mapping target row exists on any confirmed system. SIS support is expected in a future release 
