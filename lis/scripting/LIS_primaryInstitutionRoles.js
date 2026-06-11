(function() { 
// Blackboard SIS Mapping Script
// Correctly maps primary institution roles
 var sField = 'Primary Institution Role: ';  //login prefix
 
 var primaryRole = data.getPerson().getRoles().get(0).getPrimaryInstitutionRole(); 
 if ( primaryRole != null ) { 
   var instRole = primaryRole.value; 
   helper.logInfo("Primary Role found in XML = " +  instRole );
     
   if ( instRole == 'Student' ) {
             helper.logInfo(sField + "Mapping to STUDENT");
             return 'STUDENT'; 
      }
   else if ( instRole == 'Instructor' ) {
             helper.logInfo(sField + "Mapping to FACULTY");
             return 'FACULTY';
      }
   else if ( instRole == 'Staff' ) {
             helper.logInfo(sField + "Mapping to STAFF");
             return 'STAFF';
      } 
   else {
             helper.logInfo(sField + "No map value.");
             return instRole; 
   }
 }  
 else { 
   helper.logWarning(sField + "Role not found.  Skip Record");
   helper.skipRecord();
 }
}()); 
