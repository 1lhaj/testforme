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

# دالة للتحقق من وجود الحساب
# دالة للتحقق من وجود الحساب
def is_account_exist(username, email):
    try:
        # فحص الحسابات في ملف CSV للتأكد من عدم التكرار
        with open("accounts.csv", "r") as file:
            accounts = csv.reader(file)
            next(accounts)  # تخطي العنوان

            # التأكد من أن هناك بيانات
            accounts_list = list(accounts)
            if not accounts_list:  # إذا كان الملف فارغًا
                return False

            for account in accounts_list:
                if len(account) >= 5:  # التأكد من أن كل صف يحتوي على البيانات المطلوبة
                    if account[0] == username or account[1] == email:
                        return True
        return False
    except FileNotFoundError:
        return False  # إذا كان الملف غير موجود من البداية
  # إذا كان الملف غير موجود من البداية

# دالة لإنشاء حساب جديد والتحقق من صحته
def create_account():
    try:
        driver.get("https://ar.secure.imvu.com/welcome/ftux/account/")  # رابط التسجيل
        time.sleep(5)  # انتظر تحميل الصفحة بالكامل

        # توليد بيانات وهمية جديدة
        username = fake.user_name()
        email = fake.email()
        password = "password123"
        birthdate = fake.date_of_birth(minimum_age=18, maximum_age=99)  # العمر أكبر من 18 سنة
        formatted_birthdate = birthdate.strftime("%Y-%m-%d")  # تنسيق التاريخ كما هو مطلوب (yyyy-mm-dd)

        # التحقق من أن الحساب غير موجود مسبقًا
        if is_account_exist(username, email):
            print(f"الحساب بالاسم {username} أو البريد {email} موجود بالفعل، جاري إنشاء حساب جديد...")
            return create_account()  # إعادة المحاولة لإنشاء حساب جديد

        # تعبئة الحقول
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

        # تحقق من أن الحساب تم إنشاؤه بنجاح
        driver.get("https://secure.imvu.com/welcome/login/")  # رابط تسجيل الدخول
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "login_email"))).send_keys(email)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "login_password"))).send_keys(password)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "login_button"))).click()

        # تحقق من تسجيل الدخول
        time.sleep(3)
        logged_in = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "user-profile")))
        if logged_in:
            print(f"تم تسجيل الدخول بنجاح باستخدام الحساب {username}.")
        else:
            print("فشل تسجيل الدخول.")

    except Exception as e:
        print(f"حدث خطأ أثناء إنشاء الحساب: {e}")

# تشغيل الكود
create_account()

# إغلاق المتصفح بعد الانتهاء
driver.quit()
