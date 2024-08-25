# Urls Monitor

Urls Monitor is a Home Assistant integration designed to monitor URLs for content updates, providing detailed feedback on the status and changes of the specified URLs.

## Installation

To install the Urls Monitor integration, follow these steps:

1. Ensure HACS (Home Assistant Community Store) is installed and running on your Home Assistant instance.
2. Add this repository to HACS by going to **HACS > Integrations > Custom repositories**.
3. Click on **Explore & Download Repositories** and search for **Urls Monitor**.
4. Download and install the integration.

## Configuration

To configure the Urls Monitor integration:

1. Navigate to **Configuration > Integrations** and click on **Add Integration**.
2. Search for **Urls Monitor**.
3. Fill in the following required fields:
   - **URL**: The URL to monitor.
   - **Headers**: Request headers in the format `key:value`, separated by `|`.
   - **Interval**: Time in seconds between the requests.
   - **Timeout**: Request timeout duration in seconds.
4. Save the configuration.

## Usage

Once configured, the integration will create a sensor for each URL you have set up, providing the following attributes:

- **state**: Hash of the content if the request is successful, otherwise a hash of the error message.
- **error**: Error message if an error occurs.
- **extract**: Truncated content or error message.
- **status_code**: HTTP status code of the response.
- **content_length**: Length of the content.

## Features

- Easy installation and configuration through Home Assistant.
- Monitors multiple URLs simultaneously.
- Provides detailed sensor attributes for monitored URLs.
- Customizable request headers, interval and timeout settings.

## Contributing and reports

Contributions are welcome! If you'd like to contribute, please look at <https://baltig.o.pfzone.net/pfzone/home-assistant/urls-monitor/-/issues>

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
