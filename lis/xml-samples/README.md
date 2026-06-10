# The sample XML files in this repository are provided in two formats:

- Uploadable XML – files that are correctly structured and can be manually uploaded into Blackboard for testing and validation.
- Guidance-only XML – files included as examples to demonstrate configuration patterns. These are not in a directly uploadable form and must be adapted before use.

## Files in this directory

| File | Format | Purpose |
|---|---|---|
| `LIS_courseSection_uploadable_1.xml` | Uploadable | Minimal course section example |
| `LIS_courseSection_uploadable_2.xml` | Uploadable | Full course section example |
| `ILP_LIS_course_section.xml` | Guidance-only | Native ILP request format (not directly uploadable) |
| `sample_LIS2_term.xml` | Guidance-only | LIS 2.0 term (group) record example |

## The Uploadable Wrapper (`<bulkDataRecord>`)

Manual uploads through the Blackboard admin UI require a `<bulkDataRecord>` envelope that packages a LIS operation with explicit service and parameter metadata. This differs from the native format the Integration Layer Provider (ILP) sends automatically.

### Structure

```xml
<bulkDataRecord>
  <transactionRecord>
    <transactionOpIdentifier>tx1</transactionOpIdentifier>
    <serviceName>CourseManagementService</serviceName>
    <interfaceName>CourseSectionManager</interfaceName>
    <operationName>replaceCourseSection</operationName>
    <parameterSet>
      <parameterRecord>
        <parameterInvoc>In</parameterInvoc>
        <parameterName>sourcedId</parameterName>
        <parameterType>GUID</parameterType>
        <parameterValue><!-- course section sourcedId --></parameterValue>
      </parameterRecord>
      <parameterRecord>
        <parameterInvoc>In</parameterInvoc>
        <parameterName>courseSectionRecord</parameterName>
        <parameterType>CourseSectionRecord</parameterType>
        <parameterValue>
          <courseSectionRecord>
            <!-- course section data -->
          </courseSectionRecord>
        </parameterValue>
      </parameterRecord>
    </parameterSet>
  </transactionRecord>
</bulkDataRecord>
```

### Uploadable format vs. native ILP format

The inner course section data is the same in both formats. The differences are in the outer structure:

| | Uploadable (`<bulkDataRecord>`) | Native ILP (`<replaceCourseSectionRequest>`) |
|---|---|---|
| **Root element** | `<bulkDataRecord>` | `<replaceCourseSectionRequest xmlns="...">` |
| **Namespace** | None | IMS LIS CMS v1.0 on root element |
| **Service metadata** | Explicit (`serviceName`, `interfaceName`, `operationName`) | Implied by namespace and element name |
| **Data location** | Nested inside `<parameterSet>` → `<parameterValue>` | Direct children of root |
| **Timestamp format** | `2026-01-09T05:00:00` (no Z suffix) | `2026-01-09T05:00:00Z` (UTC Z suffix) |
| **`<timeFrame>` extras** | Includes `<restrict>` and `<adminPeriod>` | Begin and end dates only |

### Key fields

- **`transactionOpIdentifier`** – A unique identifier for this transaction record within the file (e.g., `tx1`, `tx2`). Must be unique if a file contains multiple `<transactionRecord>` blocks.
- **`sourcedId`** (first `parameterRecord`) – The external identifier for the course section. Must match the `sourcedId` inside the `courseSectionRecord`.
- **`restrict`** – Controls whether the term date range is enforced. `true` = use dates; `false` = continuous enrollment.
- **`adminPeriod`** – The term identifier associated with this course section.
