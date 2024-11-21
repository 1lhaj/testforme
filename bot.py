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

# إعداد البيانات الوهمية
fake = Faker()

# إعداد المتصفح في وضع headless
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)

def create_account():
    driver.get("https://ar.secure.imvu.com/welcome/ftux/account/")  # رابط التسجيل
    time.sleep(5)  # انتظر 5 ثوانٍ للتأكد من تحميل الصفحة بالكامل

    # الانتظار حتى يظهر العنصر
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "signup_displayname_input")))
    except:
        print("لم يتم العثور على العنصر بعد 30 ثانية.")
        driver.quit()
        return

    username = fake.user_name()
    email = fake.email()
    password = "password123"
    birthdate = fake.date_of_birth(minimum_age=18, maximum_age=99)  # العمر أكبر من 18 سنة
    formatted_birthdate = birthdate.strftime("%Y-%m-%d")  # تنسيق التاريخ كما هو مطلوب (yyyy-mm-dd)

    # تعبئة الحقول
    driver.find_element(By.CLASS_NAME, "signup_displayname_input").send_keys(username)  # استخدام الصنف
    driver.find_element(By.NAME, "signup_email").send_keys(email)    # استبدل "email" باسم الحقل
    driver.find_element(By.NAME, "signup_password").send_keys(password)  # كلمة السر

    # الانتظار والتأكد من وجود حقل إعادة إدخال كلمة المرور
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "confirm_password")))  # تأكد من وجود حقل إعادة إدخال كلمة السر
        driver.find_element(By.NAME, "confirm_password").send_keys(password)  # إعادة إدخال كلمة المرور
    except:
        print("لم يتم العثور على حقل إعادة إدخال كلمة المرور.")
        driver.quit()
        return

    # إدخال تاريخ الميلاد باستخدام XPath
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//input[@class='date-picker-input']")))
        driver.find_element(By.XPATH, "//input[@class='date-picker-input']").send_keys(formatted_birthdate)  # إدخال تاريخ الميلاد
    except:
        print("لم يتم العثور على حقل تاريخ الميلاد.")
        driver.quit()
        return

    # إرسال النموذج
    driver.find_element(By.NAME, "signup_submit_button").click()  # استبدل "signup_submit_button" بزر الإرسال الصحيح
    time.sleep(5)

    # حفظ البيانات في ملف CSV
    with open("accounts.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([username, email, password, username, formatted_birthdate])

def follow_account(target_username):
    driver.get("https://secure.imvu.com/welcome/login/")  # رابط تسجيل الدخول

    with open("accounts.csv", "r") as file:
        accounts = csv.reader(file)
        for account in accounts:
            username, email, password, display_name, birthdate = account
            # تسجيل الدخول
            driver.find_element(By.NAME, "login_email").send_keys(email)    # استبدل "login_email" باسم الحقل
            driver.find_element(By.NAME, "login_password").send_keys(password)  # استبدل "login_password" باسم الحقل
            driver.find_element(By.NAME, "login_button").click()  # استبدل "login_button" بزر الدخول الصحيح
            time.sleep(3)

            # متابعة الحساب
            driver.get(f"https://www.imvu.com/next/av/{target_username}/")
            driver.find_element(By.CLASS_NAME, "follow_button").click()  # استبدل "follow_button" بزر المتابعة الصحيح
            time.sleep(2)

            # تسجيل الخروج
            driver.get("https://secure.imvu.com/welcome/logout/")  # رابط تسجيل الخروج

# مثال على كيفية استخدام الدوال
create_account()
follow_account("Joseph583531")

# إغلاق المتصفح بعد الانتهاء
driver.quit()
