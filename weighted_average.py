# Defining the electoral votes and probabilities for each swing state
# The probabilities are given in percentage form, so we'll convert them to decimals for calculations.

swing_states = {
    "Georgia": {"votes": 16, "Red": 0.66, "Blue": 0.34},
    "Pennsylvania": {"votes": 19, "Red": 0.60, "Blue": 0.40},
    "Nevada": {"votes": 6, "Red": 0.55, "Blue": 0.45},
    "Wisconsin": {"votes": 10, "Red": 0.54, "Blue": 0.46},
    "North Carolina": {"votes": 16, "Red": 0.69, "Blue": 0.31},
    "Michigan": {"votes": 15, "Red": 0.37, "Blue": 0.63}
}

# Calculate weighted probabilities for Red and Blue across all swing states
total_votes = sum(state["votes"] for state in swing_states.values())

weighted_red_prob = sum(state["votes"] * state["Red"] for state in swing_states.values()) / total_votes
weighted_blue_prob = sum(state["votes"] * state["Blue"] for state in swing_states.values()) / total_votes

print(weighted_red_prob, weighted_blue_prob)
