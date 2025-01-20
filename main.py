import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from temp_mails import Tenminemail_com
from dotenv import load_dotenv
import os
import re
from bs4 import BeautifulSoup

# Load variabel dari .env
load_dotenv()

# Variabel konfig
PASSWORD = os.getenv("PASSWORD", "DefaultPassword123!")
REFERRAL = os.getenv("REFERRAL", "678a148718fc9")
TIMEOUT = int(os.getenv("TIMEOUT", "120"))

def extract_otp_from_email(mail_content):
    """Fungsi untuk mengekstrak OTP dari konten email HTML menggunakan BeautifulSoup."""
    soup = BeautifulSoup(mail_content, "html.parser")
    otp_match = re.search(r"\b\d{6}\b", soup.get_text())  # Cari pola angka 6 digit
    if otp_match:
        return otp_match.group(0)
    return None

def handle_popup(driver):
    """Fungsi untuk menangani pop-up jika ada."""
    try:
        # Tambahkan jeda eksplisit sebelum menunggu popup
        time.sleep(7)  # Jeda 7 detik untuk memastikan popup muncul
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btnOkPopOneButtonNonTitle"))
        ).click()
        print("Popup handled successfully.")
    except Exception:
        print("No popup detected or failed to handle.")

def initialize_driver():
    """Inisialisasi driver Selenium."""
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")  # Hapus baris ini untuk GUI mode
    #options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(service=service, options=options)

def main():
    """Fungsi utama untuk menjalankan proses pendaftaran."""
    url = "https://arichain.com/wallet/member/signup_form"

    while True:
        try:
            # Inisialisasi driver
            driver = initialize_driver()
            driver.get(url)

            # Refresh halaman sebelum memulai proses baru
            driver.refresh()

            # Buat email sementara menggunakan `temp-mails`
            temp_email = Tenminemail_com()
            email_address = temp_email.email
            print(f"Generated Email: {email_address}")

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
            email_data = temp_email.wait_for_new_email(delay=1.0, timeout=TIMEOUT)
            if not email_data:
                print("No email received. Retrying...")
                continue

            # Ambil konten email berdasarkan ID
            mail_content = temp_email.get_mail_content(email_data["id"])
            print("Mail content retrieved successfully.")

            # Ekstrak OTP dari email
            otp = extract_otp_from_email(mail_content)
            if otp:
                print(f"OTP Received: {otp}")

                # Isi OTP pada form
                otp_field = driver.find_element(By.ID, "inputCode")
                otp_field.clear()
                otp_field.send_keys(otp)

                # Isi password
                password_field = driver.find_element(By.ID, "pw")
                password_field.clear()
                password_field.send_keys(PASSWORD)

                # Isi password verifikasi
                password_verify_field = driver.find_element(By.ID, "pw_re")
                password_verify_field.clear()
                password_verify_field.send_keys(PASSWORD)

                # Isi Referral Code
                referral_code_field = driver.find_element(By.ID, "inputInviteCode")
                referral_code_field.clear()
                referral_code_field.send_keys(REFERRAL)

                # Klik tombol 'Sign Up'
                sign_up_button = driver.find_element(By.ID, "btnSignupFinish")
                driver.execute_script("arguments[0].click();", sign_up_button)  # Gunakan JavaScript click

                print("Sign-up process completed. Waiting before restarting...")
                time.sleep(12)  # Tunggu sebelum memulai ulang
            else:
                print("No OTP found in the email. Retrying...")

        except Exception as e:
            print(f"An error occurred: {e}. Restarting process...")
        finally:
            try:
                driver.quit()
            except Exception:
                print("Driver already closed or not initialized. Continuing loop...")

# Jalankan program utama
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program terminated by user.")
