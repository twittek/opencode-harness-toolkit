# GitLab Integration

Use this file when the project uses GitLab for repository hosting, issues, merge requests or CI/CD.

## Recommended access

Preferred access path:

```text
glab CLI through approved wrapper scripts
```

## Allowed read operations

```text
- read issues
- read merge requests
- read branches
- read CI pipeline status
- read repository metadata
```

## Write operations requiring approval

```text
- create issue comments
- create merge request comments
- create branches
- create merge requests
- trigger pipelines
- change labels or assignees
```

## Forbidden by default

```text
- deleting issues
- deleting branches
- force-pushing
- changing protected branch settings
- modifying CI/CD variables
- reading or printing secrets
```

## Required wrapper scripts

Prefer wrappers under:

```text
.agent/scripts/gitlab-*.sh
```

Do not invent ad-hoc `glab` commands for write operations when a wrapper exists.
