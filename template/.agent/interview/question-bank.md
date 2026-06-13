# Question Bank

Questions should be selected by expected information gain, not by fixed order.

## High-value early questions

```text
Soll das Ergebnis produktiv betrieben werden?
```

```text
Does the application have a backend?
```

```text
Gibt es echte Nutzer, Rollen oder Berechtigungen?
```

```text
Are there external systems or integrations?
```

```text
Ist es ein Neubau, eine Erweiterung, eine Migration oder ein Refactoring?
```

```text
Soll der Agent Code ändern oder primär planen/dokumentieren?
```

## Lower-value detail questions

Ask later only if the branch is active:

```text
Welche konkrete Testlibrary nutzt ihr?
```

```text
Welche konkrete Datenbank?
```

```text
Welcher konkrete MCP-Server?
```

```text
Welcher konkrete GitLab-Befehl?
```


## Integration discovery questions

High-value early question:

```text
Are there external systems or tools the agents should know about?
```

Repository and review branch:

```text
Which repository and code review system do you use?
```

Work tracking branch:

```text
Which work tracking system do you use?
```

Documentation branch:

```text
Which documentation or knowledge system do you use?
```

Design branch:

```text
Which design or UX system do you use?
```

Quality branch:

```text
Which quality, security or monitoring tools are relevant?
```

Avoid asking for CLI commands before the system itself is known.
