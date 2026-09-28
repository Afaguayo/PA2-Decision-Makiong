# Connect Four: Monte Carlo Search Agents

Three Connect Four agents compared head-to-head, for a Decision Making course (Programming Assignment 2, fall 2024):

| Agent | How it picks a move |
|---|---|
| **UR** (Uniform Random) | Any legal column, at random. The baseline. |
| **PMCGS** (Pure Monte Carlo Game Search) | Plays many random games to the end, then picks the first move with the best average result. |
| **UCT** (Upper Confidence bounds for Trees) | Monte Carlo tree search that balances promising moves against unexplored ones using the UCB1 formula, `win rate + c·√(ln N / n)` with `c = √2`. |

## Run it

No packages needed, just Python 3.

**Pick a move for one position:**

```bash
python3 connectFour.py test_UCT.txt Verbose 500
#                      <board file>  <None|Brief|Verbose>  <simulations>
```

A board file names the algorithm, the player to move (`R` or `Y`), then the 6×7 board from the top row down (`O` = empty):

```text
UCT
R
OOOOOOO
OOOOOOO
OOYOOOY
OOROOOY
OYRYOYR
YRRYORR
```

`Verbose` prints the running win and visit counts (PMCGS) or the UCB value of each column (UCT) as the search goes, then the chosen column. Sample boards: `test_UR.txt`, `test_PMCGS.txt`, `test_UCT.txt`, `test2.txt`.

**Run the tournament:**

```bash
python3 connectFour.py
```

Every agent plays every other one (UR, PMCGS with 100 and 200 simulations, UCT with 100 and 200) over 100 rounds, and it prints wins, losses and draws for each pairing.

## Results

From [`tournamentResults.txt`](tournamentResults.txt), 200 games per pairing:

| | vs UR | vs PMCGS (100) | vs PMCGS (200) | vs UCT (100) | vs UCT (200) |
|---|---|---|---|---|---|
| **UR** | | 2–198 | 2–198 | 10–190 | 18–182 |
| **PMCGS (100)** | 198–2 | | 86–108 (6 draws) | 167–33 | 179–21 |
| **PMCGS (200)** | 198–2 | 108–86 (6 draws) | | 182–18 | 182–18 |
| **UCT (100)** | 190–10 | 33–167 | 18–182 | | 100–100 |

Both search agents crush random play, and more simulations help (PMCGS 200 beats PMCGS 100). In this run, PMCGS also beat UCT at the same budget. The write-up is in `PA2 Report.docx`.
