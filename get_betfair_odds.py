import requests
import json
import csv
import betfairlightweight
from betfairlightweight import filters
from datetime import datetime

# Your Betfair credentials and API key
USERNAME = '<USERNAME>'
PASSWORD = '<PASSWORD>'
APP_KEY = '<APP_KEY>'

# Initialize Betfair API client
trading = betfairlightweight.APIClient(USERNAME, PASSWORD, app_key=APP_KEY, certs="./certs")

trading.login()  # Log in to Betfair

# Function to retrieve odds and probabilities for all markets in a given event
def get_odds_and_probabilities(event_id):
    # Open CSV file to write the data
    with open("betfair_odds.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Market ID", "Market Name", "Runner ID", "Runner Name", "Odds", "Probability"])

        # Define filter to get markets for the event
        market_filter = filters.market_filter(event_ids=[event_id])

        # List all markets for the event
        market_catalogues = trading.betting.list_market_catalogue(
            filter=market_filter,
            max_results=100,  # Increase to retrieve all markets
            market_projection=['MARKET_DESCRIPTION', 'RUNNER_METADATA']
        )
        
        if not market_catalogues:
            print("No markets found for the given event ID.")
            return

        # Iterate over each market
        for market_catalogue in market_catalogues:
            market_id = market_catalogue.market_id
            market_name = market_catalogue.market_name
            print(f"\nMarket ID: {market_id}, Market Name: {market_name}")

            # Get the odds (prices) for this market
            price_filter = filters.price_projection(price_data=['EX_BEST_OFFERS'])
            market_books = trading.betting.list_market_book(
                market_ids=[market_id],
                price_projection=price_filter
            )

            if not market_books:
                print("No market books found.")
                continue

            # Extract runner data for the market
            market_book = market_books[0]
            runners = market_book.runners

            # Sort runners by available odds (lowest odds first)
            sorted_runners = sorted(runners, key=lambda x: x.last_price_traded or float('inf'))

            # Display and write the top two runners with odds and implied probabilities
            for runner in sorted_runners[:2]:  # Adjust to get more runners if needed
                odds = runner.last_price_traded
                probability = 1 / odds if odds else 0
                runner_name = next(
                    (runner_catalogue.runner_name for runner_catalogue in market_catalogue.runners if runner_catalogue.selection_id == runner.selection_id),
                    "Unknown"
                )

                # Print runner information
                print(f"  Runner ID: {runner.selection_id}, Runner Name: {runner_name}, Odds: {odds}, Probability: {probability:.2f}")

                # Write to CSV
                writer.writerow([
                    market_id,
                    market_name,
                    runner.selection_id,
                    runner_name,
                    odds,
                    f"{probability:.2f}"
                ])

# Replace '33356718' with the specific event ID you want to analyze
event_id = '33356718'
get_odds_and_probabilities(event_id)

# Get current time and format it
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("Current time:", current_time)

# Logout when done
trading.logout()