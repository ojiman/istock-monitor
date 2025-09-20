# Data Models

This document outlines the data structures used for configuration and state management in the Apple Stock Checker application.

## 1. Configuration (Environment Variables)

Configuration is managed via environment variables. In a GitHub Actions context, these should be set as repository secrets.

### `PRODUCT_MODELS`

-   **Type**: `String`
-   **Description**: A comma-separated string of the Apple product model numbers to be checked.
-   **Required**: Yes
-   **Example**: `"MG684J/A,MG6D4J/A"`

### `LOCATION`

-   **Type**: `String`
-   **Description**: The location code (e.g., a postal code) used to query for local store availability.
-   **Required**: Yes
-   **Example**: `"141-0032"`

### `SLACK_WEBHOOK_URL`

-   **Type**: `String` (URL)
-   **Description**: The full URL for the Slack incoming webhook, used to post notifications.
-   **Required**: Yes
-   **Example**: `"https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"`

---

## 2. State Data (`state.json`)

The application persists its last known stock status in a JSON file named `state.json` at the root of the repository. This file is read at the start of each run and updated at the end if the stock status has changed.

### Structure

The file contains a single JSON object where:
-   The **keys** are the product model strings.
-   The **values** are an array of strings, representing the names of the stores where the product was last seen in stock.

### Example `state.json`

```json
{
  "MG684J/A": [
    "渋谷",
    "新宿"
  ],
  "MG6D4J/A": []
}
```

In this example:
-   The model `MG684J/A` was available at "渋谷" and "新宿".
-   The model `MG6D4J/A` was not available at any store.
