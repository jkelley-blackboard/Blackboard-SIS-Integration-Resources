# Sample Documents

Reference material downloaded from the **Sample Documents** link on the Student Information System Integrations admin page (Administrator Panel > Data Integration > Student Information System Integrations).

## Contents

| File | Format | What it is |
|---|---|---|
| `Custom Field Mapping Script Examples.html` | Static HTML | The same help page already available on any Learn deployment at `/webapps/dataIntegration/docs/custom_script_examples.html` — general custom-scripting syntax and `ScriptHelper` API reference, with example scripts against a generic `Person` object. |
| `data-integration-lis-final-javadoc.zip` / `data-integration-lis-final-javadoc/` | Generated JavaDoc site | The full Java class reference for `blackboard.dataintegration.lis.data.*` — the actual object model behind the `data` global variable in **LIS** custom field mapping scripts. |
| `data-integration-flatfile-javadoc.zip` / `data-integration-flatfile-javadoc/` | Generated JavaDoc site | The full Java class reference for `blackboard.dataintegration.flatfile.*` — the object model and mapping/handler classes behind **Snapshot Flat File** custom field mapping scripts. |

---

## Value assessment

### `Custom Field Mapping Script Examples.html`
No new information — its "Introduction," `ScriptHelper` API list, and script examples match [`lis/scripting/custom_scripting_help.md`](../lis/scripting/custom_scripting_help.md) method-for-method (`getBatchUid`, `getXPathString`, `getHelper`, `skipAttribute`, `skipAttributeIfNull`, `skipRecord`, `skipRecordIfNull`, and the four logging methods). Useful as an authoritative cross-check confirming that transcription is accurate, but doesn't add anything.

### LIS JavaDoc (`data-integration-lis-final-javadoc`)
This is high-value — it's ground truth for the method chains documented (with varying confidence) in [`lis/data-models/README.md`](../lis/data-models/README.md). Cross-checking it against that doc found:

A full row-by-row comparison against `lis/data-models/README.md` is below, under [Discrepancy List](#discrepancy-list-for-lisdata-modelsreadmemd-for-review) — most rows in the Person, Course Section, and Course Membership tables need some correction, ranging from a missing `.get(0)` to method names that don't exist at all.

### Flat File (Snapshot) JavaDoc (`data-integration-flatfile-javadoc`)
This is new territory relative to the rest of the repo. `snapshot/` currently documents field-level specs and posting mechanics only — it has no coverage of custom field-mapping scripting for Snapshot Flat File, the way `lis/scripting/` does for LIS. This javadoc confirms that capability exists as its own thing:

- `FlatFileScriptingHelper` — the likely `helper`-equivalent for Snapshot custom scripts.
- `FlatFileRecord` — a much flatter object model than LIS's, exposing `getFields()`, `getRawData()`, and `getValues()` rather than a typed hierarchy of nested objects.
- A `mapping`/`mapping.handler` package with a `*SISObjectType` and `*DataHandler` class for essentially every object already covered in `snapshot/specs/` (Course, Membership, Node, Term, Subject, Program, Category, and associations) — a 1:1 correspondence with the existing spec files' scope.

---

## Discrepancy List for `lis/data-models/README.md` (For Review)

Every row below was checked directly against the LIS javadoc class files. **Nothing in `data-models/README.md` has been changed yet** — this is the review list the fixes would be based on.

### 1. Person

| Field | Current | Status | What the javadoc actually shows |
|---|---|---|---|
| External Person Key / Batch UID | `data.getPerson().getSourcedGUID().getSourcedId()` | **Wrong nesting** | `getSourcedGUID()` is a method on `PersonRecord` (the `data` object itself), not on `Person`. Correct: `data.getSourcedGUID().getSourcedId()`. |
| Username / User ID | `data.getPerson().getUserName()` | **Method doesn't exist** | `Person` has no `getUserName()`. The value lives on `Roles.getUserId()` → `UserId.getValue()`: `data.getPerson().getRoles().get(0).getUserId().getValue()`. |
| First Name | `data.getPerson().getName().getGivenName()` | **Method doesn't exist** | `Person` has no `getName()`/`getGivenName()`. `Person.getNames()` returns `Map<String, Name>`; `Name` only exposes `getParts()` (a list) and `getType()` — no direct given/family accessor. Exact one-line replacement isn't determinable from the class shape alone; needs a live payload or the `Name`/part-type javadoc detail to confirm how "given" vs. "family" is keyed. |
| Last Name | `data.getPerson().getName().getFamilyName()` | **Method doesn't exist** | Same issue as First Name above. |
| Email Address | `data.getPerson().getEmail()` | **Method doesn't exist** | `Person` has no `getEmail()`. `Person.getContactInfo()` returns `Map<String, ContactInfo>`; `ContactInfo` has `getType()`/`getValue()`. Likely `data.getPerson().getContactInfo().get('EmailPrimary').getValue()` (the XML sample uses that key), but the key string itself isn't independently confirmed by this javadoc. |
| Primary Institution Role | `data.getPerson().getRoles().get(0).getPrimaryInstitutionRole().getValue()` | **Confirmed correct** | Every link checks out: `getRoles()` → `List<Roles>`, `Roles.getPrimaryInstitutionRole()` → `InstitutionRole`, `InstitutionRole.getValue()` → `String`. |
| Secondary Institution Roles | `data.getPerson().getRoles().getSecondaryInstitutionRoles()` | **Missing `.get(0)`** | Method name is confirmed correct and returns `List<InstitutionRole>`, but it's an instance method on `Roles`, not on `List<Roles>`. Should read `data.getPerson().getRoles().get(0).getSecondaryInstitutionRoles()`, matching the Primary Institution Role row's pattern. |
| Extensions | `data.getPerson().getExtensions().get('fieldName')` | **Confirmed correct** | `Person.getExtensions()` returns `Map<String, ExtensionField>`. |

### 2. Course Section

| Field | Current | Status | What the javadoc actually shows |
|---|---|---|---|
| External Course Key / SourcedId | `data.getCourseSection().getSourcedGUID().getSourcedId()` | **Wrong nesting** | Same pattern as Person: `getSourcedGUID()` lives on `CourseSectionRecord` (the `data` object), not `CourseSection`. Correct: `data.getSourcedGUID().getSourcedId()`. |
| Course Title / Name | `data.getCourseSection().getTitle()` | **Confirmed correct** | |
| Long Description | `data.getCourseSection().getCatalogDescription().getLongDescription()` | **Confirmed correct** | `getCatalogDescription()` returns `Description`, which has `getLongDescription()`. |
| Short Description | `data.getCourseSection().getCatalogDescription().getShortDescription()` | **Confirmed correct** | Same `Description` class, has `getShortDescription()`. |
| Data Source | `data.getCourseSection().getDataSource()` | **Confirmed correct** | |
| Start Date | `data.getCourseSection().getTimeFrames().get(0).getBegin()` | **Confirmed correct** | `getTimeFrames()` → `List<TimeFrame>`, `TimeFrame.getBegin()` exists. |
| End Date | `data.getCourseSection().getTimeFrames().get(0).getEnd()` | **Confirmed correct** | Same as above, `getEnd()` exists. |
| Term / Academic Session | `data.getCourseSection().getAcademicSession()` | **Confirmed correct** | |
| Department Name | `data.courseSection.org.orgUnit` | **Wrong property name** | `Org` has `getUnit()`, not `getOrgUnit()`. The XML element is `<orgUnit>`, but the Java accessor is `getUnit()` — under Rhino's JavaBean property-access convention that resolves as `.unit`, not `.orgUnit`. |
| Department ID | `data.courseSection.org.id` | **Confirmed correct** | `Org.getId()` exists. |
| Available Flag | `data.getCourseSection().getIsAvailable()` | **Method doesn't exist** | No `getIsAvailable()` anywhere on `CourseSection`. Availability is `getStatus()`, returning a `String` — `"Active"` or `"Inactive"` — not a boolean. |

### 3. Course Membership

| Field | Current | Status | What the javadoc actually shows |
|---|---|---|---|
| External Course Key | `data.getMembership().getCourseSection().getSourcedGUID().getSourcedId()` | **Method doesn't exist** | `Membership` has no `getCourseSection()` at all. It exposes `getCollectionSourcedId()` directly — likely just `data.getMembership().getCollectionSourcedId()`, no nested `CourseSection` object. |
| External Person Key | `data.getMembership().getPerson().getSourcedGUID().getSourcedId()` | **Method doesn't exist** | `Membership` has no `getPerson()`. Real chain: `data.getMembership().getMember().getPersonSourcedId()` — `Member.getPersonSourcedId()` returns a plain `String`, no nested `SourcedGUID`. |
| Role (Student / Instructor) | `data.getMembership().getRole()` | **Method doesn't exist** | `Membership` has no `getRole()`. Real chain: `data.getMembership().getMember().getRoles().get(0).getRoleType()` — `Member.getRoles()` returns `List<Role>`, `Role.getRoleType()` returns `String`. |
| Enrollment Date | `data.getMembership().getEnrollmentDate()` | **Method doesn't exist** | No such method anywhere in this object graph. `Role` has `getTimeFrame()` and `getDateTime()` — one of these may represent it, but neither is named "enrollment date" and which one (if either) actually holds it isn't confirmed here. |
| Availability | `data.getMembership().getIsAvailable()` | **Method doesn't exist** | No such method anywhere in this object graph. `Role` has `getStatus()` (String) — possibly analogous to `CourseSection.getStatus()`, but not confirmed to mean the same thing here. |
| Data Source | `data.getMembership().getDataSource()` | **Confirmed correct** | |

### 4. Term (Group Record)

| Field | Current | Status | What the javadoc actually shows |
|---|---|---|---|
| Term Name | `data.getGroup().getDescription().getShortDescription()` | **Confirmed correct** | `Group.getDescription()` returns `Description`, which has `getShortDescription()`. |
| Start Date | `data.getGroup().getTimeframe().getBegin()` | **Wrong casing** | The real method is `getTimeFrame()` (capital F), not `getTimeframe()`. Java is case-sensitive — this would fail to compile/resolve as literally written. |
| End Date | `data.getGroup().getTimeframe().getEnd()` | **Wrong casing** | Same issue — should be `getTimeFrame()`. |
| Sourced ID | `data.getSourcedGUID().getSourcedId()` | **Confirmed correct** | `GroupRecord.getSourcedGUID()` exists directly on `data`, matching this row's (correct, un-nested) pattern — notably the one place the current doc already uses this shape correctly, which is what tipped off the Person/Course Section nesting errors above. |
| Data Source | `data.getGroup().getDataSource()` | **Confirmed correct** | |

---

## Suggested next steps (not yet acted on)

1. Work through the [Discrepancy List](#discrepancy-list-for-lisdata-modelsreadmemd-for-review) above and decide which corrections to apply to `lis/data-models/README.md` — several are one-line fixes, but First/Last Name and Email Address need a live test payload (or a look at `Name`'s and `ContactInfo`'s actual key/type values) to determine the real one-liner, not just this javadoc.
2. Update `LIS_secondaryInstitutionRoles.js` and `lis/scripting/README.md` to drop the singular-vs-plural hedge on `getSecondaryInstitutionRoles()` now that it's confirmed, and to add the missing `.get(0)`.
3. Consider whether Snapshot Flat File custom scripting deserves its own guide (mirroring `lis/scripting/custom_scripting_help.md`), now that this javadoc confirms the capability and its object model exist.
4. The raw javadoc HTML/zips are now `.gitignore`d (not tracked) — only this README and the small `Custom Field Mapping Script Examples.html` file are tracked, keeping the ~12 MB / 550+ generated files out of version control.
