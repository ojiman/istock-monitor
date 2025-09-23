# Quickstart Guide

This guide provides instructions for setting up and running the Apple Stock Checker project locally for development and testing purposes.

## Prerequisites

-   Python 3.13 or later
-   `pip` for installing dependencies
-   Git

## 1. Clone the Repository

First, clone the project repository to your local machine:

```bash
git clone https://github.com/ojiman/istock-monitor.git
cd istock-monitor
```

## 2. Install Dependencies

Install the required Python libraries using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## 3. Create Configuration File

The script is configured via environment variables. For local development, it's easiest to create a `.env` file in the root of the project. The script is not configured to read this file automatically; you will need to source it yourself or set the variables in your shell.

Create a file named `.env` with the following content:

```
# .env file

# Comma-separated list of Apple product model numbers to check
export PRODUCT_MODELS="MG684J/A,MG6D4J/A"

# Location code (e.g., postal code) for checking local stores
export LOCATION="141-0032"

# Your Slack incoming webhook URL
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/SLACK/URL"

# The base URL for the Apple API
export API_BASE_URL="YOUR_API_BASE_URL"

# The User-Agent string for requests
export USER_AGENT="YOUR_USER_AGENT"

# (Optional) Set the logging level to DEBUG for verbose output
# export LOG_LEVEL="DEBUG"
```

**Note**: Remember to replace the placeholder values with your actual configuration. The `.env` file should be added to your global `.gitignore` or the repository's `.gitignore` to prevent committing secrets.

## 4. Run the Script

Before running the script, load the environment variables from your `.env` file:

```bash
source .env
```

Now, you can execute the main script as a module from the project root:

```bash
python -m src.main
```

The script will perform a stock check, and if there are any changes compared to the `state.json` file, it will print the changes and attempt to send a Slack notification.

## 5. Run Tests

To ensure all components are working as expected, run the test suite using `pytest`:

```bash
pytest
```

All tests should pass, confirming that the modules for state management, API checking, and notifications are functioning correctly.
