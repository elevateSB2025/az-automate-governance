package identity.roles

deny[msg] {
  some i
  assignment := input.roleAssignments[i]
  lower(assignment.roleName) == "global administrator"
  lower(assignment.principalType) == "user"

  msg := sprintf(
    "Direct Global Administrator assignment to user '%s' is not allowed. Use a group instead.",
    [assignment.principal]
  )
}
