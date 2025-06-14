import os
import time
import pyperclip 
from playwright.sync_api import sync_playwright
from licensing.methods import Key, Helpers
import colorama
from colorama import Fore, Style
import zipfile

extension_zip = "Trust Wallet.zip"


if not os.path.exists(extension_zip):
    raise FileNotFoundError(f"Extension file '{extension_zip}' not found in the current directory.")


extension_path = os.path.abspath(extension_zip)


extracted_extension_path = os.path.splitext(extension_path)[0]  # Remove .zip from name

if not os.path.exists(extracted_extension_path):
    with zipfile.ZipFile(extension_zip, 'r') as zip_ref:
        zip_ref.extractall(extracted_extension_path)


if not os.path.exists("phrase.txt"):
    raise FileNotFoundError("File 'phrase.txt' not found in the current directory.")


with open("phrase.txt", "r") as file:
    phrases = [line.strip() for line in file if line.strip()]  # Read non-empty lines

if not phrases:
    raise ValueError("No phrases found in 'phrase.txt'.")

print(f"Found {len(phrases)} phrases. Processing them one by one...")


with sync_playwright() as p:
    browser_type = p.chromium

    for index, secret_phrase in enumerate(phrases, start=1):
        print(f"\nProcessing phrase {index}/{len(phrases)}: {secret_phrase}")

       
        pyperclip.copy(secret_phrase)
        print("Secret phrase copied to clipboard.")

      
        context = browser_type.launch_persistent_context(
            user_data_dir=os.path.join(os.getcwd(), f"user_data_{index}"),  
            headless=False, 
            args=[
                f"--disable-extensions-except={extracted_extension_path}",
                f"--load-extension={extracted_extension_path}",
            ],
        )

        
        page = context.pages[0]  
        page.set_default_navigation_timeout(30000)  

        
        trust_wallet_url = "chrome-extension://egjidjbpglichdcondbcbdnbeeppgdph/home.html#/onboarding"
        print(f"Navigating to {trust_wallet_url}...")
        page.goto(trust_wallet_url)

        try:
            
            target_xpath = '//*[@id="root"]/div/div[2]/div/div/div/div/div[3]/div/div/div[2]/p[1]'
            page.wait_for_selector(target_xpath, timeout=10000)
            page.locator(target_xpath).click()
            time.sleep(2)
            
            print("Checking for extra tabs...")
            tabs = context.pages  

           
            if len(tabs) > 1:
                for tab in tabs[1:]:  
                    print(f"Closing tab: {tab.url}")
                    tab.close()

            
            new_password_xpath = '//*[@id="root"]/div[2]/div/div/div[2]/form/div[1]/div/div/input'
            confirm_password_xpath = '//*[@id="root"]/div[2]/div/div/div[2]/form/div[2]/div/div/input'
            checkbox_selector = '[data-testid="checkbox-terms-of-service"]'
            next_button_xpath = '//*[@id="root"]/div[2]/div/div/div[2]/form/div[4]/div[2]/button'
            alternate_button_xpath = '//*[@id="root"]/div[2]/div/div/div[2]/form/div[2]/div[2]/button'

            try:
                page.wait_for_selector(new_password_xpath, timeout=5000)  
                new_password = "Laila#1019$"
                print(f"Entering the password: {new_password}")
                page.locator(new_password_xpath).fill(new_password)
                page.wait_for_selector(confirm_password_xpath, timeout=5000)  
                confirm_password = "Laila#1019$"
                print(f"Entering the password: {new_password}")
                page.locator(confirm_password_xpath).fill(confirm_password)
                page.wait_for_selector(checkbox_selector, state='visible', timeout=10000)
                page.locator(checkbox_selector).check()

                time.sleep(2)
                page.wait_for_selector(next_button_xpath, timeout=10000)
                page.locator(next_button_xpath).click()

            except Exception:
                print("Password field not found. Clicking alternate button.")
                page.locator(alternate_button_xpath).click()  
                time.sleep(2) 

            
            print("Pasting the secret phrase into the input field...")
            page.keyboard.press("Control+V")

            invalid_message_selector = '.text-textBrand.caption-text.flex-1.text-start'
            
            try:
                page.wait_for_selector(invalid_message_selector, timeout=5000)
                print("Invalid secret phrase detected.")

                
                with open("Wrong Phrase.txt", "a") as wrong_file:
                    wrong_file.write(secret_phrase + "\n")
                print(f"Invalid phrase saved in 'Wrong Phrase.txt'.")

                
                with open("phrase.txt", "r") as file:
                    lines = file.readlines()

                with open("phrase.txt", "w") as file:
                    
                    file.writelines([line for line in lines if line.strip() != secret_phrase])

                print(f"Invalid phrase removed from 'phrase.txt'.")

            except Exception:
                print("Valid secret phrase detected.")
                with open("True Phrase.txt", "a") as true_file:
                    true_file.write(secret_phrase + "\n")
                print(f"Valid phrase saved in 'True Phrase.txt'.")
        finally:
            
            print(f"Closing the browser for phrase {index}...")
            context.close()

    print("All phrases processed.")
