# GitHub Integration

Use this file when the project uses GitHub for repository hosting, issues, pull requests or actions.

## Recommended access

Preferred access path:

```text
gh CLI through approved wrapper scripts
```

## Allowed read operations

```text
- read issues
- read pull requests
- read branches
- read GitHub Actions status
- read repository metadata
```

## Write operations requiring approval

```text
- create issue comments
- create pull request comments
- create branches
- create pull requests
- trigger workflows
- change labels or assignees
```

## Forbidden by default

```text
- deleting issues
- deleting branches
- force-pushing
- changing repository settings
- modifying secrets or variables
- reading or printing secrets
```

## Required wrapper scripts

Prefer wrappers under:

```text
.agent/scripts/github-*.sh
```

Do not invent ad-hoc `gh` commands for write operations when a wrapper exists.
