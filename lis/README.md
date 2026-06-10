# LIS (Learning Information Services)

Resources for Blackboard Learn LIS-based SIS integrations, including custom field mapping scripts, XML samples, and reference documentation.

> All content is the property of Blackboard Inc. and is provided for reference and educational purposes only, without support, maintenance, or warranty of any kind. Use at your own risk.

## Contents

| Path | Contents |
|---|---|
| [`scripts/`](scripts/) | Sample JavaScript field mapping scripts |
| [`xml-samples/`](xml-samples/) | Sample LIS XML files for testing and reference |
| [`guides/`](guides/) | Scripting guide and integration how-tos |
| [`data-models/`](data-models/) | Data model reference for accessing SIS data in scripts |

## Useful Links

- [Sample LIS formatted files](https://github.com/blackboard/bbdn-lis_samples)
- [Help page on SIS custom field mapping scripting](https://help.anthology.com/test-blackboard-administrator/en/integrations/student-information-system--sis-/snapshot-flat-file/snapshot-flat-file-custom-field-mapping.html)
- [RHINO 1.7.13 Info](https://p-bakker.github.io/rhino/releases/new_in_rhino_1.7.13.html)
- [RHINO Engine Compatibility](https://mozilla.github.io/rhino/compat/engines.html)

---

# Guidance for Authoring Custom SIS Field Mapping Scripts in Blackboard

Custom scripting for SIS field mapping in Blackboard is powerful, but that power comes with responsibility. These scripts often live a long time, outlast their authors, and become critical to data integrity.

---

## 1. Documentation: More Is Better Than Less

I am not always fastidious about documentation—but for SIS field mapping scripts, **more documentation is always better**.

### Use the Integration Comment Box
Use the integration's **comment box** as a front-door summary:

- What the script does
- Which fields are manipulated
- Why the script exists
- Who authored or last updated it
- When it was last modified
- Where additional documentation lives (repo, ticket, wiki)

### Comment Your Code Generously
Comment each major section of the script. Explain *why* logic exists, not just *what* it does.

---

## 2. Use Helper Functions for Logging

Leverage the provided helper functions to report success, failure, and transformation details to the SIS integration logs.
Learn more about helpers in [guides/custom_scripting_help.md](guides/custom_scripting_help.md).

Benefits:
- Clear visibility into script execution
- Faster troubleshooting
- Safer long-term maintenance

Avoid silent failures. Every script should clearly log when it runs and what it attempts to do.

---

## 3. Identify the Field Being Manipulated

Always define a readable logging prefix string identifying the field and purpose.

```javascript
var sField = 'Primary Node Batch Uid Script '; // Logging prefix
```

Use this string consistently in helper calls so log entries are easy to interpret.

---

## 4. Basic Error Handling

There is **no substitute for basic error handling**.

- Guard against null or missing values
- Expect unexpected SIS input
- Log errors with actionable detail

Fail safe, not silent. Clear logging beats hidden corruption.

---

## Final Thoughts

These scripts are infrastructure code. Optimize for clarity, observability, and maintainability over cleverness.

Well-documented, well-logged scripts save time and prevent data issues long after their original author has moved on.
