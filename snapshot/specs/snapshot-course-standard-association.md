---
title: "Snapshot Flat File — Course Standard Association"
id: snapshot-flatfile-course-standard-association
categories: SIS, Snapshot Flat File
published: "2026-04-22"
edited: "2026-04-22"
author: "Jeff Kelley, Principal Solutions Engineer, Blackboard Inc."
---

# Course Standard Association

**SIS Object:** Goal / Standard Association  
**Endpoint:** `/endpoint/standardsassociation/`  
**Insert/Update behavior:** Smart Insert or Update  
**Delete behavior:** Purge

The Course Standard Association object links Goals and Standards to Courses in Blackboard Learn. This object is notably lean — it has only two fields, both required.

---

## Endpoints

| Operation | URL |
| :--- | :--- |
| Store | `.../endpoint/standardsassociation/store` |
| Complete Refresh | `.../endpoint/standardsassociation/refresh` |
| Complete Refresh by Data Source | `.../endpoint/standardsassociation/refreshlegacy` |
| Delete | `.../endpoint/standardsassociation/delete` |

---

## Fields

| Field | Header | Required | Unique | Format / Values / Max | Comments |
| :--- | :--- | :---: | :---: | :--- | :--- |
| Standard / Goal Key | `std_sub_doc_key` | Yes | No | — | The unique identifier (batch_uid) of the Goal or Standard being associated. References a standard defined in the Goals / Standards catalog. |
| Course Key | `course_key` | Yes | No | Max 64 | The `external_course_key` of the Course to which the Goal or Standard will be associated. |

---

## Sample Feed File

Header row is required. Column order is flexible. Values are pipe-delimited.

```text
std_sub_doc_key|course_key
GOAL-STEM-CRITICAL-THINKING|MATH101-F25
```

---

## Notes

- **Delete behavior is Purge.** Deleted associations are permanently removed.
- **Minimum required headers:** `std_sub_doc_key`, `course_key`.
- **The Goal or Standard must already exist** in the Goals / Standards catalog before this association can be created.
- **No `data_source_key` or `row_status`** — this object has a simpler structure than other association objects.
