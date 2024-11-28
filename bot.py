from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
import time
import csv
from webdriver_manager.firefox import GeckoDriverManager
import os
from PIL import Image, ImageDraw

# إعداد البيانات الوهمية
fake = Faker()

# إعداد المتصفح في وضع headless
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)

# استرجاع الرقم التالي للحساب
def get_next_account_number():
    try:
        with open("last_account_number.txt", "r") as file:
            return int(file.read().strip()) + 1
    except FileNotFoundError:
        return 1

# حفظ الرقم الأخير
def save_account_number(account_number):
    with open("last_account_number.txt", "w") as file:
        file.write(str(account_number))

# إعداد مجلد لحفظ لقطات الشاشة
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

# عداد الصور
screenshot_counter = 1

# حفظ لقطات الشاشة
def save_screenshot(step_name):
    global screenshot_counter
    screenshot_path = f"screenshots/{screenshot_counter:04d}_{step_name}.png"
    driver.save_screenshot(screenshot_path)
    screenshot_counter += 1
    print(f"تم حفظ لقطة الشاشة: {screenshot_path}")

# حفظ لقطة شاشة عند الضغط على المكان المحدد
def save_click_location_screenshot(element, step_name):
    global screenshot_counter
    location = element.location
    size = element.size
    x = int(location["x"] + size["width"] / 2)
    y = int(location["y"] + size["height"] / 2)

    # التقاط لقطة الشاشة
    screenshot_path = f"screenshots/{screenshot_counter:04d}_{step_name}.png"
    driver.save_screenshot(screenshot_path)

    # فتح الصورة ورسم دائرة على مكان الضغط
    image = Image.open(screenshot_path)
    draw = ImageDraw.Draw(image)
    radius = 10
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline="red", width=3)
    image.save(screenshot_path)
    screenshot_counter += 1
    print(f"تم حفظ لقطة الشاشة مع تحديد الضغط: {screenshot_path}")

# إنشاء حساب
def create_account():
    try:
        # استرجاع الرقم التالي وإنشاء الاسم والإيميل
        account_number = get_next_account_number()
        username = f"elitbotnew{account_number}"
        email = f"elitbotnew{account_number}@dsf.com"
        password = "Moammedmax34"
        birthdate = "1990-01-01"

        # فتح صفحة التسجيل
        driver.get("https://ar.secure.imvu.com/welcome/ftux/account/")
        time.sleep(5)
        save_screenshot("page_loaded")

        # تعبئة الحقول
        username_field = driver.find_element(By.CLASS_NAME, "signup_displayname_input")
        username_field.send_keys(username)
        save_click_location_screenshot(username_field, "username_filled")

        email_field = driver.find_element(By.NAME, "signup_email")
        email_field.send_keys(email)
        save_click_location_screenshot(email_field, "email_filled")

        password_field = driver.find_element(By.NAME, "signup_password")
        password_field.send_keys(password)
        save_click_location_screenshot(password_field, "password_filled")

        confirm_password_field = driver.find_element(By.NAME, "confirm_password")
        confirm_password_field.send_keys(password)
        save_click_location_screenshot(confirm_password_field, "confirm_password_filled")

        # إدخال تاريخ الميلاد
        date_picker = driver.find_element(By.XPATH, "//input[@class='date-picker-input']")
        date_picker.send_keys(birthdate)
        save_click_location_screenshot(date_picker, "birthdate_filled")

        # الضغط على زر "Create Account"
        submit_button = driver.find_element(By.ID, "registration-submit")
        submit_button.click()
        save_click_location_screenshot(submit_button, "submit_clicked")

        # الانتظار حتى يظهر مربع Captcha
        print("الانتظار حتى يظهر مربع Captcha...")
        try:
            # الانتظار حتى يظهر iframe الخاص بالكابتشا
            WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@title, 'reCAPTCHA')]"))
            )
            print("تم العثور على إطار الكابتشا.")
            
            # التعامل مع عناصر الكابتشا المحجوبة
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "recaptcha-checkbox-checkmark"))
            )

            # التعامل مع عناصر مغطاة
            captcha_checkbox = driver.find_element(By.CLASS_NAME, "recaptcha-checkbox-checkmark")
            ActionChains(driver).move_to_element(captcha_checkbox).click().perform()
            save_click_location_screenshot(captcha_checkbox, "captcha_clicked")
            
        except Exception as e:
            print(f"لم يتم العثور على مربع Captcha: {e}")
            save_screenshot("captcha_not_found")

        # حفظ البيانات
        save_account_number(account_number)

    except Exception as e:
        print(f"حدث خطأ أثناء إنشاء الحساب: {e}")
        save_screenshot("error")

# تشغيل الكود
create_account()

# إغلاق المتصفح
driver.quit()
