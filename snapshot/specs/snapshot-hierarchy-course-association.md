---
title: "Snapshot Flat File — Hierarchy Course Association"
id: snapshot-flatfile-hierarchy-course-association
categories: SIS, Snapshot Flat File
published: "2026-04-22"
edited: "2026-04-22"
author: "Jeff Kelley, Principal Solutions Engineer, Blackboard Inc."
---

# Hierarchy Course Association

**SIS Object:** Course / Organization Association  
**Endpoint:** `/endpoint/courseassociation/`  
**Insert/Update behavior:** Smart Insert or Update  
**Delete behavior:** Purge

The Hierarchy Course Association object associates Courses and Organizations with nodes in the Institutional Hierarchy.

---

## Endpoints

| Operation | URL |
| :--- | :--- |
| Store (Course) | `.../endpoint/courseassociation/courseassociation/store` |
| Complete Refresh (Course) | `.../endpoint/courseassociation/courseassociation/refresh` |
| Complete Refresh by Data Source (Course) | `.../endpoint/courseassociation/courseassociation/refreshlegacy` |
| Delete (Course) | `.../endpoint/courseassociation/courseassociation/delete` |
| Store (Organization) | `.../endpoint/courseassociation/organizationassociation/store` |
| Complete Refresh (Organization) | `.../endpoint/courseassociation/organizationassociation/refresh` |
| Complete Refresh by Data Source (Organization) | `.../endpoint/courseassociation/organizationassociation/refreshlegacy` |
| Delete (Organization) | `.../endpoint/courseassociation/organizationassociation/delete` |

---

## Fields

| Field | Header | Required | Unique | Format / Values / Max | Comments |
| :--- | :--- | :---: | :---: | :--- | :--- |
| Batch Uid | `external_association_key` | Yes | Yes | Max 64 | Unique identifier for this course-to-node association. Recommended convention: concatenate the Course and Node batch UIDs (e.g. `MATH101-F25_NODE.ENGR.DEPT`). Use a natural unique key from your source system if one exists. |
| Course / Org Batch Uid | `external_course_key` | Yes | No | Max 64 | The `external_course_key` of the course to be associated. Use `external_organization_key` for Organizations. |
| Data Source Key | `data_source_key` | Yes | No | Max 256, multi-byte | May be supplied by the integration configuration rather than the file. |
| Node Batch Uid | `external_node_key` | Yes | No | Max 64, multi-byte | The `external_node_key` of the target node. |
| Primary Association Indicator | `is_primary_association` | No | No | `Y` \| `N` | Designates this as the primary association when a course is associated with multiple nodes. |
| Replacement Batch Uid | `new_external_association_key` | No | Yes | Max 64, multi-byte | Use only when an association's EXTERNAL KEY must change. |
| Replacement Data Source Batch Uid | `new_data_source_key` | No | No | — | UI mapping: `script.flatfile.CourseAssociationReplacementDataSourceBatchUid` |

---

## Sample Feed File

Header row is required. Column order is flexible. Values are pipe-delimited.

```text
external_association_key|data_source_key|external_node_key|external_course_key|is_primary_association
MATH101-F25_NODE.ENGR.DEPT|SIS-IMPORT-2025|NODE.ENGR.DEPT|MATH101-F25|Y
```

---

## Notes

- **Delete behavior is Purge.** Deleted associations are permanently removed.
- **Minimum required headers:** `external_association_key`, `data_source_key`, `external_node_key`, `external_course_key`.
- **Course and Organization associations use the same fields** but are submitted to separate endpoints (`/courseassociation/` or `/organizationassociation/`).
- **`external_association_key`** must be unique. The recommended convention is to concatenate the Course Batch Uid and Node Batch Uid. If your source system has a natural unique key, that may be used instead.
