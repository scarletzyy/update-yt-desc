from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import json

# Create the Chrome driver instance with the service and options
driver = webdriver.Chrome()

# The old text and new text for replacement
old_text = "This is old text"
new_text = "This is new text"

# Load YouTube
driver.get('https://www.youtube.com/')

# Load cookies from the JSON file
with open('/path/to/cookies.json', 'r') as cookies_file:  # Update the path to your cookie JSON file
    cookies = json.load(cookies_file)

# Add cookies to the browser, ensuring 'sameSite' is present
for cookie in cookies:
    # Check if 'sameSite' is not in cookie or invalid
    if 'sameSite' not in cookie or cookie['sameSite'] not in ["Strict", "Lax", "None"]:
        cookie['sameSite'] = "Lax"  # Defaulting to "Lax" if not present
    driver.add_cookie(cookie)

# Refresh the page to log in
driver.refresh()

def update_video_descriptions():
    driver.get('https://studio.youtube.com/channel/<YOUR_CHANNEL_ID>/videos/upload') # Update to your channel's ID

    # Wait for the video elements to be present
    WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.XPATH, '//a[@id="thumbnail-anchor"]'))
    )

    index = 0  # Index to track the video we are on

    # Loop through pages until there are no more
    while True:
        # Re-fetch the video elements on the current page
        video_elements = driver.find_elements(By.XPATH, '//a[@id="thumbnail-anchor"]')

        if index < len(video_elements):
            # Locate the corresponding video title
            video_title_element = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, f'(//*[@id="video-title"])[{index + 1}]'))
            )
            if video_title_element:
                video_title = video_title_element.text
            else:
                video_title = "Title not found"

            print(f"Processing video at index: {index}, Title: {video_title}")  # Print the current index and video title

            # Select the current video based on index
            video = video_elements[index]            
            WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable(video)
            ).click()

            # Wait for the description area to be clickable
            description_area = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Tell viewers about your video (type @ to mention a channel)"]'))
            )
            time.sleep(1)
            current_description = description_area.get_attribute('innerText')

            # Replace the old text with the new text if it exists
            if old_text in current_description:
                new_description = current_description.replace(old_text, new_text)
                description_area.clear()  # Clear the existing description
                description_area.send_keys(new_description)  # Add new description

                time.sleep(1)

                # Wait for the save button to be clickable and then click it
                save_button = WebDriverWait(driver, 60).until(
                    EC.element_to_be_clickable((By.XPATH, '//ytcp-button[@id="save"]'))
                )
                save_button.click()

                print(f"Changes saved for video at index {index}.\n")

                # Wait for the "Changes saved" toast notification
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, '//tp-yt-paper-toast[contains(@class, "paper-toast-open")]'))
                )
                time.sleep(2)

            else:
                print(f"No changes needed for video at index {index}. Skipping.\n")

            # Go back to video list
            driver.back()

            # Wait for the video list to be present again
            WebDriverWait(driver, 60).until(
                EC.presence_of_all_elements_located((By.XPATH, '//a[@id="thumbnail-anchor"]'))
            )

            # Increment index to move to the next video
            index += 1

        else:
            # If no more videos on the current page, check if there's still next page
            next_button = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '//ytcp-icon-button[@id="navigate-after"]'))
            )
            aria_disabled = next_button.get_attribute("aria-disabled")
            if aria_disabled != "true":
                next_button.click()
                time.sleep(5)
            else:
                print("No more pages to navigate.")
                break  # Exit the loop if no more pages

            # Wait for the next page to load
            WebDriverWait(driver, 60).until(
                  EC.presence_of_all_elements_located((By.XPATH, '//a[@id="thumbnail-anchor"]'))
            )

            # Reset index for the new page
            index = 0

# Run the function
update_video_descriptions()
driver.quit()
