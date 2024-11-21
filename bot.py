from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from faker import Faker
import time
import csv

# إعداد البيانات الوهمية
fake = Faker()

# إعداد المتصفح
driver = webdriver.Chrome(executable_path="chromedriver")

def create_account():
    driver.get("https://ar.secure.imvu.com/welcome/ftux/account/")  # ضع رابط التسجيل الخاص بالموقع هنا

    username = fake.user_name()
    email = fake.email()
    password = "password123"

    # تعبئة الحقول
    driver.find_element(By.ID, "username_field").send_keys(username)
    driver.find_element(By.ID, "email_field").send_keys(email)
    driver.find_element(By.ID, "password_field").send_keys(password)

    # إرسال النموذج
    driver.find_element(By.ID, "submit_button").click()
    time.sleep(5)

    # حفظ البيانات
    with open("accounts.csv", "a") as file:
        file.write(f"{username},{email},{password}\n")

def follow_account(target_username):
    driver.get("https://secure.imvu.com/welcome/login/")  # ضع رابط تسجيل الدخول هنا

    with open("accounts.csv", "r") as file:
        accounts = csv.reader(file)
        for account in accounts:
            username, email, password = account
            # تسجيل الدخول
            driver.find_element(By.ID, "email_field").send_keys(email)
            driver.find_element(By.ID, "password_field").send_keys(password)
            driver.find_element(By.ID, "login_button").click()
            time.sleep(3)

            # متابعة الحساب
            driver.get(f"https://www.imvu.com/next/av/Joseph583531/")
            driver.find_element(By.ID, "follow_button").click()
            time.sleep(2)

            # تسجيل الخروج
            driver.get("https://example.com/logout")

driver.quit()
