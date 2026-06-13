# SonarQube Integration

Use this file when the project uses SonarQube or SonarCloud for quality analysis.

## Allowed read operations

```text
- read quality gate status
- read vulnerabilities
- read code smells
- read coverage
- read duplicated code metrics
```

## Write operations requiring approval

```text
- marking issues as false positive
- changing quality profiles
- changing quality gates
```

## Forbidden by default

```text
- modifying global quality gates
- changing project permissions
- hiding findings without justification
```

## Agent usage

Use SonarQube results to guide:

```text
- refactoring
- security fixes
- quality gate remediation
- technical debt tracking
```
