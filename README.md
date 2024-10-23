# Updating YouTube video Descriptions Automatically with Selenium

A Python script for automating the process of updating YouTube video descriptions using Selenium WebDriver.
This script enables you to automatically modify the descriptions of multiple YouTube videos based on a predefined template.

## Login Method

Due to restrictions imposed by Google on automated browser windows for signing in, this script utilizes browser cookies stored as JSON for authentication. Ensure you export your browser cookies and save them in a JSON file for the script to use.

## Requirements

- Python 3.x
- Selenium library
- Chrome WebDriver (or appropriate WebDriver for your browser).

Ensure that your WebDriver matches the version of your browser.

## Installation

You can use this script by simply downloading the file: [update-yt-desc.py](https://github.com/scarletzyy/update-yt-desc/blob/main/update-yt-desc.py)

## Usage

1. Ensure that you have the required packages installed:
```bash
pip install selenium
```
2. Modify the script as needed to set your YouTube login credentials and the description template.
Run the script:
```bash
python update-yt-desc.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
