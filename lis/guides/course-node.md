
# **Ellucian ILP → Blackboard Learn**  
## **IMS LIS Course → Department (Node) Association Guide**  
---

## **1) Overview & Assumptions**

This guide describes how to map **Ellucian ILP (IMS LIS)** course section data to **Blackboard Learn’s Institutional Hierarchy** using the **SIS Integration Framework**.

We assume:

- Your Blackboard **Institutional Hierarchy** already exists.
- The **lowest-level nodes** represent academic **departments**.
- Node values originate from your SIS and match ILP fields (e.g.,  
  **Name:** `PSY` • **ID:** `0256` • **Description:** "Psychology Department").

ILP must be configured to include the department metadata in the LIS **Course Section** XML.

Full XML example:  
🔗 https://github.com/jkelley-blackboard/SIS-Integration-Field-Mapping-Scripts/blob/main/xml_samples/ILP_LIS_course_section.xml

Department information appears in the `<org>` block:

```xml
<org>
  <orgName>
    <language>en-US</language>
    <textString>Psychology</textString>
  </orgName>
  <orgUnit>
    <language>en-US</language>
    <textString>PSY</textString>
  </orgUnit>
  <id>
    <language>en-US</language>
    <textString>0256</textString>
  </id>
</org>
```

To extract the department ID:

```javascript
var dept = data.courseSection.org.id;
```

Full working script reference:  
🔗 https://github.com/jkelley-blackboard/SIS-Integration-Field-Mapping-Scripts/blob/main/javascripts/LIS_course_primary_node_department.js

---

## **2) Mapping Department to Blackboard’s Primary Node (LIS)**

Blackboard Learn’s SIS Integration Framework requires two fields to establish a **primary node association** for a course:

1. `primary_external_node_key`  
2. `external_association_key`

These must be populated through **SIS field mapping scripts** (JavaScript-style functions) in the LIS feed configuration.

---

## **2.1 `primary_external_node_key`**

This determines the **node** where the course will appear.

**Recommended mapping**: use the department **ID** from `<org><id>`.

```javascript
(function () {
    var deptId = (data && data.courseSection && data.courseSection.org && data.courseSection.org.id) || "";
    return String(deptId).trim();  // Example: "0256"
})();
```

If your Blackboard node external IDs instead use department **codes** (like `PSY`), replace:

```javascript
data.courseSection.org.id
```

with:

```javascript
data.courseSection.org.orgUnit
```

---

## **2.2 `external_association_key`**

This key represents the **course ↔ node relationship** and must be **globally unique**.
The recomended format is: 
```
<courseSourcedId>=<deptId>
```

Example:

```
123456.202610=0256
```

### Example Script

```javascript
(function () {
    var deptId   = (data && data.courseSection && data.courseSection.org && data.courseSection.org.id) || "";
    var courseId = (data && data.courseSection && data.courseSection.sourcedId) || "";

    deptId   = String(deptId).trim();
    courseId = String(courseId).trim();

    // New required order: courseSourcedId=deptId
    return courseId && deptId ? (courseId + "=" + deptId) : "";
})();
```

This pattern ensures stability and avoids Blackboard database errors such as:

```
duplicate key value violates unique constraint "domain_course_coll_uid_ak1"
```

---

## **3) Secondary Nodes in LIS (Optional)**

LIS handles multi-node relationships as **repeating node-association elements**, but in Blackboard SIS mapping:

- Secondary nodes **must** be supplied as an **array**
- They **must** come from a **script**
- You **cannot** enter them directly as text
- Blackboard will generate **unique, non‑reusable keys** for LIS-based secondaries

Example placeholder:

```javascript
(function () {
    var nodes = [];  // add secondary node IDs here if needed
    return nodes;    // must be an array
})();
```

### ✔ Best practice  
If your institution frequently uses secondary nodes, handle them via **Snapshot Course Associations**, not LIS.

---

## **4) Recommended Overall Strategy**

- **Use LIS for primary node (department) placement** — mapping leverages ILP’s `<org>` block.  
- **Avoid secondary nodes via LIS unless absolutely necessary** — prefer Snapshot Associations for clarity and key control.  
- **Use `=` concatenation for association keys** with the order `courseSourcedId=deptId`.  
- **Keep node IDs consistent** — ensure Blackboard node external IDs match ILP `<org.id>` or `<orgUnit>` values.

---

- **ILP LIS Course Section XML Sample**  
  🔗 https://github.com/jkelley-blackboard/SIS-Integration-Field-Mapping-Scripts/blob/main/xml_samples/ILP_LIS_course_section.xml

- **Working Primary Node Mapping Script**  
  🔗 https://github.com/jkelley-blackboard/SIS-Integration-Field-Mapping-Scripts/blob/main/javascripts/LIS_course_primary_node_department.js

---
