# visa-automation

Selenium-based script using Python automating the Homescreen to till Login page simulating the visa journey of a user.

# Technologies Used

- Python 3.12
- Selenium
- Google Chrome (compatible with your `chromedriver`)  

# Usage
Run the script directly-

- python main.py

1. Country Selection
- Types “Dubai” into the search box and selects it.

2. Purpose Selection
- Chooses “Tourist.”

3. Plan Selection
- Scans available plans, picks the cheapest, and clicks Select.

4. Plan Details & Continue
- Waits for plan-detail page, clicks Continue.
- 
5. Login + OTP

- Prompts you to enter your phone or email.
- Clicks Get OTP, then prompts you to paste the OTP from your device.
- Enters OTP into the individual fields and clicks Verify Account.

6. Pause

- After verification, the browser remains open for you to inspect the result.
- Press Enter in the console to close the browser and end the script.
