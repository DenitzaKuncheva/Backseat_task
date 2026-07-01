"""Problem 5 — Craps
The player rolls two dice.
• On the initial (come-out) roll:
• A sum of 7 or 11 → the player wins immediately.
• A sum of 2, 3, or 12 → the player loses immediately.
• Any other sum becomes the "point", and play continues.
• If a point was established, the player keeps rolling until either:
• the point is rolled again → the player wins, or
• a 7 is rolled → the player loses. 
Step 2 — Deliverable 1: The Game Engine
Implement the chosen game as a single, reusable game function/module.
Input: a bet amount (a numeric value).
Output: a well-structured response object describing exactly what happened during one full play
cycle of the game. This should be structured data (e.g. an object / dictionary / JSON), not just
printed text. At minimum it should make clear:
• the bet amount,
• the sequence of events in the round (the rolls made, or the path the spider took),
• the outcome (win / loss where applicable), and
• the amount won. 
"""
import random
def roll(rng=None):
  d1=rng.randint(1,6)
  d2=rng.randint(1,6)
  total=d1+d2
  return total


def Craps(bet, rng=None):
    if rng is None:
     rng = random.Random()

    events = []
    curr=roll(rng)
    events.append(f"Roll 1: {curr}")
    point=curr
    if curr in (7, 11):
     outcome="win"
    elif curr in(2,3,12):
     outcome="loss"
    else:
     outcome=None
     rollNumber=1
     while outcome is None:
       curr=roll(rng)
       rollNumber+=1
       events.append(f"Roll {rollNumber}:  {curr}")
       if curr==point:
         outcome="win"
       elif curr==7:
         outcome="loss"
         
    win_amount=0
    if outcome=="win":
        win_amount=2*bet 
   
    return{
      "Game": "Craps",
      "Bet": bet,
      "Point": point,
      "Events": events,
      "Outcome":outcome,
      "Win_amount":win_amount,


    }

"""test:"""
if __name__ == "__main__":
    # Small manual demo
    rng = random.Random(99)
    for _ in range(3):
        result = Craps(bet=10, rng=rng)
        print(result)



    


