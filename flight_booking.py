import asyncio
import os
from dotenv import load_dotenv
import json
from transformers import pipeline
from faker import Faker
from browser_use import Agent
from groq import Groq

#load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

#initializing the groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

OUTPUT_FILE = "flight_booking.json"

#generating fake data using the faker library
fake = Faker()

#creating a function to generate fake passenger details
def get_passenger_data():
    prompt = """
    Generate a JSON object which has only the mentioned things below:
    -name : realistic Indian passenger full name
    -travel_date: a travel date in "YYYY-MM-DD" format
    -email: a realistic email
    -phone: a realistic phone number
    Output ONLY valid in JSON. Nothing else.
    """
    response = client.chat.completions.create(
        model="moonshotai/kimi-k2-instruct-0905", 
        messages= [{"role": "user", "content": prompt}]
    )

    generated_text= response.choices[0].message.content.strip()
    print("Raw Output:", generated_text)

    try:
        passenger_data = json.loads(generated_text)
    except json.JSONDecodeError:
        passenger_data = {
            "name" : fake.name(),
            "email" : fake.email(),
            "phone" : fake.phone_number(),
            "travel_date" : "2025-09-30",
            "raw_output" : generated_text
        }

    return passenger_data

# by using browser-use, we will now automate browsing based on the passenger data

async def run_booking(passenger_data):
    agent = Agent(
    task = f"""
    Open MakeMyTrip.com
    Close any popups if they appear.
    Search flights from Delhi (DEL) to Mumbai (BOM) on {passenger_data['travel_date']}
    and make sure the travel dates are on present and within future 30 days.
    Sort by lowest price
    Choose the CHEAPEST flight
    Proceed to book the page.
    Fill the passenger details:
        Name : {passenger_data['name']}
        Email : {passenger_data['email']}
        Phone : {passenger_data['phone']}
    STOP BEFORE PAYMENT.
    Extract and Return flight details in JSON WITH KEYS:
        airline, departure_time, arrival_time, price
    """)

    result = await agent.run()
    return result


async def main():
    passenger_data = get_passenger_data()
    print("Generated Passenger Data", passenger_data)

    #to be able to see what is happening, we will add sleep timer of five seconds
    await asyncio.sleep(5) 

    booking_result = await run_booking(passenger_data)

    #to check our result, we will add timer for seven seconds.
    await asyncio.sleep(7)

    output = {
        "passenger" : passenger_data,
        "booking" : str(booking_result)
    }

    #saving to file
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent= 4)

    print(f"Booking details saved to {OUTPUT_FILE}")
    print("Flight Info : ", booking_result)

if __name__=="__main__":
    asyncio.run(main())
