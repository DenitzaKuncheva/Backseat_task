import pytest
from Simulator import simulate, input_default

def test_simulate_returns_expected_keys():
    result = simulate(num_simulations=100, bet=10, seed=1)
    expected_keys = {
        "RTP",
        "Number of simulations",
        "Number of Wins",
        "Total Bet",
        "Win amount",
        "Average numbers of rolls",
        "Observed win probability",
    }
    assert expected_keys.issubset(result.keys())

 
def test_total_bet_matches_num_simulations_times_bet():
    result = simulate(num_simulations=500, bet=10, seed=2)
    assert result["Total Bet"] == 500 * 10

def test_win_amount_is_double_wins_times_bet():
    # Every win pays exactly 2x bet, so total win = wins * 2 * bet
    result = simulate(num_simulations=500, bet=10, seed=3)
    assert result["Win amount"] == result["Number of Wins"] * 2 * 10

def test_rtp_matches_win_amount_over_total_bet():
    result = simulate(num_simulations=500, bet=10, seed=4)
    assert result["RTP"] == pytest.approx(
        result["Win amount"] / result["Total Bet"]
    )

def test_observed_win_probability_matches_wins_over_simulations():
    result = simulate(num_simulations=500, bet=10, seed=5)
    assert result["Observed win probability"] == pytest.approx(
        result["Number of Wins"] / 500
    )

def test_reproducible_with_same_seed():
    result1 = simulate(num_simulations=1000, bet=10, seed=42)
    result2 = simulate(num_simulations=1000, bet=10, seed=42)
    assert result1 == result2

def test_different_seeds_can_give_different_results():
    result1 = simulate(num_simulations=1000, bet=10, seed=1)
    result2 = simulate(num_simulations=1000, bet=10, seed=2)
    # Not guaranteed mathematically, but astronomically likely to differ
    assert result1 != result2

def test_rtp_close_to_theoretical_value():
    # Theoretical win probability of craps is ~0.4929, win pays 2x bet,
    # so theoretical RTP ~= 0.9859. With enough simulations this should
    # land close to that value.
    result = simulate(num_simulations=50_000, bet=10, seed=7)
    assert 0.94 < result["RTP"] < 1.03
    assert 0.46 < result["Observed win probability"] < 0.53

def test_bet_of_zero_gives_zero_rtp_without_crashing():
    result = simulate(num_simulations=100, bet=0, seed=8)
    assert result["Total Bet"] == 0
    assert result["RTP"] == 0

def test_input_default_uses_default_when_input_empty(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt="": "")
    result = input_default("prompt: ", 100000, int)
    assert result == 100000

def test_input_default_casts_int(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt="": "250")
    result = input_default("prompt: ", 100000, int)
    assert result == 250
    assert isinstance(result, int)

def test_input_default_casts_to_float(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt="": "12.5")
    result = input_default("prompt: ", 10, float)
    assert result == 12.5

def test_input_default_ignores_whitespace_only_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt="": "   ")
    result = input_default("prompt: ", 10, int)
    assert result == 10