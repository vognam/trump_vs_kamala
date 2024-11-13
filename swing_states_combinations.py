# Correcting the approach to calculate probability of Blue winning the majority of electoral votes
from itertools import product

# Step 1: Define the states with their electoral votes and respective Blue win probabilities
swing_states = [
    {"name": "Georgia", "votes": 16, "prob_blue": 0.34},
    {"name": "Pennsylvania", "votes": 19, "prob_blue": 0.40},
    {"name": "Nevada", "votes": 6, "prob_blue": 0.45},
    {"name": "Wisconsin", "votes": 10, "prob_blue": 0.46},
    {"name": "North Carolina", "votes": 16, "prob_blue": 0.31},
    {"name": "Michigan", "votes": 15, "prob_blue": 0.63}
]

# Step 2: Total electoral votes
total_votes = sum(state["votes"] for state in swing_states)
majority_needed = total_votes // 2 + 1  # Minimum votes for majority

# Step 3: Generate all possible outcomes and calculate probabilities
# Each state can either go Blue or Red, forming a "binary" outcome for each state
prob_blue_wins = 0.0  # To accumulate the total probability where Blue wins majority
prob_red_wins = 0.0  # To accumulate the total probability where Red wins majority

# We loop through each combination of outcomes (Blue or Red win in each state)
for outcome in product([True, False], repeat=len(swing_states)):
    blue_votes = 0
    red_votes = 0
    outcome_prob = 1.0  # Probability of this specific combination of outcomes
    
    # Calculate votes and probability for this specific outcome
    for i, state in enumerate(swing_states):
        if outcome[i]:  # If True, this state goes to Blue
            blue_votes += state["votes"]
            outcome_prob *= state["prob_blue"]
        else:  # If False, this state goes to Red
            outcome_prob *= (1 - state["prob_blue"])
            red_votes += state["votes"]
    
    # Check if this outcome gives Blue a majority
    if blue_votes >= majority_needed:
        prob_blue_wins += outcome_prob
    elif red_votes >= majority_needed:
        prob_red_wins += outcome_prob

# last one takes into account a tie
print(prob_blue_wins, prob_red_wins, 1 - prob_blue_wins - prob_red_wins)
