"""
  Login to account using user credentials and fetch the request-token from URL using selenium.
  - Reads USER & APP credentials from PRIVATE.KEY
  - Generates TOTP.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyotp
import os
import time

path = os.path.dirname(os.path.abspath(__file__))
cwd = os.chdir(path)

# Path to chromedriver (replace with your path if not in PATH)
DRIVER_PATH = '../../../chromedriver_linux64/chromedriver'


def fetch_web_access_token(_url, _client_id, _client_pass, _totp_key):

    #Set credentials
    creden = [ _client_id, _client_pass, _totp_key ]

    #Get stocks details
    request_token = open_url_fetch_access_token(creden, _url)

    return request_token

    
def open_url_fetch_access_token(creden, url):

    # Generate access token from web url
    # 1. Login
    # 2. Go to your app's redirect URL to get request_token

    # Set up Chrome options (optional: headless mode)
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment to run without GUI
    
    # Initialize the WebDriver
    service = Service(DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Open login page
        driver.get(url)
    

        # Wait for Page #1 to load: Login
        user_id_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "login_id"))
        )
        user_id_field.send_keys(creden[0]) # enter user id

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(creden[1]) # enter password

        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click() # click login


        # Wait for Page #2 to load: App Code
        WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.NAME, "answers[]"))
            )
        app_code_field = driver.find_element(By.NAME, "answers[]")
        totp = pyotp.TOTP(creden[2])
        totp_code = totp.now()
        print(f"{totp_code}:{creden[2]}")
        app_code_field .send_keys(totp_code) # enter app code

        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click() # click login

        # Wait for Page #3 to load: request token
        WebDriverWait(driver, 300).until(
            lambda x: "https://127.0.0.1" in driver.current_url
            )


        # Get the final URL and extract request-token from url
        final_url = driver.current_url

        print(f"access-url: {final_url}")

        request_token = ""
        url_parts = final_url.split("code=")
        token_parts = url_parts[1].split("&")
        print(f"request-token: {token_parts[0]}")
        request_token = token_parts[0]

        return request_token

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Keep browser open for a few seconds, then close
        time.sleep(1)  # Adjust as needed to verify login
        driver.quit()

def main():
    url = "xxx"

    fetch_web_access_token(url)


if __name__ == "__main__":
    # Run the main function
    main()