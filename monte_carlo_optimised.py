import pandas as pd
import numpy as np
from datetime import datetime

# Load the data
data = pd.read_csv("betfair_odds.csv")

# Define electoral votes for each state
electoral_votes = {
    'Alabama': 9, 'Alaska': 3, 'Arizona': 11, 'Arkansas': 6, 'California': 54,
    'Colorado': 10, 'Connecticut': 7, 'Delaware': 3, 'District of Colombia': 3,
    'Florida': 30, 'Georgia': 16, 'Hawaii': 4, 'Idaho': 4, 'Illinois': 19,
    'Indiana': 11, 'Iowa': 6, 'Kansas': 6, 'Kentucky': 8, 'Louisiana': 8,
    'Maine (Statewide result)': 4, 'Maryland': 10, 'Massachusetts': 11, 'Michigan': 15,
    'Minnesota': 10, 'Mississippi': 6, 'Missouri': 10, 'Montana': 4, 'Nebraska (Statewide result)': 5,
    'Nevada': 6, 'New Hampshire': 4, 'New Jersey': 14, 'New Mexico': 5, 'New York': 28,
    'North Carolina': 16, 'North Dakota': 3, 'Ohio': 17, 'Oklahoma': 7,
    'Oregon': 8, 'Pennsylvania': 19, 'Rhode Island': 4, 'South Carolina': 9,
    'South Dakota': 3, 'Tennessee': 11, 'Texas': 40, 'Utah': 6, 'Vermont': 3,
    'Virginia': 13, 'Washington': 12, 'West Virginia': 4, 'Wisconsin': 10, 'Wyoming': 3
}

# Preprocess data to normalize probabilities
data['Implied_Probability'] = 1 / data['Odds']
data['Overround'] = data.groupby('Market Name')['Implied_Probability'].transform('sum')
data['Adjusted_Probability'] = data['Implied_Probability'] / data['Overround']


# Create a dictionary for quick probability lookup
probabilities = data.pivot_table(
        index='Market Name',
        columns='Runner Name',
        values='Adjusted_Probability'
    ).to_dict('index')

# Monte Carlo simulation
num_simulations = 1000000
democrat_wins = 0
republican_wins = 0
ties = 0

for _ in range(num_simulations):
    democrat_total_votes = 0
    republican_total_votes = 0
    
    for state in electoral_votes.keys():
        if state not in probabilities:
            raise ValueError(f"Probabilities for {state} not found in data.")
        
        probs = probabilities[state]
        democrat_prob = probs.get('Democrats', 0)
        republican_prob = probs.get('Republicans', 0)
        
        # Ensure probabilities sum to 1
        total_prob = democrat_prob + republican_prob
        if total_prob == 0:
            print("ERROR: No probabilities found for state", state)
            continue  # Skip states with no probabilities
        democrat_prob /= total_prob
        republican_prob /= total_prob
        
        # Simulate the state outcome
        rand = np.random.rand()
        if rand < democrat_prob:
            democrat_total_votes += electoral_votes[state]
        else:
            republican_total_votes += electoral_votes[state]
    
    # Determine the winner for this simulation
    if democrat_total_votes > republican_total_votes:
        democrat_wins += 1
    elif republican_total_votes > democrat_total_votes:
        republican_wins += 1
    else:
        ties += 1

# Calculate probabilities of each party winning with ties
total_simulations = democrat_wins + republican_wins + ties
democrat_win_probability = democrat_wins / total_simulations
republican_win_probability = republican_wins / total_simulations
tie_probability = ties / total_simulations

# Get current time and format it
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("Current time:", current_time)

# Display results
print(f"Democrat win probability: {democrat_win_probability:.2%}")
print(f"Republican win probability: {republican_win_probability:.2%}")
print(f"Tie probability: {tie_probability:.2%}")

# Calculate total win probability excluding ties
total_win_probability = democrat_wins + republican_wins
normalized_democrat_win_probability = democrat_wins / total_win_probability
normalized_republican_win_probability = republican_wins / total_win_probability

# Display normalized results
print(f"Normalized Democrat win probability: {normalized_democrat_win_probability:.2%}")
print(f"Normalized Republican win probability: {normalized_republican_win_probability:.2%}")