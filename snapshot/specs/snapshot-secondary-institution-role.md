---
title: "Snapshot Flat File — Secondary Institution Role"
id: snapshot-flatfile-secondary-institution-role
categories: SIS, Snapshot Flat File
published: "2026-04-22"
edited: "2026-04-22"
author: "Jeff Kelley, Principal Solutions Engineer, Blackboard Inc."
---

# Secondary Institution Role

**SIS Object:** User Secondary Institution Role  
**Endpoint:** `/endpoint/secondaryinstrole/`  
**Insert/Update behavior:** Smart Insert or Update  
**Delete behavior:** Disable

The Secondary Institution Role object assigns additional institution roles to users. A user may hold multiple institution roles; this object manages the secondary assignments.

---

## Endpoints

| Operation | URL |
| :--- | :--- |
| Store | `.../endpoint/secondaryinstrole/store` |
| Complete Refresh | `.../endpoint/secondaryinstrole/refresh` |
| Complete Refresh by Data Source | `.../endpoint/secondaryinstrole/refreshlegacy` |
| Delete | `.../endpoint/secondaryinstrole/delete` |

---

## Fields

| Field | Header | Required | Unique | Format / Values / Max | Comments |
| :--- | :--- | :---: | :---: | :--- | :--- |
| Data Source Key | `data_source_key` | Yes | No | Max 256, multi-byte | May be supplied by the integration configuration rather than the file. |
| Secondary Institution Role ID | `role_id` | Yes | No | — | The identifier for the secondary institution role for this association. |
| User Batch Uid | `external_person_key` | Yes | No | Max 64 | The `external_person_key` (batch_uid) of the user. |
| Replacement Data Source Batch Uid | `new_data_source_key` | No | No | — | UI mapping: `script.flatfile.SecondaryInstRoleReplacementDataSourceBatchUid` |
| Row Status | `row_status` | No | No | `enabled` \| `disabled` \| `deleted` | `enabled`: normal access. `disabled`: visible but not editable. `deleted`: scheduled for removal. |

---

## Sample Feed File

Header row is required. Column order is flexible. Values are pipe-delimited.

```text
data_source_key|external_person_key|role_id|row_status
SIS-IMPORT-2025|STU-100042|ONLINE-STUDENT|enabled
```

---

## Notes

- **Deleted rows are not automatically removed.** Records set to `deleted` must be manually removed by an administrator.
- **`role_id`** must match a valid Institution Role ID configured on your system. See **Administrator Panel > Institution Roles**.
