import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 30)

    try:
        # 1. Homepage
        driver.get("https://v2f-core-uat.web.app/")

        # 2. Search Dubai
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@formcontrolname='destinationCountry']"))).send_keys("Dubai")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(., 'Dubai')]"))).click()

        # 3. Purpose page
        wait.until(EC.url_contains("/visa/select-purpose?country=Dubai"))
        print("✅ Reached select-purpose page")

        # 4. Pick Tourist as Visa Purpose
        wait.until(EC.element_to_be_clickable((By.XPATH, "//p[normalize-space()='Tourist']"))).click()

        # 5. Plan page
        wait.until(EC.url_contains("/visa/select-plan?country=dubai&purpose=tourist"))
        print("✅ Reached select-plan page")

        # 6. Find & click the cheapest plan’s Select button
        plans = wait.until(EC.visibility_of_all_elements_located((
            By.XPATH, "//div[contains(@class,'pricing')]"
        )))
        lowest = float("inf")
        for p in plans:
            price = p.find_element(
                By.XPATH, ".//a[contains(@class,'dropdown-toggle')]/span"
            ).text.replace(",", "")
            lowest = min(lowest, float(price))
        price_str = f"{int(lowest):,}"

        # Click its “Select” button
        select_button_xpath = (
            f"//div[contains(@class,'card-plan-detail')]"
            f"[.//a[contains(@class,'dropdown-toggle')]/span"
            f"[normalize-space(text())='{price_str}']]"
            f"//button[contains(@class,'btn-select')]"
        )
        select_button = wait.until(EC.element_to_be_clickable((By.XPATH, select_button_xpath)))
        driver.execute_script("arguments[0].scrollIntoView(true);", select_button)
        select_button.click()

        # 7. Plan Details page
        wait.until(lambda d: re.search(
            r"/visa/plan-detail\?country=dubai&purpose=tourist&iso=&quoteId=Dubai-quote-",
            d.current_url
        ))
        print("✅ On plan-detail page")

        # 8. Click Continue
        wait.until(EC.element_to_be_clickable((By.ID, "visa-plan-continue"))).click()
        print("✅ Clicked Continue, navigating to login…")

        # 9 Login page
        wait.until(EC.url_contains("/auth/login"))
        print("✅ On login page, URL:", driver.current_url)

        #10 Enter Phone Number
        phone_input = wait.until(EC.element_to_be_clickable((By.ID, "userId")))
        phone_input.clear()
        phone_input.send_keys(input("Enter your phone/email: ").strip())

        get_otp_button = wait.until(EC.element_to_be_clickable((By.ID, "get-login-otp")))
        get_otp_button.click()
        print("✅ Get OTP clicked")

        # Enter OTP
        otp_code = input("Enter the OTP you received (or type any 6-digit code to mock): ").strip()

        # wait for all the individual OTP input boxes to appear
        otp_fields = wait.until(EC.presence_of_all_elements_located((
            By.CSS_SELECTOR, "input[autocomplete='one-time-code']"
        )))

        # type one character into each box
        for idx, digit in enumerate(otp_code):
            otp_fields[idx].send_keys(digit)

        verify_button = wait.until(EC.element_to_be_clickable((By.ID, "verify-account")))
        verify_button.click()
        print("✅ Verify Account clicked, logging in…")

        input("🚀 Press Enter to close the browser and exit script…")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
