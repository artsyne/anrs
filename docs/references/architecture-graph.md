---
name: architecture-graph
description: |
  High-density component dependency graph. Read when:
  (1) Understanding how AHES components connect
  (2) Tracing execution flow
  (3) Debugging component interactions
---

# Architecture Graph

High-density context for AI agents. Format: `Component -> Dependency [label]`

## Core Components

```
Orchestrator -> State [reads]
Orchestrator -> Skills [invokes]
Orchestrator -> Harness [validates]
Orchestrator -> Plans [follows]
```

## State Dependencies

```
State -> state.json [persists]
State -> state.schema.json [validates]
State -> scratchpad [temp_memory]
```

## Skills Dependencies

```
Skills -> index.json [registry]
Skills -> Rules [constraints]
Skills -> Contracts [schemas]
```

## Harness Dependencies

```
Harness -> L1_Static [evaluates]
Harness -> L2_Dynamic [evaluates]
Harness -> L3_Stability [evaluates]
Harness -> Reports [outputs]
```

## Execution Flow

```
Plan -> Skill -> Code -> Harness -> Commit
```

## Data Flow

```
User_Request -> State -> Plan -> Skill_Select
Skill_Select -> Skill_Execute -> Code_Change
Code_Change -> Harness_Eval -> Result
Result:PASS -> Atomic_Commit -> State_Update
Result:FAIL -> Reflection -> Scratchpad -> Retry
```
