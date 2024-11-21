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

    # تعبئة الحقول (تأكد من صحة أسماء الحقول)
    driver.find_element(By.ID, "name").send_keys(username)  # استبدل "name" بالحقل الصحيح
    driver.find_element(By.ID, "email").send_keys(email)    # استبدل "email" بالحقل الصحيح
    driver.find_element(By.ID, "password").send_keys(password)  # استبدل "password" بالحقل الصحيح

    # إرسال النموذج
    driver.find_element(By.ID, "submit_button").click()  # استبدل "submit_button" بزر الإرسال الصحيح
    time.sleep(5)

    # حفظ البيانات
    with open("accounts.csv", "a") as file:
        file.write(f"{username},{email},{password}\n")

def follow_account(target_username):
    driver.get("https://secure.imvu.com/welcome/login/")  # رابط تسجيل الدخول

    with open("accounts.csv", "r") as file:
        accounts = csv.reader(file)
        for account in accounts:
            username, email, password = account
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
