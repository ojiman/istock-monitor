# Tasks: Apple Product Stock Checker

**Input**: Design documents from `/specs/001-apple-slack-github/`

## Phase 3.1: Setup
- [X] T001 [P] Create the project directory structure: `src/`, `tests/`, and `.github/workflows/`.
- [X] T002 [P] Create `requirements.txt` and add `requests`, `slack-sdk`, and `pytest`.
- [X] T003 [P] Create an empty `state.json` file in the root directory to store the initial state.
- [X] T004 [P] Create empty Python files: `src/main.py`, `src/apple_stock_checker.py`, `src/slack_notifier.py`, `src/state_manager.py`.
- [X] T005 [P] Create empty Python test files: `tests/test_apple_stock_checker.py`, `tests/test_slack_notifier.py`, `tests/test_state_manager.py`.

## Phase 3.2: Core Implementation
- [X] T006 [P] In `src/state_manager.py`, implement `read_state()` to read and parse `state.json`, and `write_state(state)` to write a dictionary to `state.json`.
- [X] T007 [P] In `tests/test_state_manager.py`, write unit tests for `read_state` and `write_state`, using a temporary file.
- [X] T008 [P] In `src/apple_stock_checker.py`, implement a function `check_stock(models: list, location: str)` that takes product models and a location, calls the Apple API, and returns a dictionary representing the current stock state.
- [X] T009 [P] In `tests/test_apple_stock_checker.py`, write unit tests for `check_stock`, mocking the `requests.get` call and using the sample JSON response.
- [X] T010 [P] In `src/slack_notifier.py`, implement a function `send_notification(message: str)` that sends a formatted message to the Slack webhook URL read from environment variables.
- [X] T011 [P] In `tests/test_slack_notifier.py`, write unit tests for `send_notification`, mocking the `slack_sdk.WebhookClient`.

## Phase 3.3: Integration
- [ ] T012 In `src/main.py`, implement the main orchestration logic:
    1. Load configuration from environment variables.
    2. Call `state_manager.read_state()` to get the old state.
    3. Call `apple_stock_checker.check_stock()` to get the new state.
    4. Call `state_manager.write_state()` to save the new state immediately.
    5. Compare the old and new states to identify changes.
    6. If changes are found, format a message and call `slack_notifier.send_notification()`.

## Phase 3.4: Automation
- [ ] T013 In `.github/workflows/stock_check.yml`, create a GitHub Actions workflow that:
    1. Runs on a 5-minute schedule (`cron: '*/5 * * * *'`).
    2. Sets up Python 3.13.
    3. Installs dependencies from `requirements.txt`.
    4. Executes `python src/main.py`.
    5. Passes the `SLACK_WEBHOOK_URL`, `PRODUCT_MODELS`, and `LOCATION` as environment variables from GitHub Secrets.

## Phase 3.5: Documentation
- [X] T014 [P] Create `specs/001-apple-slack-github/research.md` and document the findings about the Apple API endpoint, request, and response format.
- [ ] T015 [P] Create `specs/001-apple-slack-github/data-model.md` to document the structure of the environment variables and the `state.json` file.
- [ ] T016 [P] Create `specs/001-apple-slack-github/quickstart.md` with instructions for local setup, configuration, and execution.

## Dependencies
- `T001`-`T005` (Setup) must be done before `T006`-`T011` (Core Implementation).
- `T006`-`T011` can be done in parallel.
- `T012` (Integration) depends on `T006`, `T008`, and `T010`.
- `T013` (Automation) depends on `T012`.
- `T014`-`T016` (Documentation) can be done anytime after the plan is approved.
mentation) can be done anytime after the plan is approved.
