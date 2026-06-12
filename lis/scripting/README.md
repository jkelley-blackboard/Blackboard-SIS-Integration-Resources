# LIS Custom Field Mapping Scripts and Guides

This directory contains JavaScript field mapping scripts and supporting guides for configuring the Blackboard LIS SIS Integration.

Custom field mapping scripts are entered directly in the SIS Integration Framework under **Advanced Configuration → Use a Custom Script**. They receive the incoming SIS data object as `data` and a helper API as `helper`, and return the value to be written to the mapped field.

> Reference documentation for the scripting environment is also available on each Blackboard deployment at:
> `/webapps/dataIntegration/docs/custom_script_examples.html`

---

## Guides

### `custom_scripting_help.md`
Overview of the custom field mapping scripting environment: JavaScript syntax, the `data` and `helper` global variables, the full `ScriptHelper` API (`getBatchUid`, `getXPathString`, `skipRecord`, `skipAttribute`, logging methods, etc.), and a library of example scripts covering string manipulation, value normalization, null handling, and XPath extraction.

### `course-node.md`
Step-by-step guide for mapping Ellucian ILP course section data to Blackboard's Institutional Hierarchy using the LIS feed. Covers how to extract department metadata from the `<org>` block in the LIS XML, construct the `primary_external_node_key` and `external_association_key` field mapping scripts, handle secondary node associations, and recommended strategy for node placement via LIS vs. Snapshot.

---

## Scripts

### `LIS_course_primary_node_department.js`
**Field:** `Primary Node Batch Uid`

Maps a course section to its primary Institutional Hierarchy node by returning the department ID from `data.courseSection.org.id`. Logs a warning and exits if the department code is missing. Pair this with an association key script (see `course-node.md`).

### `LIS_course_section_end_date_update.js`
**Field:** Course end date

Extends a course's end date by 8 or 14 days based on term ID format:
- 6-character term IDs (e.g., `2024SP`) → +14 days
- All others → +8 days

Skips the record if start date or term ID is missing. Sets the final time to 23:59:59.

### `LIS_primaryInstitutionRoles.js`
**Field:** Primary Institution Role / System Role

Maps incoming LIS institution role values to Blackboard system role constants:

| LIS value | Blackboard value |
|---|---|
| `Student` | `STUDENT` |
| `Instructor` | `FACULTY` |
| `Staff` | `STAFF` |

Skips the record if no role is found.

### `LIS_secondaryInstitutionRoles.js`
**Field:** `secondaryInstRoles`

Maps secondary institution role values from the LIS person record to valid Blackboard institution role IDs. A person may carry multiple secondary roles alongside their primary role — all are mapped and returned as an array.

Blackboard reads secondary `<institutionRole>` elements natively (those that omit `<primaryroletype>` or set it to false) and flags them as invalid when the role ID doesn't exist in the system. This script intercepts that mapping before the validation runs.

| LIS value | Blackboard value |
|---|---|
| `Learner` | `LSCO_Student` |
| `Instructor` | `LSCO_Faculty` |
| `LSCO_Staff` | `LSCO_Staff` |

Unmapped values pass through unchanged. Secondary roles are optional — if none are present, skips the attribute (not the record) and logs at info level.

> **Note:** Uses `getSecondaryInstitutionRoles()` (plural). This method name has not yet been confirmed against a live instance's JavaDocs — if it fails, try `getSecondaryInstitutionRole()` (singular), which may return only the first secondary role. See `/webapps/dataIntegration/docs/` on any Learn deployment.

### `LIS_user_add_node.js`
**Field:** Added Node Batch UID

Assigns users to Institutional Hierarchy nodes based on primary institution role. Returns an array (required by the Added Node field). Handles common role value variants (`S`, `Learner`, `P`, `Faculty`, etc.). Includes two implementations — an `if/else` chain and an equivalent object-map approach.

| Role values | Node |
|---|---|
| `Student`, `S`, `Learner` | `STUDENT` |
| `Instructor`, `P`, `Faculty` | `FACULTY` |
| `Staff` | `STAFF` |
| `PROSPECTIVE_STUDENT` | `PROSPECTIVE_STUDENT` |
