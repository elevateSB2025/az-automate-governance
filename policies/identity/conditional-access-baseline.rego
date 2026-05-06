package identity.conditional_access

deny[msg] {
  not admin_mfa_baseline_present
  msg := "Baseline conditional access policy for admin MFA is missing."
}

admin_mfa_baseline_present {
  some i
  baseline := input.conditionalAccess.baselines[i]
  lower(baseline.name) == "admin mfa requirement"
}
