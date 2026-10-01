# Interview State Schema

The interview maintains a structured belief state internally.

This is a conceptual schema for the LLM-driven engine. Implementations may persist it as JSON when interview telemetry is enabled.

```json
{
  "interviewVersion": "2",
  "subject": {
    "mode": "target-product-bootstrap|existing-harness-reinitialization|toolkit-self-development",
    "targetRoot": ".",
    "name": null,
    "status": "unknown|inferred|confirmed",
    "confidence": 0.0,
    "excludedFromProductInference": [
      "AGENTS.md",
      ".agent/**",
      ".opencode/**",
      "opencode.jsonc",
      "template/**"
    ],
    "evidenceIds": []
  },
  "evidence": [
    {
      "id": "evidence-1",
      "source": "user|repository|organization-policy|default|inference",
      "reference": "README.md or answer summary",
      "trust": "authoritative|strong|tentative",
      "facts": ["project.intent=existing-system"]
    }
  ],
  "dimensions": {
    "project.intent": {
      "status": "unknown|inferred|confirmed|not-applicable",
      "hypotheses": [
        { "value": "new-build", "probability": 0.4 },
        { "value": "extension", "probability": 0.3 },
        { "value": "migration", "probability": 0.2 },
        { "value": "refactoring", "probability": 0.1 }
      ],
      "confidence": 0.0,
      "impactWeight": 1.0,
      "riskWeight": 1.0,
      "evidenceIds": []
    }
  },
  "topics": {
    "active": [],
    "possible": [],
    "pruned": [],
    "completed": []
  },
  "candidateQuestions": [
    {
      "id": "topic.question-id",
      "topic": "topic-id",
      "resolves": ["dimension.id"],
      "estimatedInformationGain": 0.0,
      "interactionCost": 1.0,
      "questionValue": 0.0,
      "blockingSafetyUnknown": false
    }
  ],
  "entropy": {
    "weightedBeforeLastAnswer": null,
    "weightedCurrent": null,
    "bestRemainingQuestionValue": null
  },
  "coverage": {
    "discoverySubject": "missing|partial|sufficient",
    "projectIntent": "missing|partial|sufficient",
    "runtimeContext": "missing|partial|sufficient",
    "agentResponsibilities": "missing|partial|sufficient",
    "autonomyBoundary": "missing|partial|sufficient",
    "qualityExpectations": "missing|partial|sufficient",
    "integrationAccess": "missing|partial|sufficient",
    "riskProfile": "missing|partial|sufficient"
  },
  "criticalUnknowns": [],
  "assumptions": [],
  "safeDefaults": [],
  "selectedQuestion": null,
  "interviewTrace": [],
  "readyForSummary": false,
  "readyForGeneration": false
}
```

## Probability rules

For every unresolved dimension:

```text
probabilities must be between 0 and 1
probabilities should sum to 1
confirmed dimensions should have one value at probability 1
not-applicable dimensions contribute zero entropy
confidence describes evidence quality, not answer probability
```

Do not invent fine-grained precision. Coarse estimates such as `0.6 / 0.3 / 0.1` are sufficient for candidate comparison.

## Evidence precedence

Use this default precedence when sources conflict:

```text
explicit current user answer
organization or project policy
current repository evidence
existing documentation
inference
safe default
```

Do not automatically override a higher-precedence source. Ask one clarification question when the conflict changes generated behavior or safety.

Evidence classification is evaluated before precedence. A highly detailed harness file is still control evidence and cannot outrank product evidence for product-purpose or product-architecture dimensions.

## Readiness rule

`readyForSummary` becomes true when:

```text
criticalUnknowns is empty
discoverySubject coverage is sufficient
required coverage is sufficient
remaining assumptions have safe defaults
bestRemainingQuestionValue is below the configured stop threshold
```

`readyForGeneration` becomes true only after the user approves the final summary.
