"""Step 3 — Deliverable 2: The Simulator
Implement a simulator that runs the game repeatedly.
Input: - the number of simulations to run, and - the bet amount.
Behaviour: run the game that many times and accumulate the total amount bet and the total
amount won across all rounds.
Output: the RTP (Return To Player), defined as:
RTP = accumulated win / accumulated bet
Feel free to also surface any additional statistics you find useful (e.g. observed win probability,
average number of steps/rolls), but RTP is the required result."""

import random

from Craps import Craps


def input_default(prompt, default, cast):
    value=input(prompt)
    if value.strip():
        return cast(value) 
    
    return default


def simulate(num_simulations, bet, seed=None):
    rng=random.Random(seed)

    total_bet = 0.0
    total_win = 0.0
    wins = 0
    total_events = 0

    for _ in range(num_simulations):
        curr = Craps(bet, rng=rng)
        total_bet += curr["Bet"]
        total_win += curr["Win_amount"]
        total_events += curr.get("steps",len(curr.get("Events",[])))
        if curr["Outcome"] == "win":
            wins += 1

    rtp=0
    if total_bet != 0:
        rtp=total_win/total_bet

    return{
        "RTP": rtp,
        "Number of simulations": num_simulations,
        "Number of Wins": wins,
        "Total Bet": total_bet,
        "Win amount": total_win,
        "Average numbers of rolls":total_events/num_simulations,
        "Observed win probability": wins/num_simulations

    }

def _main():
    num_simulations = input_default("Input numbers of Simulations: ", 100000, int)
    bet = input_default("Input Bet: ", 10, float)
    seed = input_default("Input seed: ", None, int)
    result=simulate(num_simulations,bet,seed)
    print(f"RTP: {result['RTP']}")
    print(f"Number of simulations: {result['Number of simulations']}")
    print(f"Number of Wins: {result['Number of Wins']}")
    print(f"Total Bet: {result['Total Bet']}")
    print(f"Win amount: {result['Win amount']}")
    print(f"Average numbers of rolls: {result['Average numbers of rolls']}")
    print(f"Observed win probability: {result['Observed win probability']}")
    

if __name__ == "__main__":
    _main()


