import random
import time
from temp_mails import Tenminemail_com
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
from fake_useragent import UserAgent


def extract_otp_from_email(mail_content):
    """Ekstrak OTP dari konten email HTML menggunakan BeautifulSoup."""
    soup = BeautifulSoup(mail_content, "html.parser")
    otp_match = re.search(r"\b\d{6}\b", soup.get_text())  # Cari pola angka 6 digit
    if otp_match:
        return otp_match.group(0)
    return None


def handle_popup(driver):
    """Tangani pop-up jika muncul."""
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btnOkPopOneButtonNonTitle"))
        ).click()
        print("Popup handled successfully.")
    except Exception:
        print("No popup found or failed to handle.")


def create_temp_email_with_delay():
    """Buat email sementara dengan jeda acak untuk menghindari rate limit."""
    while True:
        try:
            delay = random.randint(5, 20)
            print(f"Waiting {delay} seconds before creating a new email...")
            time.sleep(delay)
            temp_email = Tenminemail_com()
            print(f"Generated Email: {temp_email.email}")
            return temp_email
        except Exception as e:
            if "429" in str(e):
                print("Rate limit hit. Waiting for 60 seconds...")
                time.sleep(60)  # Tunggu lebih lama jika terlalu sering
            else:
                print(f"Error occurred: {e}")
                time.sleep(10)


# Setup Selenium WebDriver
service = Service(ChromeDriverManager().install())
chrome_options = Options()
chrome_options.add_argument("--headless")  # Gunakan mode headless jika tidak perlu melihat browser
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--log-level=3")
# Rotasi User-Agent
ua = UserAgent()
chrome_options.add_argument(f"user-agent={ua.random}")

driver = webdriver.Chrome(service=service, options=chrome_options)

# URL halaman pendaftaran
url = "https://arichain.com/wallet/member/signup_form"
driver.get(url)

try:
    while True:  # Loop untuk pendaftaran berulang
        # Refresh halaman sebelum memulai proses baru
        driver.refresh()

        # Buat email sementara dengan jeda acak
        temp_email = create_temp_email_with_delay()
        email_address = temp_email.email

        # Isi email pada form
        email_field = driver.find_element(By.ID, "id")
        email_field.clear()
        email_field.send_keys(email_address)

        # Klik tombol 'Get code'
        get_code_button = driver.find_element(By.ID, "btnSendEmail")
        get_code_button.click()

        # Tangani pop-up setelah klik 'Get code'
        handle_popup(driver)

        # Tunggu email masuk
        print("Waiting for email...")
        email_data = temp_email.wait_for_new_email(delay=1.0, timeout=120)
        if not email_data:
            print("No email received. Retrying...")
            continue

        # Ambil konten email berdasarkan ID
        try:
            mail_content = temp_email.get_mail_content(email_data["id"])
            print("Mail content retrieved successfully.")
        except Exception as e:
            print(f"Failed to get mail content: {e}")
            continue

        # Ekstrak OTP dari email
        otp = extract_otp_from_email(mail_content)
        if otp:
            print(f"OTP Received: {otp}")

            # Isi OTP pada form
            otp_field = driver.find_element(By.ID, "inputCode")
            otp_field.clear()
            otp_field.send_keys(otp)

            # Isi password
            password = "Dilz@2408"  # Ganti dengan pengambilan dari .env jika perlu
            password_field = driver.find_element(By.ID, "pw")
            password_field.clear()
            password_field.send_keys(password)

            # Isi password verifikasi
            password_verify_field = driver.find_element(By.ID, "pw_re")
            password_verify_field.clear()
            password_verify_field.send_keys(password)

            # Isi Referral Code
            referral_code = "678a148718fc9"  # Ganti dengan pengambilan dari .env jika perlu
            referral_code_field = driver.find_element(By.ID, "inputInviteCode")
            referral_code_field.clear()
            referral_code_field.send_keys(referral_code)

            # Klik tombol 'Sign Up'
            sign_up_button = driver.find_element(By.ID, "btnSignupFinish")
            sign_up_button.click()

            print("Sign-up process completed. Waiting for 12 seconds before restarting...")
            time.sleep(12)  # Tunggu 12 detik sebelum memulai proses berikutnya
        else:
            print("No OTP found in the email. Retrying...")

        # Tambahkan jeda sebelum memulai ulang
        time.sleep(random.randint(5, 15))

except KeyboardInterrupt:
    print("Process interrupted by user. Exiting...")
finally:
    driver.quit()
