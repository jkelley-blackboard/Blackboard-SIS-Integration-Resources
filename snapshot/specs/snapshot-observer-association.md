---
title: "Snapshot Flat File — Observer Association"
id: snapshot-flatfile-observer-association
categories: SIS, Snapshot Flat File
published: "2026-04-22"
edited: "2026-04-22"
author: "Jeff Kelley, Principal Solutions Engineer, Blackboard Inc."
---

# Observer Association

**SIS Object:** Observer Association  
**Endpoint:** `/endpoint/associateobserver/`  
**Insert/Update behavior:** Smart Insert or Update  
**Delete behavior:** Disable

The Observer Association object links Observer-role users to Student-role users, granting the observer visibility into the student's courses and activity.

---

## Endpoints

| Operation | URL |
| :--- | :--- |
| Store | `.../endpoint/associateobserver/store` |
| Complete Refresh | `.../endpoint/associateobserver/refresh` |
| Complete Refresh by Data Source | `.../endpoint/associateobserver/refreshlegacy` |
| Delete | `.../endpoint/associateobserver/delete` |

---

## Fields

| Field | Header | Required | Unique | Format / Values / Max | Comments |
| :--- | :--- | :---: | :---: | :--- | :--- |
| Data Source Key | `data_source_key` | Yes | No | Max 256, multi-byte | May be supplied by the integration configuration rather than the file. |
| Observed Student | `external_user_key` | Yes | No | Max 64, multi-byte | The `external_person_key` of the student being observed. Must have the Institution Role of Student. |
| Observer | `external_observer_key` | Yes | No | Max 64, multi-byte | The `external_person_key` of the observer. Must have the system role of Observer. |
| Replacement Data Source Batch Uid | `new_data_source_key` | No | No | — | UI mapping: `script.flatfile.AssociateObserverReplacementDataSourceBatchUid` |
| Row Status | `row_status` | No | No | `enabled` \| `disabled` \| `deleted` | `enabled`: normal access. `disabled`: visible but not editable. `deleted`: scheduled for removal. |

---

## Sample Feed File

Header row is required. Column order is flexible. Values are pipe-delimited.

```text
data_source_key|external_user_key|external_observer_key|row_status
SIS-IMPORT-2025|STU-100042|OBS-200099|enabled
```

---

## Notes

- **The observed user must have Institution Role of Student** and the observer must have system role of Observer. Associations referencing users without the correct roles will fail.
