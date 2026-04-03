---
feature: ""
status: ""
author: Joseph Flinn

---

# Feature Specification: [Feature Name]
## 1. High-Level Objective
**Goal:** [One sentence describing the value]
**Logic:** [Briefly explain the "Why" and the "How" at a high level]


## 2. System Context
**Target Files:**
- `path/to/relevant_file.ext`: [Role of this file]
- `path/to/another_file.ext`: [Role of this file]

**Dependencies:** [e.g., "Requires Stripe API", "Uses Tailwind CSS"]

**Existing Patterns:** [e.g., "Follow the repository pattern used in the Product module"]


## 3. Requirements & Implementation Tasks
_Please implement the following in order:_

### Phase 1: Data & Schema
- [ ] Task: [e.g., Add is_active boolean to Organization model]
- [ ] Constraint: [e.g., Default value must be true]

### Phase 2: Business Logic
- [ ] Task: [e.g., Create a service method to toggle status]
- [ ] Logic: [e.g., If status is toggled to false, revoke all active sessions]

### Phase 3: Interface / API
- [ ] Endpoint: POST /api/v1/feature-route
- [ ] Payload:
  ```JSON
  { "id": "uuid", "action": "string" }
  ```


## 4. Technical Constraints & Guardrails
**Security:** [e.g., "Ensure only users with admin role can access this."]

**Performance:** [e.g., "Query must be optimized to avoid N+1 issues."]

**Code Style:** [e.g., "Use functional components; no class-based components."]

**Error Handling:** [e.g., "Throw a CustomDomainException if the ID is not found."]


## 5. Definition of Done (Testing)
_The agent must verify the following before completion:_

**Unit Test:** [Test Name] should verify [Condition].

**Integration Test:** Ensure [Feature] works with [Existing System].

**Manual Verification:** [e.g., "The 'Save' button should remain disabled until the form is valid."]


## 6. Reference Material
[Optional: Paste snippets of existing code, API docs, or specific library syntax you want the agent to use.]
