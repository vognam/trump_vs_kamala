import pandas as pd
import numpy as np

# Load the data
data = pd.read_csv("betfair_odds.csv")  # Replace with the correct path

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


# Monte Carlo simulation
num_simulations = 10000
democrat_wins = 0
republican_wins = 0

for _ in range(num_simulations):
    democrat_total_votes = 0
    republican_total_votes = 0
    
    for state, group in data.groupby("Market Name"):
        # Get the probabilities for each party
        democrat_prob = group[group["Runner Name"] == "Democrats"]["Probability"].values[0]
        republican_prob = group[group["Runner Name"] == "Republicans"]["Probability"].values[0]

        # Normalize probabilities
        total_prob = democrat_prob + republican_prob
        democrat_prob /= total_prob
        republican_prob /= total_prob
        
        # Simulate the state outcome
        if np.random.rand() < democrat_prob:
            democrat_total_votes += electoral_votes[state]
        else:
            republican_total_votes += electoral_votes[state]
    
    # Determine the winner for this simulation
    ties = 0

    # In the simulation loop
    if democrat_total_votes > republican_total_votes:
        democrat_wins += 1
    elif republican_total_votes > democrat_total_votes:
        republican_wins += 1
    else:
        ties += 1

# Calculate probabilities of each party winning
democrat_win_probability = democrat_wins / num_simulations
republican_win_probability = republican_wins / num_simulations
tie_probabilitiy = ties / num_simulations

# Display results
print(f"Democrat win probability: {democrat_win_probability:.2%}")
print(f"Republican win probability: {republican_win_probability:.2%}")
print(f"Tie probability: {tie_probabilitiy:.2%}")
