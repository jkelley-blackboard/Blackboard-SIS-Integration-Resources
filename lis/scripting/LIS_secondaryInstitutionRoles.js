(function() {
  // Field: secondaryInstRoles
  // Maps secondary institution role values from the LIS person record to valid
  // Blackboard institution role IDs. A person may carry one or more secondary
  // roles alongside their primary role — all are mapped and returned as an array.
  //
  // Secondary roles are <institutionRole> elements in the <roles> block that
  // omit <primaryroletype> (or set it to false). Blackboard reads these natively
  // and reports them as invalid if the role ID does not exist in the system —
  // this script performs the mapping before that check runs.
  //
  // NOTE: getSecondaryInstitutionRoles() (plural) is not yet confirmed against
  // a live instance's JavaDocs. If it fails, try getSecondaryInstitutionRole()
  // (singular), which may return only the first secondary role.
  // JavaDocs are available at: /webapps/dataIntegration/docs/ on any Learn deployment.

  var sField = 'Secondary Institution Role: ';

  var roleMap = {
    'Learner':    'LSCO_Student',
    'Instructor': 'LSCO_Faculty',
    'LSCO_Staff': 'LSCO_Staff'
  };

  var secondaryRoles = data.getPerson().getRoles().get(0).getSecondaryInstitutionRoles();

  // Secondary roles are optional — not all person records will carry them.
  // Log at info level and skip only the attribute (not the whole record).
  if (!secondaryRoles || secondaryRoles.isEmpty()) {
    helper.logInfo(sField + 'No secondary roles found. Skipping attribute.');
    helper.skipAttribute();
    return;
  }

  var mapped = [];
  for (var i = 0; i < secondaryRoles.size(); i++) {
    var val = secondaryRoles.get(i).value;
    var mappedVal = roleMap[val] || val;
    helper.logInfo(sField + 'found ' + val + ', mapping to ' + mappedVal);
    mapped.push(mappedVal);
  }

  helper.logInfo(sField + 'returning: ' + mapped.join(', '));
  return mapped;
}());
