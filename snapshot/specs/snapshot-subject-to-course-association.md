---
title: "Snapshot Flat File — Subject to Course Association"
id: snapshot-flatfile-subject-to-course-association
categories: SIS, Snapshot Flat File
published: "2026-04-22"
edited: "2026-04-22"
author: "Jeff Kelley, Principal Solutions Engineer, Blackboard Inc."
---

# Subject to Course Association

**SIS Object:** Subject to Course Association  
**Endpoint:** `/endpoint/subjecttocourseassociation/`  
**Insert/Update behavior:** Smart Insert or Update  
**Delete behavior:** Disable

The Subject to Course Association object links Courses to Subjects, classifying individual course offerings under their curricular subject area.

---

## Endpoints

| Operation | URL |
| :--- | :--- |
| Store | `.../endpoint/subjecttocourseassociation/store` |
| Complete Refresh | `.../endpoint/subjecttocourseassociation/refresh` |
| Complete Refresh by Data Source | `.../endpoint/subjecttocourseassociation/refreshlegacy` |
| Delete | `.../endpoint/subjecttocourseassociation/delete` |

---

## Fields

| Field | Header | Required | Unique | Format / Values / Max | Comments |
| :--- | :--- | :---: | :---: | :--- | :--- |
| Batch Uid | `external_association_key` | Yes | Yes | Max 64 | Unique identifier for this Subject-to-Course association. Recommended convention: concatenate the Subject and Course batch UIDs (e.g. `CHEM-SUBJ_MATH101-F25`). Note: Subject batch UIDs may contain double underscores — use a different separator such as a dash or colon to avoid ambiguity. Use a natural unique key from your source system if one exists. |
| Data Source Key | `data_source_key` | Yes | No | Max 256, multi-byte | May be supplied by the integration configuration rather than the file. |
| Course Batch Uid | `external_course_key` | Yes | No | Max 64 | The `external_course_key` of the Course being associated with the Subject. |
| Subject Batch Uid | `external_subject_key` | Yes | No | Max 64 | The `external_subject_key` of the Subject to which the Course is being associated. |

---

## Sample Feed File

Header row is required. Column order is flexible. Values are pipe-delimited.

```text
external_association_key|data_source_key|external_subject_key|external_course_key
CHEM-SUBJ_MATH101-F25|SIS-IMPORT-2025|CHEM-SUBJ|MATH101-F25
```

---

## Notes

- **Minimum required headers:** `external_association_key`, `data_source_key`, `external_course_key`, `external_subject_key`.
- **`external_association_key`** must be unique. The recommended convention is to concatenate the Subject and Course batch UIDs. Because Subject IDs use double underscores, use a different separator (e.g. a dash) when building the association key to avoid ambiguity.
- **Both the Subject and Course must already exist** before creating this association.
