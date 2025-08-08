from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def fetch_bse_result(company_name):
    print(f"Searching for: {company_name}")

    options = Options()
    options.binary_location = "/usr/bin/google-chrome"  # Important for Render
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--disable-extensions")
    options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("detach", False)
    options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
    options.page_load_strategy = 'eager'

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://www.bseindia.com/corporates/Forth_Results.aspx")
        print("Page loaded.")

        search_box = wait.until(EC.visibility_of_element_located((By.ID, "scripsearchtxtbx")))
        search_box.clear()
        for ch in company_name:
            search_box.send_keys(ch)
            time.sleep(0.15)
        print("Search term entered.")

        try:
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".quotemenu")))
            search_box.send_keys(Keys.DOWN)
            search_box.send_keys(Keys.ENTER)
        except Exception as e:
            print("Dropdown issue:", e)
            return {"error": "Company dropdown not found or failed to select"}

        submit_button = wait.until(EC.element_to_be_clickable((By.ID, "btnSubmit")))
        submit_button.click()
        print("Submit clicked.")

        try:
            rows = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, "//tr[@ng-repeat='fr in forthresult']"))
            )
            print(f"Rows found: {len(rows)}")
        except Exception as e:
            print(f"No rows found: {e}")
            rows = []

        if rows:
            columns = rows[0].find_elements(By.CLASS_NAME, "tdcolumn")
            print(f"Columns: {[c.text for c in columns]}")
            return {
                "company": company_name,
                "security_code": columns[0].text.strip(),
                "security_name": columns[1].text.strip(),
                "result_date": columns[2].text.strip(),
                "debug": {
                    "columns": [c.text for c in columns]
                }
            }
        else:
            return {
                "error": "The Result is not Announced yet!"
            }

    except Exception as e:
        print(f"Exception: {e}")
        return {"error": f"Failed to fetch data: {str(e)}"}

    finally:
        try:
            driver.quit()
        except Exception as e:
            print("Error closing browser:", e)

        print("✅ Chrome closed properly")
