# Take-Home Engineering Task: Craps

Implementation of **Problem 5 (Craps)** as a game engine + simulator, with
a pytest test suite covering both.

## Project structure

```
.
├── Craps.py            # game engine
├── Simulator.py         # simulator + interactive CLI
├── test_Craps.py        # tests for the game engine
└── test_Simulator.py    # tests for the simulator
```

All files live in the same folder — no imports need any path setup.

## Requirements

- Python 3.x
- `pytest` (only external dependency, used for running the tests)

```bash
pip install pytest
```

Everything else used in the project (`random`) is part of the Python
standard library.


## Game engine — `Craps.py`

```python
def Craps(bet, rng=None) -> dict
```

- `bet`: the amount wagered (numeric).
- `rng`: an optional `random.Random` instance, used so results can be made
  reproducible (see "Seeding" below). If not provided, a fresh, unseeded
  `random.Random()` is created.

Returns a dict describing the full round:

```python
{
    "Game": "Craps",
    "Bet": bet,
    "Point": point,        # the point established on come-out, or the
                            # come-out sum itself if won/lost immediately
    "Events": events,      # list of strings, e.g. "Roll 1: 7"
    "Outcome": "win" | "loss",
    "Win_amount": win_amount,
}
```

Run it directly for a quick manual demo (3 example rounds, fixed seed 99):

```bash
python Craps.py
```

## Simulator — `Simulator.py`

```python
def simulate(num_simulations, bet, seed=None) -> dict
```

Runs `Craps` `num_simulations` times with the given `bet`, accumulating the
total amount bet and won, and returns:

```python
{
    "RTP": ...,                          # total_win / total_bet
    "Number of simulations": ...,
    "Number of Wins": ...,
    "Total Bet": ...,
    "Win amount": ...,
    "Average numbers of rolls": ...,     # average events (rolls) per round
    "Observed win probability": ...,     # wins / num_simulations
}
```

### Running the simulator

```bash
python Simulator.py
```

This is **interactive** — it will prompt you for three values:

```
Input numbers of Simulations:
Input Bet:
Input seed:
```

Press **Enter without typing anything** to accept the default for any
field:

| Prompt | Default if left empty |
|---|---|
| Number of simulations | `100000` |
| Bet | `10` |
| Seed | `None` (unseeded — a different random sequence every run) |



## Running the tests

From the project root:

```bash
python -m pytest
```



The suite has 26 tests covering:
- **`test_Craps.py`** — result structure, payout correctness, all come-out
  outcomes (7/11 win, 2/3/12 loss), the point-established roll loop, exact
  event log content, and reproducibility with a fixed seed.
- **`test_Simulator.py`** — correctness of accumulated statistics (RTP,
  total bet/win, observed win probability), reproducibility with a fixed
  seed, a statistical sanity check against the theoretical RTP (~0.986),
  the `bet=0` edge case, and the `input_default` helper (using
  `monkeypatch` to simulate user input without needing a real terminal).

## Seeding / reproducibility

Both `Craps()` and `simulate()` accept a `random.Random` instance (or a
`seed` in the case of `simulate`). Passing the **same seed** guarantees the
**same sequence** of rolls across runs — useful for verifying results or
debugging. Leaving `seed` empty at the prompt (or passing `None`) uses an
unseeded generator, so each run produces different results.

## Assumptions

- **Payout rule**: a win pays `2×` the bet (net profit = `1×` the bet); a
  loss pays `0`, matching the task's stated rule literally.
- **`Point` field**: on an immediate win/loss (come-out roll of 7, 11, 2, 3,
  or 12), `Point` is set to that come-out sum rather than `None`, since no
  point was ever actually "established" as a target to re-roll for.
- **Reproducibility**: rather than seeding the global `random` module, the
  engine accepts an injected `random.Random` instance, so the simulator can
  seed once and reuse the same generator across all rounds without touching
  global state.
