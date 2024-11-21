from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
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

    username = fake.user_name()
    email = fake.email()
    password = "password123"
    birthdate = fake.date_of_birth(minimum_age=18, maximum_age=99)  # العمر أكبر من 18 سنة
    formatted_birthdate = birthdate.strftime("%m/%d/%Y")  # تنسيق التاريخ كما هو مطلوب (mm/dd/yyyy)

    # تعبئة الحقول
    driver.find_element(By.ID, "display_name").send_keys(username)  # استبدل "display_name" بالحقل الصحيح
    driver.find_element(By.ID, "email").send_keys(email)    # استبدل "email" بالحقل الصحيح
    driver.find_element(By.ID, "password").send_keys(password)  # استبدل "password" بالحقل الصحيح
    driver.find_element(By.ID, "reenter_password").send_keys(password)  # إعادة إدخال كلمة المرور
    driver.find_element(By.ID, "birthdate").send_keys(formatted_birthdate)  # إدخال تاريخ الميلاد

    # إرسال النموذج
    driver.find_element(By.ID, "create_account_button").click()  # استبدل "create_account_button" بزر الإرسال الصحيح
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
            driver.find_element(By.ID, "email").send_keys(email)    # استبدل "email" بالحقل الصحيح
            driver.find_element(By.ID, "password").send_keys(password)  # استبدل "password" بالحقل الصحيح
            driver.find_element(By.ID, "login_button").click()  # استبدل "login_button" بزر الدخول الصحيح
            time.sleep(3)

            # متابعة الحساب
            driver.get(f"https://www.imvu.com/next/av/{target_username}/")
            driver.find_element(By.ID, "follow_button").click()  # استبدل "follow_button" بزر المتابعة الصحيح
            time.sleep(2)

            # تسجيل الخروج
            driver.get("https://secure.imvu.com/welcome/logout/")  # رابط تسجيل الخروج

# مثال على كيفية استخدام الدوال
create_account()
follow_account("Joseph583531")

# إغلاق المتصفح بعد الانتهاء
driver.quit()
