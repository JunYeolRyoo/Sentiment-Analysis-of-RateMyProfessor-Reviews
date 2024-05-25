from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  # Import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from random import randint

chrome_options = Options()
chrome_options.add_argument("--headless")  # Enable headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
chrome_options.add_argument("--window-size=1920x1080")  # Set the window size

# load the driver with headless options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

files = {
    "1": open("1.txt", "w"),
    "2": open("2.txt", "w"),
    "3": open("3.txt", "w"),
    "4": open("4.txt", "w"),
    "5": open("5.txt", "w"),
}

num_prof = 1
digit = 10001   # Don't touch it. Start from 10001
while digit < 50000:
    try:
        # Navigate to the professor's review page
        driver.get("https://www.ratemyprofessors.com/professor/"+ str(digit).strip())
        digit += 1

        # Click the pagination button multiple times
        for n in range(800):
            try:
                button = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.Buttons__Button-sc-19xdot-1.PaginationButton__StyledPaginationButton-txi1dr-1.eUNaBX"))
                )
                driver.execute_script("arguments[0].click();", button)
                time.sleep(randint(1, 5))
                print("Button Clicked")
            except (TimeoutException, NoSuchElementException) as e:
                print("Element not found or clickable")
                break

        # Extract ratings and comments
        ratings = driver.find_elements(By.CSS_SELECTOR, 'div.Rating__RatingBody-sc-1rhvpxz-0')
        for rating in ratings:
            try:
                score = rating.find_element(By.CSS_SELECTOR, 'div.CardNumRating__CardNumRatingNumber-sc-17t4b9u-2').text[0]
                comment = rating.find_element(By.CSS_SELECTOR, 'div.Comments__StyledComments-dzzyvm-0').text.strip()
                if score in files:
                    files[score].write(comment + '\n')
            except (TimeoutException, NoSuchElementException) as e:
                print("Error processing a rating:", e)
        print(len(ratings), "ratings were written to txt file")
    except Exception as e:
        print("Error processing professor page:", e)

    print("---------------------Finished one professor -----------------------------{}-{}".format(num_prof,digit))
    num_prof += 1

    # Navigate back to the previous page
    driver.back()

for file in files.values():
    file.close()

# Quit the Chrome driver
driver.quit()