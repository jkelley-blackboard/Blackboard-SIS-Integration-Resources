---
title: "Snapshot Flat File — Course / Organization"
id: snapshot-flatfile-course
categories: SIS, Snapshot Flat File
published: "2026-04-22"
edited: "2026-07-10"
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
| Available | `available_ind` | No | No | `Y` \| `N` | Establishes availability within Blackboard Learn. Ignored if `use_term_availability_ind` is `Y`, in which case the associated Term's availability governs instead. |
| Allow Guests | `allow_guest_ind` | No | No | `Y` \| `N` | Allows guest access. |
| Allow Observers | `allow_observer_ind` | No | No | `Y` \| `N` | Allows observer access. |
| Classification Key | `classification_key` | No | No | Max 450, multi-byte | Sets the Subject Area / Discipline shown on the Create/Edit Course page — effectively deprecated, with no associated functionality elsewhere in Learn. Not related to the Subject, Program, Goals, or Outcomes features. |
| Complete | `complete` | No | No | `Y` \| `N` | Marks the Course/Organization as complete. Disables notifications and may block other updates in the future. Distinct from `lockout_ind`. Not currently documented on Blackboard's help site. |
| Maximum Disk Usage (hard limit) | `abs_limit` | No | No | Numeric bytes, e.g. `10485760` for 10MB | Hard storage limit — uploads are blocked once course storage reaches this limit. Insert only — can only be updated via the GUI, not through the SIS framework. |
| Show In Catalog | `catalog_ind` | No | No | `Y` \| `N` | Establishes whether the Course or Organization appears in catalog. |
| Days of Use | `days_of_use` | No | No | Numeric, e.g. `120` | Number of days students may access after enrollment. Used when `duration` is set to `D`. |
| Description | `description` | No | No | Max 4000, multi-byte | Complete description of the Course. |
| Description Page | `desc_page` | No | No | — | **Deprecated.** Not currently supported. Do not use. |
| Duration | `duration` | No | No | See [Duration Values](#duration-values) | Schedules course availability window. |
| End Date | `end_date` | No | No | `yyyymmdd` | Date the course stops being available. |
| Enrollment Access Code | `enroll_access_code` | No | No | Max 50 | Access code students use when enrolling in the course. |
| Enrollment End Date | `enroll_end` | No | No | `yyyymmdd` | Date that enrollment is no longer available. |
| Enrollment Start Date | `enroll_start` | No | No | `yyyymmdd` | Date that enrollment may begin. |
| Enrollment Type | `enroll_option` | No | No | `instructor` \| `self` \| `email` | Determines the enrollment method. |
| Fee | `fee` | No | No | Numeric, 2 decimal places, e.g. `1500.00` | Fee associated with this Course or Organization. |
| Institution Name | `institution_name` | No | No | Max 255, multi-byte | The name of the institution. |
| Language Pack | `locale` | No | No | Max 20, e.g. `fr_FR` | Identifier for the preferred language pack. |
| Enforce Language Pack | `locale_enforced` | No | No | `Y` \| `N` | Determines if the `locale` language pack is enforced when a user accesses the Course. |
| Locked Out | `lockout_ind` | No | No | `Y` \| `N` | If `Y`, access is restricted based on `end_date` and `start_date`. |
| Cross Listed Course Batch Uid | `parent_course_key` | No | No | Max 64, multi-byte | `external_course_key` of the parent course, if this course is cross-listed as a child of another course. |
| Maximum Disk Usage (soft limit) | `soft_limit` | No | No | Numeric bytes, e.g. `10485760` for 10MB | Triggers warning emails when course storage reaches this limit. |
| Educational Pace | `pace` | No | No | `Self` \| `Instructor` | Indicates whether the Course is self-paced or instructor-led. |
| Primary Association Batch Uid | `external_association_key` | No | Yes | Max 64 | External key of the primary Institutional Hierarchy node association. Required together with `primary_external_node_key` when creating a course associated with a hierarchy node — copies that node's tool setting defaults on course creation. |
| Primary Node Batch Uid | `primary_external_node_key` | No | No | Max 256 | External key of the primary institutional hierarchy node for this course. Required together with `external_association_key` (see above). |
| Service Level Type | `service_level` | No | No | See [Service Level Values](#service-level-values) | **Deprecated.** Set automatically by the endpoint — do not supply, and never use it to define or change a record's type. Subjects, Programs, LOR, and system courses each have their own object spec/endpoint; do not attempt to represent them through the Course/Organization object. |
| Source Copy Key | `template_course_key` | No | No | Max 64, multi-byte | External key of the content source for copy operations. Use `template_organization_key` for organizations. |
| Start Date | `start_date` | No | No | `yyyymmdd` | Date the course begins to be available. |
| Term Key | `term_key` | No | No | Max 256 | External key of the term to which this course is associated. |
| Upload Limit | `upload_limit` | No | No | Numeric bytes, e.g. `10485760` for 10MB | Maximum size of a single file uploaded to the course. |
| Use Term Availability | `use_term_availability_ind` | No | No | `Y` \| `N` | If `Y`, the associated Term's `available_ind`, `start_date`, and `end_date` govern availability instead of the course's own values. |
| Replacement Batch Uid | `new_external_course_key` | No | Yes | Max 64, multi-byte | Use only when the EXTERNAL KEY must change. Use `new_external_organization_key` for organizations. |
| Replacement Data Source Batch Uid | `new_data_source_key` | No | No | — | UI mapping: `script.flatfile.CourseReplacementDataSourceBatchUid` |
| Row Status | `row_status` | No | No | `enabled` \| `disabled` \| `deleted` | `enabled`: normal access. `disabled`: visible but not editable. `deleted`: scheduled for removal. |
| Course View / Organization View | `course_experience` | No | No | `Original` \| `Ultra` \| `Instructor choice` | Determines which course view will appear for new courses. Use `organization_experience` for Organizations. This field is insert only and can't be updated through the SIS framework. **`Original` and `Instructor choice` will not be supported after the end of 2026** — no new Original-experience courses will be possible after that date. |

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

**Deprecated.** This field must not be used to define or update a record's type. It is set automatically by the endpoint (`/course/` sets `F`, `/organization/` sets `C`) and is not a mechanism for creating Subjects, Programs, LOR objects, or system courses — those each have their own dedicated spec and file type. Do not attempt to use Course/Organization methods for them.

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
external_course_key|data_source_key|course_id|course_name|available_ind|duration|start_date|end_date|term_key|row_status
MATH101-F25|SIS-IMPORT-2025|MATH101_F25|Calculus I - Fall 2025|Y|R|20250825|20251215|TERM-F25|enabled
```

---

## Notes

- **Courses and Organizations share the same field structure** but use different header names for key fields (`course_id` vs `organization_id`, `course_name` vs `organization_name`, `external_course_key` vs `external_organization_key`) and are submitted to separate endpoints.
- **`course_id` / `organization_id` cannot be changed** after creation.
- **`service_level`** is deprecated and set automatically by the endpoint (`/course/` sets `F`, `/organization/` sets `C`). Do not supply this field, and never use it to define or update a record's type — Subjects, Programs, LOR objects, and system courses each have their own spec and file type; do not attempt to use Course/Organization methods for them.
- **Data Source Key** may be supplied by the integration configuration and does not need to appear in the file if so.
- **`course_experience` / `organization_experience`.** `Original` and `Instructor choice` will not be supported after the end of 2026 — no new Original-experience courses or organizations will be possible after that date.
- **`classification_key`** (Subject Area / Discipline) is effectively deprecated — it has no associated functionality elsewhere in Learn and is unrelated to the Subject, Program, Goals, or Outcomes features.
