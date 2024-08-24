# Urls Monitor

Urls Monitor is a Home Assistant integration that monitors URLs for content updates.

## Installation

1. Ensure HACS is installed and running on your Home Assistant instance.
2. Add this repository to HACS > Integrations > Custom repositories.
3. Click on "Explore & Download Repositories" and search for "Urls Monitor".
4. Download and install the integration.

## Configuration

1. Go to Configuration > Integrations > Add Integration.
2. Search for "Urls Monitor".
3. Fill in the required fields:
    - **URL**: The URL to monitor.
    - **Headers**: Request headers (key:value format, separated by `|`).
    - **Interval**: Time in seconds between requests.
    - **Timeout**: Request timeout in seconds.
4. Save the configuration.

## Usage

The integration will create a sensor for each configured URL:

- **state**: Hash of the content if successful, otherwise hash of the error message.
- **error**: Error message if there is any error.
- **extract**: Truncated content or error message.
- **status_code**: HTTP status code of the response.
- **content_length**: Length of the content.

## License

This project is licensed under the MIT License.
