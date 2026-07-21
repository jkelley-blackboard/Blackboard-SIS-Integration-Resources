# IMS LIS User → Node Association Guide

This guide describes how to map incoming LIS Person role data to Institutional Hierarchy node placements using the SIS Integration Framework.

For the equivalent Course → Node (department) placement guide, see [course-node.md](course-node.md).

---

## 1) Overview & Assumptions

We assume:

- Your Blackboard **Institutional Hierarchy** already exists — typically created and maintained via a [Snapshot Hierarchy Node](../../snapshot/specs/snapshot-hierarchy-node.md) feed extracted from Banner.
- Unlike Course → Node placement, which is department-based (node keys come from SIS org unit data), User → Node placement here is **role-based**: a fixed set of top-level nodes exist for each primary institution role category (e.g. `STUDENT`, `FACULTY`, `STAFF`, `PROSPECTIVE_STUDENT`), and the node external keys match those values exactly. These node key values are illustrative — confirm they match your own Institutional Hierarchy's actual node external keys before reusing this script as-is.
- The incoming LIS Person record's primary institution role is available via:

  ```javascript
  data.getPerson().getRoles().get(0).getPrimaryInstitutionRole().getValue()
  ```

  (see [data-models/README.md](../data-models/README.md#1-person)).

---

## 2) Mapping Role to Blackboard's Added Node Batch Uid

Blackboard Learn's SIS Integration Framework exposes a single field, **Added Node Batch Uid**, to assign a user to one or more Institutional Hierarchy nodes.

This differs from Course primary node placement (`primary_external_node_key` + `external_association_key`, two separate fields — see [course-node.md](course-node.md#2-mapping-department-to-blackboards-primary-node-lis)):

- Added Node Batch Uid returns an **array** of node external keys, not a single string — even when assigning a single node.
- There is no separate association-key field to populate here. Whether Blackboard generates the underlying association key internally for this field, the way [course-node.md](course-node.md#3-secondary-nodes-in-lis-optional) describes for LIS-based secondary course node associations, has not been independently confirmed for this field — treat as likely but unverified.

### Example Script

```javascript
(function() {
    // Assign users to IH node based on primaryInstitutionRole
    // Added Node BatchUid expects a list

    var sField = 'Added Node BatchUid Script: ';

    var primaryRoleObj = data.getPerson().getRoles().get(0).getPrimaryInstitutionRole().getValue();
    var primaryRole;

    if (primaryRoleObj) {
        primaryRole = primaryRoleObj + '';  // Convert to string
    } else {
        helper.logWarning(sField + 'Primary Institution Role not found. Skip Record');
        helper.skipRecord();
        return;  // Exit the function if primaryRole is not found
    }

    // This is a map of Role (key) to Node (value)
    var roleMap = {
        'Student': 'STUDENT',
        'S': 'STUDENT',
        'Learner': 'STUDENT',
        'Instructor': 'FACULTY',
        'P': 'FACULTY',
        'Faculty': 'FACULTY',
        'Staff': 'STAFF',
        'PROSPECTIVE_STUDENT': 'PROSPECTIVE_STUDENT'
    };

    var nodeList = [roleMap[primaryRole]];

    if (nodeList[0]) {
        helper.logInfo(sField + 'Mapping Node to ' + nodeList[0]);
        return nodeList;
    } else {
        helper.logInfo(sField + 'No NODE map for Primary Institution Role');
        return null;
    }
})();
```

Full working script reference: [`LIS_user_add_node.js`](LIS_user_add_node.js) — includes both this object-map implementation and an equivalent if/else chain.

---

## 3) Role Value Variants

| Role values matched | Node |
| :--- | :--- |
| `Student`, `S`, `Learner` | `STUDENT` |
| `Instructor`, `P`, `Faculty` | `FACULTY` |
| `Staff` | `STAFF` |
| `PROSPECTIVE_STUDENT` | `PROSPECTIVE_STUDENT` |

These variants exist because the primary institution role value can arrive in more than one form depending on how the SIS source system and ILP are configured (full word, single-letter code, or a synonym). Confirm which variants your own feed actually sends — via the Field Mapping test tools or an integration log review — rather than assuming this list is exhaustive for your institution.

---

## 4) A Note on the Two Reference Implementations

`LIS_user_add_node.js` includes two versions of this script: an if/else chain and an equivalent role-map lookup. They are not perfectly equivalent for an **unmapped** role value (one that isn't blank, but also isn't in the table above):

- The if/else version falls through to its final `else` branch, logs "No NODE map for Primary Institution Role," and returns an **empty array** (`[]`) — because `parentNodeList` was initialized empty and never populated.
- The role-map version's `nodeList[0]` is `undefined` in that case, so it logs the same message but returns **`null`**.

An empty array and `null` are not necessarily treated the same way by the Added Node field — this hasn't been confirmed against a live instance. If you adapt one of these scripts, pick one implementation and confirm what your Learn instance actually does with an unmapped role before relying on it in production.

---

## 5) Recommended Overall Strategy

- **Confirm your node external keys** match exactly what this script returns (`STUDENT`, `FACULTY`, `STAFF`, `PROSPECTIVE_STUDENT` are illustrative, not fixed Blackboard constants).
- **Decide what should happen for an unmapped role** (see above) and make both implementations agree, rather than relying on whichever behavior happens to fall out of the script's structure.
- **Log both the raw role value and the resolved node** (as both reference implementations do) — this is what makes an unmapped-role or missing-role case diagnosable from the integration logs alone.
