from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from PIL import Image, ImageDraw
import time
import os

# إعداد المتصفح
options = Options()
options.add_argument("--headless")  # تشغيل في الوضع الخفي
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)

# إعداد مجلد لحفظ لقطات الشاشة
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

# عداد الصور
screenshot_counter = 1

# حفظ لقطة الشاشة مع رسم علامة على المكان الذي تم الضغط عليه
def save_screenshot_with_click(x, y):
    global screenshot_counter

    # التقاط لقطة الشاشة
    screenshot_path = f"screenshots/{screenshot_counter}.png"
    driver.save_screenshot(screenshot_path)

    # فتح الصورة ورسم دائرة على مكان الضغط
    image = Image.open(screenshot_path)
    draw = ImageDraw.Draw(image)
    radius = 10
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline="red", width=3)
    image.save(screenshot_path)
    screenshot_counter += 1

# وظيفة للنقر على عنصر وتسجيل الموقع
def click_element_and_capture(element):
    location = element.location
    size = element.size
    x = int(location["x"] + size["width"] / 2)
    y = int(location["y"] + size["height"] / 2)

    # النقر على العنصر
    action = ActionChains(driver)
    action.move_to_element_with_offset(element, size["width"] / 2, size["height"] / 2).click().perform()

    # حفظ لقطة الشاشة مع الإشارة إلى مكان الضغط
    save_screenshot_with_click(x, y)

# تسجيل لقطات شاشة متكررة كل جزء من الثانية
def capture_every_step():
    while True:
        global screenshot_counter
        screenshot_path = f"screenshots/{screenshot_counter}.png"
        driver.save_screenshot(screenshot_path)
        screenshot_counter += 1
        time.sleep(0.1)  # التوقف لمدة 0.1 ثانية (10 مرات في الثانية)

# تنفيذ إنشاء الحساب
def create_account():
    try:
        # فتح صفحة التسجيل
        driver.get("https://ar.secure.imvu.com/welcome/ftux/account/")
        time.sleep(5)

        # تعبئة الحقول
        account_number = get_next_account_number()
        username = f"elitbotnew{account_number}"
        email = "elitbotnew{account_number}@dsf.com"
        password = "Moammedmax34"
        birthdate = "1990-01-01"
        
        username_field = driver.find_element(By.CLASS_NAME, "signup_displayname_input")
        username_field.send_keys(username)
        save_screenshot_with_click(username_field.location["x"], username_field.location["y"])

        email_field = driver.find_element(By.NAME, "signup_email")
        email_field.send_keys(email)
        save_screenshot_with_click(email_field.location["x"], email_field.location["y"])

        password_field = driver.find_element(By.NAME, "signup_password")
        password_field.send_keys(password)
        save_screenshot_with_click(password_field.location["x"], password_field.location["y"])

        confirm_password_field = driver.find_element(By.NAME, "confirm_password")
        confirm_password_field.send_keys(password)
        save_screenshot_with_click(confirm_password_field.location["x"], confirm_password_field.location["y"])

        # النقر على زر "Create Account"
        submit_button = driver.find_element(By.ID, "registration-submit")
        click_element_and_capture(submit_button)

    except Exception as e:
        print(f"حدث خطأ أثناء إنشاء الحساب: {e}")

# تشغيل الكود
try:
    # التقاط لقطات شاشة مستمرة في الخلفية
    from threading import Thread
    capture_thread = Thread(target=capture_every_step, daemon=True)
    capture_thread.start()

    # تنفيذ إنشاء الحساب
    create_account()

finally:
    driver.quit()
