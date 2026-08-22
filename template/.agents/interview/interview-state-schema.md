# Interview State Schema

The agent should maintain this state internally:

```json
{
  "scenarioCandidates": [
    { "id": "frontend-learning-project", "confidence": 0.0 }
  ],
  "knownFacts": {},
  "prunedTopics": [],
  "openQuestions": [],
  "nextBestQuestion": null,
  "hypothesis": null
}
```

Do not print this state unless the user asks.
