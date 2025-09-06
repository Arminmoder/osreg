import winsound  # Only works on Windows
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import winsound
import time


# -----------------------------------------

username = "YOUR USERNAME"
password = "YOUR PASSWORD"
# -----------------------------------------


# Reload and alert when receiving alerts from the browser
def handle_alert_and_reload():
    try:
        alert = driver.switch_to.alert
        print("[DEBUG] Alert detected:", alert.text)
        alert.accept()  # accept alert
        winsound.Beep(2000, 10500) # alert sound
        return True  # true to break the while loop
    except NoAlertPresentException:
        return False
    

# To navigate in iframes
def iframe_handler(facinum):
    driver.switch_to.default_content()  # Return to main content
    print("[DEBUG] Switched to default content")    
    try:
        iframe = wait.until(EC.presence_of_element_located(
            (By.ID, f"Faci{facinum}")))
        driver.switch_to.frame(iframe)
        print(f"[DEBUG] Switched to iframe 'Faci{facinum}'")
    except TimeoutException:
        print(f"[ERROR] iframe 'Faci{facinum}' not found!")
        driver.quit()
        exit()
    try:
        driver.switch_to.frame("Master")
        print("[DEBUG] Switched to frame 'Master'")
    except TimeoutException:
        print("[ERROR] frame 'Master' not found!")
        driver.quit()
        exit()
    try:
        driver.switch_to.frame("Form_Body")
        print("[DEBUG] Switched to frame 'Form_Body'")
    except TimeoutException:
        print("[ERROR] frame 'Form_Body' not found!")
        driver.quit()
        exit()


# Initialize browser and WebDriverWait
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)


# Open main login page
driver.get("https://osreg.pnu.ac.ir/forms/authenticateuser/main.htm")
print("[DEBUG] Main page loaded")
print("[DEBUG] Current URL:", driver.current_url)
print("[DEBUG] Page title:", driver.title)
time.sleep(3)
# Enter iframe #1 to access login form
iframe_handler(1)
time.sleep(5)
# Enter student ID and password
try:
    element = wait.until(EC.presence_of_element_located((By.ID, "F80351")))
    element.clear()
    element.send_keys(username)
    print("[DEBUG] Student ID entered")
    element = wait.until(EC.presence_of_element_located((By.ID, "F80401")))
    element.clear()
    element.send_keys(password)  
    print("[DEBUG] Password entered") 
except TimeoutException:
    print("[ERROR] Element 'F80401' not found even after waiting 60s!")

time.sleep(30)   # Wait to ensure the page fully loads

try:
    btn = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.ID, "btnLog"))
    )
    btn.click()
    print("[DEBUG] Login button clicked")
except TimeoutException:
    print("[ERROR] The login button was not clicked!")

time.sleep(10)

# Enter iframe #2 for menu
iframe_handler(2)

# Click "Registration Operations"
try:
    td_register = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//td[nobr[text()='ثبت نام']]")
        )
    )
    td_register.click()
    print("[DEBUG] Clicked on 'Register'")
except Exception as e:
    print("[ERROR] We were unable to click 'Register':", e)

try:
    td_register = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//td[span[text()='عمليات ثبت نام']]")
        )
    )
    td_register.click()
    print("[DEBUG] Clicked on 'Registration Operations'")
except Exception as e:
    print("[ERROR] We were unable to click 'Registration Operations':", e)


# Loop to check information
last_data = None
for i in range(100):
    # Enter iframe #2 for menu
    iframe_handler(2) 
    try:
        td_register = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//td[nobr[text()='ثبت نام اصلي']]")
            )
        )
        td_register.click()
        if (i == 0):
            td_register.click()
        print("[DEBUG] Clicked on 'Main Registration'")
    except Exception as e:
        print("[ERROR] We were unable to click 'Main Registration':", e)
    # Check alert
    if handle_alert_and_reload():
        break  # Stop loop if alert detected
    time.sleep(40)

    # In each iteration of the loop, a new iframe is created on the site.
    iframe_handler(3 + i)

    # Check table content for changes
    table_element = driver.find_element(By.ID, "T02")
    current_data = table_element.get_attribute("outerHTML")
    if last_data is not None and current_data != last_data:
        print("🔔 Data changed!")
        for j in range(10):
            winsound.Beep(700, 1000)
            time.sleep(1)

    driver.switch_to.default_content()  # Return to main content
    print("[DEBUG] Switched to default content")
    # Back to menu
    try:
        last_data = current_data
        td_register = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//div[contains(@class,'tabbutt') and contains(@class,'r2')]")
            )
        )
        td_register.click()
        print("[DEBUG] Clicked on 'Close'")
    except Exception as e:
        print("[ERROR] We were unable to click 'Close':", e)
    time.sleep(10)




winsound.Beep(700, 10000)
driver.switch_to.default_content()
time.sleep(60)  
driver.quit()
