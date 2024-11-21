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
options.add_argument("--headless")  # للتشغيل بدون واجهة
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)

def create_account():
    try:
        driver.get("https://ar.secure.imvu.com/welcome/ftux/account/")  # رابط التسجيل
        time.sleep(5)  # انتظر تحميل الصفحة بالكامل

        # تعبئة الحقول
        username = fake.user_name()
        email = fake.email()
        password = "password123"
        birthdate = fake.date_of_birth(minimum_age=18, maximum_age=99)  # العمر أكبر من 18 سنة
        formatted_birthdate = birthdate.strftime("%Y-%m-%d")  # تنسيق التاريخ كما هو مطلوب (yyyy-mm-dd)

        # تحقق من أن الاسم والبريد الإلكتروني غير موجودين مسبقًا (يمكنك إضافة بعض المنطق هنا للتحقق من الحسابات المكررة)
        with open("accounts.csv", "r") as file:
            accounts = csv.reader(file)
            for account in accounts:
                if account[0] == username or account[1] == email:
                    print(f"تم العثور على حساب مكرر: {username}, {email}. سيتم إنشاء حساب جديد.")
                    return  # عدم إنشاء الحساب إذا كانت البيانات مكررة

        # تعبئة البيانات في الحقول
        driver.find_element(By.CLASS_NAME, "signup_displayname_input").send_keys(username)
        driver.find_element(By.NAME, "signup_email").send_keys(email)
        driver.find_element(By.NAME, "signup_password").send_keys(password)

        # تأكد من وجود حقل إعادة إدخال كلمة المرور
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "confirm_password"))).send_keys(password)

        # إدخال تاريخ الميلاد باستخدام XPath
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//input[@class='date-picker-input']"))).send_keys(formatted_birthdate)

        # التحقق من تفعيل الزر وإزالته من حالة التعطيل إذا لزم الأمر
        submit_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "registration-submit")))
        
        # تمرير الصفحة إلى الزر للتأكد من أنه غير مغطى
        driver.execute_script("arguments[0].scrollIntoView();", submit_button)
        time.sleep(1)  # الانتظار قليلاً بعد التمرير

        if not submit_button.is_enabled():
            driver.execute_script("arguments[0].removeAttribute('disabled');", submit_button)

        # الضغط على الزر
        submit_button.click()
        print("تم إنشاء الحساب بنجاح.")

        time.sleep(5)  # انتظر قليلاً بعد الإرسال

        # حفظ البيانات في ملف CSV
        with open("accounts.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([username, email, password, username, formatted_birthdate])

    except Exception as e:
        print(f"حدث خطأ أثناء إنشاء الحساب: {e}")

def follow_account(target_username):
    try:
        driver.get("https://secure.imvu.com/welcome/login/")  # رابط تسجيل الدخول

        with open("accounts.csv", "r") as file:
            accounts = csv.reader(file)
            for account in accounts:
                username, email, password, display_name, birthdate = account

                # تسجيل الدخول
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "login_email"))).send_keys(email)
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "login_password"))).send_keys(password)
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "login_button"))).click()
                time.sleep(3)

                # متابعة الحساب
                driver.get(f"https://www.imvu.com/next/av/{target_username}/")
                follow_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "follow_button")))

                # تمرير الصفحة إلى الزر إذا كان مغطى
                driver.execute_script("arguments[0].scrollIntoView();", follow_button)
                time.sleep(1)  # الانتظار قليلاً بعد التمرير

                follow_button.click()
                print(f"تمت متابعة الحساب: {target_username}")

                # تسجيل الخروج
                driver.get("https://secure.imvu.com/welcome/logout/")
                print(f"تم تسجيل الخروج من الحساب: {email}")

    except Exception as e:
        print(f"حدث خطأ أثناء متابعة الحساب: {e}")

# تشغيل الكود
create_account()

# إغلاق المتصفح بعد الانتهاء
driver.quit()
