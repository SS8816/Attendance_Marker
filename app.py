from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, InvalidSessionIdException
import time
import os
from datetime import datetime
import smtplib
from email.message import EmailMessage

# === CONFIGURATION ===
form_url = "https://docs.google.com/forms/d/e/1FAIpQLScGdySssTCv_-VrqLprYduK6v-T7htAuvnHeqes9p4HKJvV4g/viewform"
your_name = "Shubham Singh"
your_id = "2022UCP1949"

sender_email = "shubham882005singh@gmail.com"
sender_password = "qxzr fkvm tzpj zrwn"
recipient_email = "2022ucp1949@mnit.ac.in"

# === DRIVER SETUP ===
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

service = Service()  # Let Selenium find chromedriver on its own (Render installs it in container)
driver = webdriver.Chrome(service=service, options=options)

# === EMAIL SENDER FUNCTION ===
def send_email_notification(screenshot_path):
    msg = EmailMessage()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg['Subject'] = '✅ Attendance Marked Notification'
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg.set_content(f"Attendance was marked successfully on {timestamp}.\nScreenshot saved at:\n{screenshot_path}")

    with open(screenshot_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(screenshot_path)
        msg.add_attachment(file_data, maintype='image', subtype='png', filename=file_name)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print("📧 Email notification sent!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# === MAIN LOOP ===
print("🔁 Checking for form availability...")

try:
    while True:
        driver.get(form_url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "M7eMe"))
            )
            print("✅ Form is open! Trying to fill it...")

            time.sleep(2)  # Let the JS finish rendering

            driver.execute_script(f'''
                const inputs = document.querySelectorAll('input[type="text"]');
                if (inputs.length >= 2) {{
                    inputs[0].value = "{your_name}";
                    inputs[1].value = "{your_id}";
                    inputs[0].dispatchEvent(new Event('input', {{ bubbles: true }}));
                    inputs[1].dispatchEvent(new Event('input', {{ bubbles: true }}));
                }}
            ''')
            print("➡️  Name and ID filled.")

            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//span[text()="Submit"]/ancestor::div[@role="button"]'))
            )
            submit_button.click()
            print("✅ Attendance marked successfully!")

            # === Screenshot Saving ===
            script_dir = os.path.dirname(os.path.abspath(__file__))
            folder_path = os.path.join(script_dir, "mark_photo")
            os.makedirs(folder_path, exist_ok=True)

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = os.path.join(folder_path, f"attendance_{timestamp}.png")

            driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot saved at: {screenshot_path}")

            send_email_notification(screenshot_path)
            break

        except TimeoutException:
            print("❌ Form still closed or not fully loaded. Retrying in 5 seconds...")
            time.sleep(5)

except InvalidSessionIdException:
    print("❌ Chrome session was unexpectedly closed. Please rerun the script.")
finally:
    driver.quit()
