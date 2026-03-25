# ANRS RFCs (Requests for Comments)

This directory contains design documents for significant changes to the ANRS specification.

## What is an RFC?

An RFC (Request for Comments) is a proposal for a significant change to ANRS. RFCs provide a consistent and controlled path for changes to enter the specification, allowing all stakeholders to be confident about the direction ANRS is evolving in.

## When is an RFC required?

An RFC is required for:

- **Spec changes**: Any modification to `ENTRY.md`, `state.schema.json`, or core contracts
- **Breaking changes**: Changes that affect backward compatibility
- **New concepts**: Adding new core concepts (skills, states, etc.)
- **Protocol changes**: Modifications to the execution loop or harness protocol

An RFC is NOT required for:

- Bug fixes in CLI or documentation
- Minor clarifications in existing docs
- Adding new adapters (unless they require spec changes)
- Typo fixes or formatting changes

## RFC Process

### 1. Proposal

Create a new file: `rfcs/NNNN-short-name.md` (NNNN = next number)

Copy the template from `rfcs/0000-template.md` and fill in all sections.

### 2. Discussion

- Open a Pull Request with your RFC
- RFC will be labeled `rfc: proposed`
- Community discussion period: minimum 7 days
- Address feedback and iterate on the design

### 3. Decision

After discussion:
- **Accepted**: RFC moves to `accepted/` subdirectory, implementation begins
- **Rejected**: RFC is closed with explanation, file remains for historical reference
- **Deferred**: RFC is valid but timing isn't right

### 4. Implementation

- Reference the RFC in implementation PRs
- Update RFC with any deviations during implementation
- RFC moves to `implemented/` when complete

## RFC Numbering

- `0001-0099`: Core specification
- `0100-0199`: Execution protocol
- `0200-0299`: Harness and quality gates
- `0300-0399`: Skills and adapters
- `0400-0499`: CLI and tooling
- `0500+`: Reserved for future categories

## Current RFCs

| Number | Title | Status |
|--------|-------|--------|
| - | - | (No RFCs yet) |

## Template

See [0000-template.md](0000-template.md) for the RFC template.
