# Automated Flight Bookings
This project demonstrates two approaches for automating flight booking searches from Delhi to Mumbai. The goal was to generate passenger data, simulate a flight search on a booking website, and save results as JSON.

## Approach 1: Using GroqCloud API + Browser Automation

Description:
This approach attempted to use the GroqCloud API with a pre-trained LLM for generating and filling flight booking forms automatically, alongside the browser-use library for web interactions.

Process:

Opened the Chrome browser and navigated to MakeMyTrip.

Attempted to use AI-generated inputs for passenger data and flight search.

Challenges:

API key misconfiguration prevented proper access to the model.

Although Chrome launched successfully and the website loaded, popups could not be reliably closed.

Outcome:

Partially automated browser interaction, but the approach could not progress beyond the popup stage.

## Approach 2: Using Selenium + Faker

Description:
This approach used Selenium for browser automation and Faker to generate realistic Indian passenger data.

Process:

Opened Chrome and navigated to MakeMyTrip.

Closed popups successfully.

Attempted to fill in departure and destination cities (From: Delhi, To: Mumbai).

Challenges:

Selenium could not interact with the city input fields due to dynamic site behavior and overlapping page elements.

Outcome:

The browser launched, popups were handled, but the automation terminated at the city input stage.

## Key Learnings

Real-world flight booking websites have dynamic elements that can break automation scripts (popups, readonly inputs, banners).

API-based approaches require valid access keys and compatible models; otherwise, scripts fail before meaningful interaction.

Using Faker + Selenium is reliable for generating test data and practicing automation workflows, even if full site interaction is blocked.

Result:

Demonstrates successful Faker-based passenger data generation and partial browser automation.

https://github.com/user-attachments/assets/cdf81028-9dc0-4bf4-b907-d2c4733a8a0f

The above video shows my attempt made to automate this.

## Future Improvements

Use test or dummy flight booking sites to ensure full Selenium automation works end-to-end.

Revisit API-based automation with correct keys and updated model availability.

Add error handling for dynamic site elements and popups to improve robustness.
