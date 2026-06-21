# Security Compliance Checklist

Reusable targeted security and privacy review for session-level validation and
documentation checks.

## Scope Rules

- Review only files created or modified by the current session
- This is a targeted review of session deliverables, not a full codebase audit
- Flag clear violations only; do not speculate about edge cases without
  evidence
- If the session added no user-facing data handling, GDPR may be marked `N/A`
  with a brief justification
- Hardcoded secrets and injection vulnerabilities are always `FAIL` regardless
  of scope
- In monorepos, scope the review to the declared package boundary unless the
  session is explicitly cross-cutting

## Security Spot-Check Categories

- **Injection**: SQL, command, LDAP, or similar injection vectors from
  unsanitized input reaching queries or shell calls
- **Broken authentication or secret handling**: Hardcoded credentials, API
  keys, tokens, shared credentials, or missing authorization checks near
  protected resources
- **Sensitive data exposure**: Unencrypted PII in logs, errors, responses, or
  plaintext config
- **Insecure dependencies**: Newly added packages with known vulnerabilities
  from the session's dependency changes
- **Security misconfiguration**: Debug modes enabled, overly permissive CORS,
  missing security headers, unsafe defaults
- **Database security**: Hardcoded connection strings, raw SQL string
  concatenation instead of parameterization, missing rollback artifacts when
  conventions require them, unencrypted sensitive columns, or unlimited
  connection pools

## GDPR Review Categories

- **Data collection and purpose**: New personal data collection has a documented
  purpose and legal basis
- **Consent**: Data that requires consent is not stored before that consent
  exists
- **Data minimization**: Only the minimum necessary personal data is collected
- **Right to erasure**: A deletion path exists or is documented as an explicit
  future requirement
- **PII in logs**: Personal data does not leak into application logs
- **Third-party sharing**: Transfers to external services are documented and
  intentional

## Documentation Use

When documentation includes setup, secrets, environment variables, deployment,
or personal-data handling claims, use this checklist to avoid documenting
insecure defaults or unsupported compliance statements.
