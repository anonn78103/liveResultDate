from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
import time
import shutil
from selenium import webdriver

options = webdriver.ChromeOptions()
options.binary_location = "/usr/bin/google-chrome-stable"  # FULL PATH here
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)


def fetch_bse_result(company_name):
    print(f"🔍 Searching for: {company_name}")

    # 🛠 Ensure ChromeDriver is installed
    chromedriver_autoinstaller.install()

    # Check if Chrome binary exists in common server location
    chrome_path = shutil.which("google-chrome") or shutil.which("chromium-browser") or shutil.which("chromium")

    if not chrome_path:
        raise RuntimeError("No chrome executable found on PATH")

    options = Options()
    options.binary_location = chrome_path
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://www.bseindia.com/corporates/Forth_Results.aspx")
        print("✅ Page loaded.")

        search_box = wait.until(EC.visibility_of_element_located((By.ID, "scripsearchtxtbx")))
        search_box.clear()
        for ch in company_name:
            search_box.send_keys(ch)
            time.sleep(0.15)

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".quotemenu")))
        search_box.send_keys(Keys.DOWN)
        search_box.send_keys(Keys.ENTER)

        submit_button = wait.until(EC.element_to_be_clickable((By.ID, "btnSubmit")))
        submit_button.click()
        print("🚀 Submit clicked.")

        rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tr[@ng-repeat='fr in forthresult']")))
        if rows:
            columns = rows[0].find_elements(By.CLASS_NAME, "tdcolumn")
            return {
                "company": company_name,
                "security_code": columns[0].text.strip(),
                "security_name": columns[1].text.strip(),
                "result_date": columns[2].text.strip()
            }
        else:
            return {"error": "The Result is not Announced yet!"}

    except Exception as e:
        print(f"❌ Exception: {e}")
        return {"error": f"Failed to fetch data: {str(e)}"}

    finally:
        try:
            driver.quit()
        except Exception as e:
            print("⚠️ Error closing browser:", e)

