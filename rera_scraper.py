from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup
driver = webdriver.Chrome()
driver.get("https://rera.odisha.gov.in/projects/project-list")
wait = WebDriverWait(driver, 10)

# Wait for page to load
wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(text(),"View Details")]')))
time.sleep(2)

# Get first 6 "View Details" buttons
view_buttons = driver.find_elements(By.XPATH, '//a[contains(text(),"View Details")]')[:6]

for i, button in enumerate(view_buttons):
    # Refresh buttons due to page reload
    buttons = driver.find_elements(By.XPATH, '//a[contains(text(),"View Details")]')
    driver.execute_script("arguments[0].click();", buttons[i])
    print(f"\n--- Project {i+1} ---")

    # Wait for project detail content
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "details-project")))
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    # Extract Project Name and RERA Regd. No.
    blocks = driver.find_elements(By.CLASS_NAME, "details-project")
    for block in blocks:
        try:
            label = block.find_element(By.TAG_NAME, "label").text.strip()
            value = block.find_element(By.TAG_NAME, "strong").text.strip()
            if label in ["Project Name", "RERA Regd. No."]:
                print(f"{label}: {value}")
        except:
            continue

    # Click "Promoter Details" tab
    try:
        promoter_tab = driver.find_element(By.LINK_TEXT, "Promoter Details")
        driver.execute_script("arguments[0].click();", promoter_tab)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ms-3")))
        time.sleep(1)

        # Fetch Promoter Info
        promoter_blocks = driver.find_elements(By.CLASS_NAME, "ms-3")
        for block in promoter_blocks:
            try:
                label = block.find_element(By.TAG_NAME, "label").text.strip()
                value = block.find_element(By.TAG_NAME, "strong").text.strip()
                if label in ["Company Name", "Registered Office Address", "GST No."]:
                    print(f"{label}: {value}")
            except:
                continue
    except Exception as e:
        print("Promoter Details not found or error:", e)

    # Go back to project list
    driver.back()
    wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(text(),"View Details")]')))
    time.sleep(2)

driver.quit()
