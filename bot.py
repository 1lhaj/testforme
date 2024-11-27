from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
import time
import csv
from webdriver_manager.firefox import GeckoDriverManager
import requests

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

def take_screenshot(filename):
    """
    التقاط لقطة شاشة وحفظها
    """
    driver.save_screenshot(f"{filename}.png")
    print(f"تم حفظ لقطة الشاشة: {filename}.png")

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

def click_captcha_checkbox():
    try:
        print("التحقق من وجود مربع Captcha...")
        # العثور على iframe الخاص بـ Captcha
        captcha_iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[@title='reCAPTCHA']"))
        )
        driver.switch_to.frame(captcha_iframe)  # التبديل إلى iframe الخاص بـ Captcha
        
        # العثور على label الخاص بـ Captcha والنقر عليه
        captcha_label = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[@id='recaptcha-anchor-label']"))
        )
        captcha_label.click()  # النقر على Captcha
        print("تم الضغط على مربع Captcha.")
        
        driver.switch_to.default_content()  # العودة إلى الإطار الأساسي
    except Exception as e:
        print(f"حدث خطأ أثناء النقر على مربع Captcha: {e}")
        take_screenshot("captcha_click_error")

def create_account():
    try:
        driver.get("https://ar.secure.imvu.com/welcome/ftux/account/")
        time.sleep(5)

        # توليد بيانات وهمية جديدة
        username = fake.user_name()
        email = f"{fake.user_name()}@dsf.com"
        password = "password123"
        birthdate = fake.date_of_birth(minimum_age=18, maximum_age=99).strftime("%Y-%m-%d")

        # تعبئة الحقول
        driver.find_element(By.CLASS_NAME, "signup_displayname_input").send_keys(username)
        driver.find_element(By.NAME, "signup_email").send_keys(email)
        driver.find_element(By.NAME, "signup_password").send_keys(password)
        driver.find_element(By.NAME, "confirm_password").send_keys(password)

        # إدخال تاريخ الميلاد
        date_picker = driver.find_element(By.XPATH, "//input[@class='date-picker-input']")
        date_picker.send_keys(birthdate)

        # التحقق من وجود Captcha
        try:
            # الضغط على Captcha بعد تقديم البيانات
            click_captcha_checkbox()

            # الانتظار حتى يتم حل Captcha
            time.sleep(10)  # تعديل الوقت حسب الحاجة
            print("تم التعامل مع Captcha، المتابعة...")
        except Exception as e:
            print("لم يتم العثور على Captcha، الاستمرار...")

        # الضغط على زر التسجيل باستخدام JavaScript
        submit_button = driver.find_element(By.ID, "registration-submit")
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", submit_button)

        # انتظار استجابة التسجيل
        time.sleep(5)
        print(f"تم إنشاء الحساب بنجاح: {username}, {email}")

        # حفظ البيانات في CSV
        with open("accounts.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([username, email, password, birthdate])

    except Exception as e:
        print(f"حدث خطأ أثناء إنشاء الحساب: {e}")
        take_screenshot("error")

# تشغيل الكود
create_account()

# إغلاق المتصفح
driver.quit()
