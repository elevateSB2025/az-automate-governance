package identity.roles

privileged_roles := {
  "global administrator",
  "privileged role administrator",
  "security administrator",
  "exchange administrator",
  "sharepoint administrator"
}

deny[msg] {
  some i
  assignment := input.roleAssignments[i]

  # Bind role BEFORE using it
  role := lower(assignment.roleName)
  role == privileged_roles[_]

  lower(assignment.principalType) != "group"

  msg := sprintf(
    "Privileged role '%s' must be assigned to a group, not %s '%s'.",
    [assignment.roleName, assignment.principalType, assignment.principal]
  )
}
