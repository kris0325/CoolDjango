import requests
from datetime import datetime


def numDevices(statusQuery, threshold, dateStr):
    # Parse the date string
    search_date = datetime.strptime(dateStr, "%m-%Y")

    # Initialize variables
    matching_devices = 0
    current_page = 1
    base_url = "https://jsonmock.hackerrank.com/api/iot_devices/search"

    while True:
        # Make API request
        response = requests.get(f"{base_url}?status={statusQuery}&page={current_page}")

        # Check if the response is successful
        if response.status_code != 200:
            break

        data = response.json()

        # Process devices on current page
        for device in data["data"]:
            # Convert timestamp to datetime
            device_date = datetime.fromtimestamp(
                device["timestamp"] / 1000
            )  # Convert milliseconds to seconds

            # Check if device matches criteria
            if (
                device_date.month == search_date.month
                and device_date.year == search_date.year
                and device["operatingParams"]["rootThreshold"] > threshold
            ):
                matching_devices += 1

        # Check if we need to fetch more pages
        if current_page >= data["total_pages"]:
            break

        current_page += 1

    return matching_devices
