import random
from Craps import Craps, roll


class FixedRng:
    
    def __init__(self, rolls):
        self.rolls = iter(rolls)
 
    def randint(self, a, b):
        return next(self.rolls)

def test_roll():
    rng=FixedRng([3,4])
    assert roll(rng) == 7

def test_result_structure():
    rng = random.Random(1)
    result = Craps(bet=5, rng=rng)
    assert result["Game"] == "Craps"
    assert result["Bet"] == 5
    assert result["Outcome"] in ("win", "loss")
    assert isinstance(result["Events"], list)
    assert len(result["Events"]) >= 1
    assert "Point" in result
    assert "Win_amount" in result

def test_win_pays_double_loss_pays_zero():
    rng = random.Random(2)
    for _ in range(300):
        result = Craps(bet=10, rng=rng)
        if result["Outcome"] == "win":
            assert result["Win_amount"] == 20
        else:
            assert result["Win_amount"] == 0
 
def test_come_out_seven_is_immediate_win():
    rng = FixedRng([3, 4])  # sum = 7
    result = Craps(bet=10, rng=rng)
    assert result["Outcome"] == "win"
    assert result["Win_amount"] == 20
    assert len(result["Events"]) == 1
    assert result["Point"] == 7
 
def test_come_out_eleven_is_immediate_win():
    rng = FixedRng([5, 6])  # sum = 11
    result = Craps(bet=10, rng=rng)
    assert result["Outcome"] == "win"
    assert len(result["Events"]) == 1

def test_come_out_two_is_immediate_loss():
    rng = FixedRng([1, 1])  # sum = 2
    result = Craps(bet=10, rng=rng)
    assert result["Outcome"] == "loss"
    assert result["Win_amount"] == 0
    assert len(result["Events"]) == 1

def test_come_out_three_is_immediate_loss():
    rng = FixedRng([1, 2])  # sum = 3
    result = Craps(bet=10, rng=rng)
    assert result["Outcome"] == "loss"

def test_come_out_twelve_is_immediate_loss():
    rng = FixedRng([6, 6])  # sum = 12
    result = Craps(bet=10, rng=rng)
    assert result["Outcome"] == "loss"

def test_point_established_then_point_hit_again_wins():
    # come-out: (2,2)=4 -> point is 4
    # next roll: (3,3)=6 -> ignored, keep rolling
    # next roll: (2,2)=4 -> point hit -> win
    rng = FixedRng([2, 2, 3, 3, 2, 2])
    result = Craps(bet=10, rng=rng)
    assert result["Point"] == 4
    assert result["Outcome"] == "win"
    assert result["Win_amount"] == 20
    assert len(result["Events"]) == 3

def test_point_established_then_seven_out_loses():
    # come-out: (2,2)=4 -> point is 4
    # next roll: (3,4)=7 -> seven-out -> loss
    rng = FixedRng([2, 2, 3, 4])
    result = Craps(bet=10, rng=rng)
    assert result["Point"] == 4
    assert result["Outcome"] == "loss"
    assert result["Win_amount"] == 0
    assert len(result["Events"]) == 2

def test_events_contain_all_rolls_in_order():
    # come-out: 4 -> point 4; then 5 (ignored); then 4 (win)
    rng = FixedRng([2, 2, 2, 3, 2, 2])
    result = Craps(bet=10, rng=rng)
    assert result["Events"] == [
        "Roll 1: 4",
        "Roll 2:  5",
        "Roll 3:  4",
    ]   

def test_reproducible_with_same_seed():
    rng1 = random.Random(123)
    rng2 = random.Random(123)
    results1 = [Craps(bet=10, rng=rng1) for _ in range(50)]
    results2 = [Craps(bet=10, rng=rng2) for _ in range(50)]
    assert results1 == results2
 
def test_default_rng_used_when_none_given():
    # Should not raise, and should return a valid, well-formed result
    result = Craps(bet=10)
    assert result["Outcome"] in ("win", "loss")
    assert result["Win_amount"] in (0, 20)
 