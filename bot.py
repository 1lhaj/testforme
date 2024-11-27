import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from webdriver_manager.firefox import GeckoDriverManager
import requests

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

def solve_captcha(captcha_image_url):
    """
    إرسال Captcha إلى الخدمة للحصول على الحل.
    """
    try:
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

def get_next_account_number():
    """
    استرجاع الرقم التالي من ملف counter.txt أو إنشاء ملف جديد إذا لم يكن موجودًا.
    """
    counter_file = "counter.txt"
    if os.path.exists(counter_file):
        with open(counter_file, "r") as file:
            return int(file.read().strip()) + 1
    else:
        return 1

def save_account_number(account_number):
    """
    حفظ الرقم الأخير المستخدم في ملف counter.txt.
    """
    with open("counter.txt", "w") as file:
        file.write(str(account_number))

def create_account():
    try:
        # استرجاع الرقم التالي وإنشاء الاسم والإيميل
        account_number = get_next_account_number()
        username = f"elitbotnew{account_number}"
        email = f"elitbotnew{account_number}@dsf.com"
        password = "password123"
        birthdate = "1990-01-01"  # تاريخ ميلاد ثابت أو يمكن جعله متغيرًا

        # فتح صفحة التسجيل
        driver.get("https://ar.secure.imvu.com/welcome/ftux/account/")
        time.sleep(5)

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

        # انتظار ظهور Captcha
        print("الانتظار حتى تظهر Captcha...")
        captcha_image = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "img.captcha-image"))
        )
        captcha_url = captcha_image.get_attribute("src")

        # حل Captcha
        captcha_solution = solve_captcha(captcha_url)
        if captcha_solution:
            print(f"حل Captcha: {captcha_solution}")
            driver.find_element(By.ID, "captcha_input").send_keys(captcha_solution)

            # إعادة الضغط على زر "Create Account" بعد إدخال Captcha
            driver.execute_script("arguments[0].click();", submit_button)

            # انتظار التأكيد
            time.sleep(5)
            print(f"تم إنشاء الحساب بنجاح: {username}, {email}")

            # حفظ الرقم الأخير
            save_account_number(account_number)

            # حفظ البيانات في CSV
            with open("accounts.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([username, email, password, birthdate])
        else:
            print("فشل حل Captcha.")
    except Exception as e:
        print(f"حدث خطأ أثناء إنشاء الحساب: {e}")

# تشغيل الكود
create_account()

# إغلاق المتصفح
driver.quit()
