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
import requests
import os

# إعداد البيانات الوهمية
fake = Faker()

# إعداد المتصفح في وضع headless
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)

# بيانات API الخاصة بحل Captcha
CAPTCHA_API_KEY = "a67d3ce22ef5749d70ee34da412c5f32d998462a"
CAPTCHA_API_URL = "https://api.zenrows.com/v1/"

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

# حفظ لقطات الشاشة
def save_screenshot(step_name):
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    driver.save_screenshot(f"screenshots/{step_name}.png")
    print(f"تم حفظ لقطة الشاشة: {step_name}.png")

# حفظ لقطة شاشة عند الضغط على المكان المحدد
def save_click_location_screenshot(x, y, step_name):
    action = ActionChains(driver)
    action.move_by_offset(x, y).perform()
    time.sleep(1)  # الانتظار قليلاً للتأكد من أن الإحداثيات تم تحديدها
    save_screenshot(f"{step_name}_clicked_at_{x}_{y}")

# حل Captcha باستخدام API
def solve_captcha(captcha_image_url):
    try:
        print(f"جاري محاولة حل Captcha: {captcha_image_url}")
        params = {
            'url': captcha_image_url,
            'apikey': CAPTCHA_API_KEY,
        }
        response = requests.get(CAPTCHA_API_URL, params=params)
        if response.status_code == 200:
            result = response.json()
            return result.get("text", "")
        else:
            print(f"خطأ في حل Captcha: {response.status_code}")
            return None
    except Exception as e:
        print(f"حدث خطأ أثناء حل Captcha: {e}")
        return None

# النقر باستخدام إحداثيات معينة
def click_at_position(x, y):
    action = ActionChains(driver)
    action.move_by_offset(x, y).click().perform()

# التعامل مع الكابتشا
def handle_captcha():
    try:
        # البحث عن الإطار (iframe) الذي يحتوي على الكابتشا
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@title, 'reCAPTCHA')]"))
        )
        print("تم التبديل إلى إطار الكابتشا.")

        # العثور على مربع الكابتشا
        captcha_checkbox = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "recaptcha-checkbox-checkmark"))
        )
        captcha_checkbox.click()
        print("تم النقر على مربع الكابتشا.")
        save_screenshot("captcha_clicked")

        # الرجوع إلى الإطار الأساسي
        driver.switch_to.default_content()
    except Exception as e:
        print(f"حدث خطأ أثناء التعامل مع الكابتشا: {e}")
        save_screenshot("captcha_error")

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
        driver.find_element(By.CLASS_NAME, "signup_displayname_input").send_keys(username)
        driver.find_element(By.NAME, "signup_email").send_keys(email)
        driver.find_element(By.NAME, "signup_password").send_keys(password)
        driver.find_element(By.NAME, "confirm_password").send_keys(password)

        # إدخال تاريخ الميلاد
        date_picker = driver.find_element(By.XPATH, "//input[@class='date-picker-input']")
        date_picker.send_keys(birthdate)

        # الضغط على زر "Create Account"
        submit_button = driver.find_element(By.ID, "registration-submit")
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", submit_button)
        save_screenshot("after_submit")

        # التعامل مع الكابتشا
        handle_captcha()

        # انتظار تأكيد الحساب
        time.sleep(5)
        save_screenshot("account_created")
        print(f"تم إنشاء الحساب بنجاح: {username}, {email}")

        # حفظ الرقم الأخير
        save_account_number(account_number)

        # حفظ البيانات في CSV
        with open("accounts.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([username, email, password, birthdate])

    except Exception as e:
        print(f"حدث خطأ أثناء إنشاء الحساب: {e}")
        save_screenshot("error")

# تشغيل الكود
create_account()

# إغلاق المتصفح
driver.quit()
