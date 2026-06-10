---
title: "Snapshot Flat File — Course / Organization"
id: snapshot-flatfile-course
categories: SIS, Snapshot Flat File
published: "2026-04-22"
edited: "2026-04-22"
author: "Jeff Kelley, Principal Solutions Engineer, Blackboard Inc."
---

# Course / Organization

**SIS Object:** Course or Organization  
**Endpoint:** `/endpoint/course/`  
**Insert/Update behavior:** Smart Insert or Update  
**Delete behavior:** Disable

The Course object creates and updates Courses and Organizations in Blackboard Learn. Courses and Organizations use the same field structure but are submitted to separate endpoints and use different header names for key identifying fields. See header notes in the Fields table below.

---

## Endpoints

| Operation | URL |
| :--- | :--- |
| Store (Course) | `.../endpoint/course/course/store` |
| Complete Refresh (Course) | `.../endpoint/course/course/refresh` |
| Complete Refresh by Data Source (Course) | `.../endpoint/course/course/refreshlegacy` |
| Delete (Course) | `.../endpoint/course/course/delete` |
| Store (Organization) | `.../endpoint/course/organization/store` |
| Complete Refresh (Organization) | `.../endpoint/course/organization/refresh` |
| Complete Refresh by Data Source (Organization) | `.../endpoint/course/organization/refreshlegacy` |
| Delete (Organization) | `.../endpoint/course/organization/delete` |

---

## Fields

| Field | Header | Required | Unique | Format / Values / Max | Comments |
| :--- | :--- | :---: | :---: | :--- | :--- |
| Batch Uid | `external_course_key` | Yes | Yes | Max 64 | Use `external_organization_key` for Organizations. |
| Data Source Key | `data_source_key` | Yes | No | Max 256, multi-byte | May be supplied by the integration configuration rather than the file. |
| Course ID / Organization ID | `course_id` | Yes | Yes | Max 100 | Short name identifying the Course or Organization (e.g. `MATH101_F25`). Use `organization_id` for Organizations. Characters not allowed: space, `&`, `/`, `'`, `+`. Cannot be changed after creation. |
| Course Name / Organization Name | `course_name` | Yes | No | Max 255, multi-byte | Complete title used for display. Use `organization_name` for Organizations. |
| Available | `available_ind` | No | No | `Y` \| `N` | Establishes availability within Blackboard Learn. |
| Allow Guests | `allow_guest_ind` | No | No | `Y` \| `N` | Allows guest access. |
| Allow Observers | `allow_observer_ind` | No | No | `Y` \| `N` | Allows observer access. |
| Show In Catalog | `catalog_ind` | No | No | `Y` \| `N` | Establishes whether the Course or Organization appears in catalog. |
| Days of Use | `days_of_use` | No | No | Numeric, e.g. `120` | Number of days students may access after enrollment. Used when `duration` is set to `D`. |
| Description Page | `desc_page_ind` | No | No | — | **Deprecated.** Not currently supported. Do not use. |
| Duration | `duration` | No | No | See [Duration Values](#duration-values) | Schedules course availability window. |
| End Date | `end_date` | No | No | `yyyymmdd` | Date the course stops being available. |
| Enrollment End Date | `enroll_end` | No | No | `yyyymmdd` | Date that enrollment is no longer available. |
| Enrollment Start Date | `enroll_start` | No | No | `yyyymmdd` | Date that enrollment may begin. |
| Enrollment Type | `enroll_option` | No | No | `instructor` \| `self` \| `email` | Determines the enrollment method. |
| Fee | `fee` | No | No | Numeric, 2 decimal places, e.g. `1500.00` | Fee associated with this Course or Organization. |
| Institution Name | `institution_name` | No | No | Max 255, multi-byte | The name of the institution. |
| Language Pack | `locale` | No | No | Max 20, e.g. `fr_FR` | Identifier for the preferred language pack. |
| Locked Out | `lockout_ind` | No | No | `Y` \| `N` | If `Y`, access is restricted based on `end_date` and `start_date`. |
| Maximum Disk Usage (soft limit) | `soft_limit` | No | No | Numeric bytes, e.g. `10485760` for 10MB | Triggers warning emails when course storage reaches this limit. |
| Primary Node Batch Uid | `primary_external_node_key` | No | No | — | External key of the primary institutional hierarchy node for this course. |
| Service Level Type | `service_level` | No | No | See [Service Level Values](#service-level-values) | Specifies the type of course. Not typically used in data feeds — set automatically by the endpoint. |
| Source Copy Key | `template_course_key` | No | No | Max 64, multi-byte | External key of the content source for copy operations. Use `template_organization_key` for organizations. |
| Start Date | `start_date` | No | No | `yyyymmdd` | Date the course begins to be available. |
| Term Key | `external_term_key` | No | No | Max 256 | External key of the term to which this course is associated. |
| Replacement Batch Uid | `new_external_course_key` | No | Yes | Max 64, multi-byte | Use only when the EXTERNAL KEY must change. Use `new_external_organization_key` for organizations. |
| Replacement Data Source Batch Uid | `new_data_source_key` | No | No | — | UI mapping: `script.flatfile.CourseReplacementDataSourceBatchUid` |
| Row Status | `row_status` | No | No | `enabled` \| `disabled` \| `deleted` | `enabled`: normal access. `disabled`: visible but not editable. `deleted`: scheduled for removal. |

---

## Duration Values

| Value | Description |
| :--- | :--- |
| `C` | Continuous — always accessible |
| `R` | Range — between `start_date` and `end_date` |
| `D` | Fixed — N days from enrollment (see `days_of_use`) |
| `T` | Term-dictated — controlled by the associated term |

---

## Service Level Values

| Value | Description |
| :--- | :--- |
| `F` | Full — standard Course |
| `C` | Community — Organization |
| `S` | System — limited functions |
| `R`, `T` | Not used |

---

## Sample Feed File

Header row is required. Column order is flexible. Values are pipe-delimited.

```text
external_course_key|data_source_key|course_id|course_name|available_ind|duration|start_date|end_date|external_term_key|row_status
MATH101-F25|SIS-IMPORT-2025|MATH101_F25|Calculus I - Fall 2025|Y|R|20250825|20251215|TERM-F25|enabled
```

---

## Notes

- **Courses and Organizations share the same field structure** but use different header names for key fields (`course_id` vs `organization_id`, `course_name` vs `organization_name`, `external_course_key` vs `external_organization_key`) and are submitted to separate endpoints.
- **`course_id` / `organization_id` cannot be changed** after creation.
- **`service_level`** is set automatically by the endpoint. Do not supply this field in feeds — the `/course/` endpoint sets `F` and `/organization/` sets `C`.
- **Data Source Key** may be supplied by the integration configuration and does not need to appear in the file if so.
