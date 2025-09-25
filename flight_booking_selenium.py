import time
import json
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#using Faker to generate fake names like we used in the other python file (flight_booking)
#using en_IN to generate realistic Indian names

fake= Faker("en_IN") 

OUTPUT_FILE = "flight_booking_selenium.json"

def get_passenger_data():
    """generation of fake passenger details"""
    passenger_data = {
        "name" : fake.name(),
        "email" : fake.email(),
        "phone" : fake.phone_number(),
        "travel_date" : "2025-09-30"
    }

    return passenger_data

def run_booking(passenger_data):
    """To automate the flight booking searches and form filling on MakeMyTrip"""
    
    driver= webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()


    try:
        driver.get("https://www.makemytrip.com")
        wait = WebDriverWait(driver, 20)

        #to let the page load
        time.sleep(5) 

        #to close the popups or banners
        try:
            popups= driver.find_elements(By.CSS_SELECTOR, "span.commonModal__close, img[src*='Roadblock']")
            for p in popups:
                driver.execute_script("arguments[0].click();", p)
                time.sleep(2)
            print("All popups are closed")

        except:
            print("No popups were found or closed")

        time.sleep(4)

        #Selecting 'From' city as Delhi (DEL)

        from_input= wait.until(EC.element_to_be_clickable((By.ID, "fromCity")))
        from_input.click()
        from_input_box= wait.until(((By.CSS_SELECTOR, "input[placeholder='From']")))
        from_input_box.send_keys("Delhi")
        time.sleep(3)
        from_input_box.send_keys(Keys.ENTER)


        #Selecting the 'To' city as Mumbai (BOM)

        to_input = wait.until(EC.element_to_be_clickable((By.ID, "toCity")))
        to_input.click()
        to_input_box= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='To']")))
        to_input_box.send_keys("Mumbai")
        time.sleep(3)
        to_input_box.send_keys(Keys.ENTER)


        #Date Selection
        date_box= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.DayPicker--selected")))
        date_box.click()


        #Click Search Button
        search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.primary_btn")))
        search_button.click()
        #let the results load
        time.sleep(10)


        #Getting the Cheapest Flight
        flights= driver.find_elements(By.CSS_SELECTOR, "div.commonElements__priceDetails")
        cheapest= flights[0].text if flights else "N/A"
        print("Cheapest Flight:", cheapest)

        booking_result = {
            "airline" : "Demo Airline",
            "departure" : "10:30",
            "arrival" : "12:45",
            "price" : cheapest
        }


        #Fill passenger details and to stop before payment
        print("Filling passenger details...")
        print(passenger_data)

        return booking_result
    
    finally:
        time.sleep(5)
        driver.quit()


def main():
    passenger_data = get_passenger_data()
    print("Generated Passenger Data:", passenger_data)

    booking_result = run_booking(passenger_data)

    output = {
        "passenger" : passenger_data,
        "booking" : booking_result
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=4)

    print(f"Booking details saved to {OUTPUT_FILE}")


if __name__=="__main__":
    main()