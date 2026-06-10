---
title: "Snapshot Flat File — Hierarchy User Association"
id: snapshot-flatfile-hierarchy-user-association
categories: SIS, Snapshot Flat File
published: "2026-04-22"
edited: "2026-04-22"
author: "Jeff Kelley, Principal Solutions Engineer, Blackboard Inc."
---

# Hierarchy User Association

**SIS Object:** User Association  
**Endpoint:** `/endpoint/userassociation/`  
**Insert/Update behavior:** Smart Insert or Update  
**Delete behavior:** Purge

The Hierarchy User Association object associates users with nodes in the Institutional Hierarchy.

---

## Endpoints

| Operation | URL |
| :--- | :--- |
| Store | `.../endpoint/userassociation/store` |
| Complete Refresh | `.../endpoint/userassociation/refresh` |
| Complete Refresh by Data Source | `.../endpoint/userassociation/refreshlegacy` |
| Delete | `.../endpoint/userassociation/delete` |

---

## Fields

| Field | Header | Required | Unique | Format / Values / Max | Comments |
| :--- | :--- | :---: | :---: | :--- | :--- |
| Batch Uid | `external_association_key` | Yes | Yes | Max 64 | Unique identifier for this user-to-node association. Recommended convention: concatenate the User and Node batch UIDs (e.g. `STU-100042_NODE.ENGR.DEPT`). Use a natural unique key from your source system if one exists. |
| Data Source Key | `data_source_key` | Yes | No | Max 256, multi-byte | May be supplied by the integration configuration rather than the file. |
| Node Batch Uid | `external_node_key` | Yes | No | Max 64 | The `external_node_key` of the target node. Also the Node Identifier found in Edit Node in the UI. |
| User Batch Uid | `external_user_key` | Yes | No | Max 64 | The `external_person_key` of the user to be associated with this node. |
| Replacement Batch Uid | `new_external_association_key` | No | Yes | Max 64, multi-byte | Use only when an association's EXTERNAL KEY must change. |
| Replacement Data Source Batch Uid | `new_data_source_key` | No | No | — | UI mapping: `script.flatfile.UserAssociationReplacementDataSourceBatchUid` |

---

## Sample Feed File

Header row is required. Column order is flexible. Values are pipe-delimited.

```text
external_association_key|data_source_key|external_node_key|external_user_key
STU-100042_NODE.ENGR.DEPT|SIS-IMPORT-2025|NODE.ENGR.DEPT|STU-100042
```

---

## Notes

- **Delete behavior is Purge.** Deleted associations are permanently removed.
- **Minimum required headers:** `external_association_key`, `data_source_key`, `external_node_key`, `external_user_key`.
- **`external_association_key`** must be unique. The recommended convention is to concatenate the User Batch Uid and Node Batch Uid separated by an underscore. If your source system has a natural unique key for this relationship, that may be used instead.
