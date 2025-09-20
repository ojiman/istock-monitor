# Implementation Plan: Apple Product Stock Checker

**Branch**: `001-apple-slack-github` | **Date**: 2025-09-21 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-apple-slack-github/spec.md`

## Summary
This plan outlines the development of a Python script to monitor Apple's in-store product availability. The script will be executed periodically by a GitHub Actions workflow. It will compare the current stock status against a previously stored state (in a JSON file) and send a notification to Slack only when a change is detected. The entire solution will be designed to operate within the free tiers of the services used.

## Technical Context
**Language/Version**: Python 3.13.7
**Primary Dependencies**: `requests` (for API calls), `slack-sdk` (for Slack notifications), `pytest` (for testing).
**Storage**: A single JSON file (`state.json`) to persist the last known stock status.
**Testing**: `pytest` will be used for unit and integration tests.
**Target Platform**: GitHub Actions (using a standard Ubuntu runner).
**Project Type**: Single project (a self-contained Python script and supporting files).
**Performance Goals**: Each execution should complete within 1 minute to ensure efficient use of GitHub Actions runners.
**Constraints**: Must adhere to the free tier of GitHub Actions. All secrets (like the Slack webhook URL) must be managed via GitHub Secrets.
**Scale/Scope**: The script will be designed to monitor a configurable list of approximately 1-10 products across 1-5 stores.

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Reliability**: PASS. The plan includes retries for network requests and notifications for persistent failures.
- **Efficiency**: PASS. The script only sends notifications on state changes, and using a simple JSON file for state is resource-light.
- **Clarity**: PASS. The core function is to produce a clear, understandable Slack message.
- **Maintainability**: PASS. Products and stores are configurable via environment variables, and the code will be structured in modules for easy updates.
- **Simplicity**: PASS. The design uses a minimal set of tools (Python script, JSON file, GitHub Actions) and avoids database or complex infrastructure.

## Project Structure

### Documentation (this feature)
```
specs/001-apple-slack-github/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/tasks command)
```

### Source Code (repository root)
```
# Option 1: Single project (DEFAULT)
src/
├── apple_stock_checker.py # Logic to call Apple's API
├── slack_notifier.py      # Logic to send Slack messages
├── state_manager.py       # Logic to read/write state.json
└── main.py                # Main script orchestrating the checks

tests/
├── test_apple_stock_checker.py
├── test_slack_notifier.py
└── test_state_manager.py

.github/
└── workflows/
    └── stock_check.yml    # GitHub Actions workflow

requirements.txt           # Python dependencies
state.json                 # Stores last known stock status
```

**Structure Decision**: Option 1: Single project. The provided script will be refactored into this modular structure to enhance maintainability and testability.

## Phase 0: Outline & Research
**This phase is complete.** The user provided research findings demonstrating a viable method for checking stock.

**Key Findings**:
- **API Endpoint**: A request to `https://www.apple.com/jp/shop/pickup-message-recommendations` with query parameters for location and product model can retrieve stock data.
- **Request Headers**: A `User-Agent` header is required to mimic a standard browser.
- **JSON Response**: The stock availability is located within the JSON response at `body.PickupMessage.stores[].partsAvailability.{part_number}.pickupDisplay`.
- **Core Logic**: The provided script contains the fundamental logic for making the request, parsing the response, and identifying available stores.

**Output**: `research.md` will be created to formally document these findings.

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Define Data Models** in `data-model.md`:
   - **Config**: Document the structure of environment variables for configuration (`PRODUCT_MODELS`, `LOCATION`, `SLACK_WEBHOOK_URL`). `PRODUCT_MODELS` will be a comma-separated string of model numbers.
   - **State**: Define the JSON structure for `state.json`, which will map a product model to a list of available store names.

2. **Define Contracts**:
   - The function signatures for each module will serve as internal contracts. For example, `apple_stock_checker.check_stock(models: list)` will return a dictionary representing the current stock state.

3. **Create Quickstart Guide** in `quickstart.md`:
   - Detail the steps to set up the project locally:
     1. Clone the repository.
     2. Create and populate a `.env` file with `PRODUCT_MODELS`, `LOCATION`, and `SLACK_WEBHOOK_URL`.
     3. Install dependencies from `requirements.txt`.
     4. Run the main script: `python src/main.py`.
     5. Run tests: `pytest`.

**Output**: `data-model.md`, `quickstart.md`.

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do.*

**Task Generation Strategy**:
- The tasks will focus on refactoring the user-provided script into the modular structure defined above.
- Create tasks for each component: `state_manager`, `apple_stock_checker`, `slack_notifier`, and the orchestrating `main.py`.
- Create tasks for writing unit tests for each component, using mocking where appropriate (e.g., for `requests` and `slack-sdk`).
- Create a final task to implement the GitHub Actions workflow (`stock_check.yml`).

**Ordering Strategy**:
1.  Setup tasks (project structure, `requirements.txt`).
2.  Implement `state_manager.py` and its tests.
3.  Refactor the API call logic into `apple_stock_checker.py` and write tests.
4.  Implement `slack_notifier.py` and its tests.
5.  Implement `main.py` to integrate all modules.
6.  Implement the GitHub Actions workflow.

## Phase 3+: Future Implementation
*These phases are beyond the scope of this /plan command.*

**Phase 3**: Task execution (/tasks command will generate `tasks.md`).
**Phase 4**: Implementation (developers execute the tasks).
**Phase 5**: Validation (manual run, observing GitHub Actions, and checking Slack).

## Progress Tracking
*This checklist is updated during execution flow.*

**Phase Status**:
- [X] Phase 0: Research complete (/plan command)
- [X] Phase 1: Design complete (/plan command)
- [X] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [X] Initial Constitution Check: PASS
- [ ] Post-Design Constitution Check: PENDING
- [X] All NEEDS CLARIFICATION resolved
- [ ] Complexity deviations documented: None

---
*Based on Constitution v1.0.0 - See `.specify/memory/constitution.md`*
