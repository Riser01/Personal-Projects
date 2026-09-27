# InterviewForge — Context-Grounded AI Mock Technical Interview Simulator

> Multi-agent technical interview and system design simulator featuring realistic FAANG/Principal interviewer personas, anti-sycophantic pushback, and calibrated rubric grading.

## Concept Overview

Traditional AI mock interviewers suffer from sycophancy: they praise shallow, vague answers and fail to challenge edge cases. InterviewForge reverses this by embedding adversarial interviewer personas calibrated to actual Job Descriptions, pushing candidates on throughput, failover, concurrency, and distributed state.

## Multi-Agent Graph Topology

```mermaid
flowchart TD
    Candidate([Candidate Submission: Resume & JD]) --> ContextParser[Context Ingestion Node<br/>Extracts Key Competencies & Skill Blindspots]
    ContextParser --> PersonaSelector{Interviewer Persona Selector}
    
    PersonaSelector --> DrChen[Dr. Chen: Staff ML Systems<br/>Latency Budgets, Quantization & Serving]
    PersonaSelector --> Marcus[Marcus Brody: Principal Architect<br/>CRDTs, Raft Consensus & Sharding]
    PersonaSelector --> Tariq[Tariq Vance: Lead FDE<br/>Dirty Data, Air-Gapped MVPs & Palantir-style Execution]
    
    DrChen --> ChallengeLoop[Multi-Turn Pushback Loop<br/>Probes Scale Limits & Single Points of Failure]
    Marcus --> ChallengeLoop
    Tariq --> ChallengeLoop
    
    ChallengeLoop --> RubricEvaluator[Rubric Evaluator Node<br/>Grades Architecture, Rigor & Trade-offs]
    RubricEvaluator --> Scorecard([Diagnostic Scorecard & Interview Debrief])
```

## Core Differentiators

1. **Anti-Sycophantic Prompt Engineering**: Explicitly prohibits empty flattery. If an architecture fails at 100k QPS, the agent demands a failure mitigation strategy.
2. **Context-Grounded Rubric**: Calibrates evaluation directly against the candidate's target company (e.g. Meta E6 vs. Early-Stage Staff).
3. **State Machine Transitions**: Tracks question difficulty adaptation (escalating to harder trade-offs when candidate performs well; offering targeted hints when stuck).
