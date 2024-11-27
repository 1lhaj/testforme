def create_account():
    try:
        driver.get("https://ar.secure.imvu.com/welcome/ftux/account/")
        time.sleep(5)

        # توليد بيانات وهمية جديدة
        username = fake.user_name()
        email = fake.email()
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
            captcha_image = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "img.captcha-image"))
            )
            captcha_url = captcha_image.get_attribute("src")

            # حل Captcha
            captcha_solution = solve_captcha(captcha_url)
            if captcha_solution:
                driver.find_element(By.ID, "captcha_input").send_keys(captcha_solution)
            else:
                print("فشل حل Captcha.")
                return
        except Exception as e:
            print("لم يتم العثور على Captcha، الاستمرار...")

        # الضغط على زر التسجيل
        submit_button = driver.find_element(By.ID, "registration-submit")
        driver.execute_script("arguments[0].scrollIntoView();", submit_button)
        submit_button.click()

        # انتظار الصفحة الجديدة واكتشاف وجود كابتشا جديد
        try:
            captcha_image = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "img.captcha-image"))
            )
            print("تم العثور على كابتشا جديدة بعد التسجيل.")
            captcha_url = captcha_image.get_attribute("src")

            # حل Captcha الجديدة
            captcha_solution = solve_captcha(captcha_url)
            if captcha_solution:
                driver.find_element(By.ID, "captcha_input").send_keys(captcha_solution)
                submit_button = driver.find_element(By.ID, "registration-submit")
                submit_button.click()
            else:
                print("فشل حل Captcha الجديدة.")
                return
        except Exception as e:
            print("لم يتم العثور على كابتشا جديدة، المتابعة...")

        # انتظار استجابة التسجيل
        time.sleep(5)
        print(f"تم إنشاء الحساب بنجاح: {username}, {email}")

        # حفظ البيانات في CSV
        with open("accounts.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([username, email, password, username, birthdate])

    except Exception as e:
        print(f"حدث خطأ أثناء إنشاء الحساب: {e}")
