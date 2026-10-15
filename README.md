# DS5110 Homework 1: Coffee Cart Sales Analysis (reproducible)

A reproducible version of `original_messy_analysis.ipynb`. It reads the raw coffee sales data and reports average daily revenue, a seeded random split of the days, and total revenue by product.

## How to run (one command)

From the repository root, after installing the pinned environment:

```bash
pip install -r requirements.txt
python src/analysis.py
```

The pipeline command is `python src/analysis.py`. On macOS/Linux, `make` does the same thing.

It prints a summary and writes all results to `output/`. Running it again produces the same files.

Tested with Python 3.13 (any Python 3.10–3.13 should work with the pinned versions). Using a virtual environment is recommended:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/analysis.py
```

## Repository layout

```
data/raw/coffee_sales.csv        raw data, never edited
src/analysis.py                  the pipeline (runs top to bottom)
output/                          everything the pipeline produces
  summary.txt                    the results in plain text
  daily_revenue.csv
  revenue_by_product.csv
  revenue_by_product.png
requirements.txt                 pinned library versions
Makefile                         optional shortcut: `make`
original_messy_analysis.ipynb    the notebook as it was handed over, kept for reference
```

## What was wrong with the original notebook, and how it was fixed

1. **Hard-coded absolute paths.** The notebook read from and saved to `/Users/jmwaura/Desktop/analysis/...`, which only exists on one machine. All paths are now built relative to the repository (`data/raw/`, `output/`).
2. **Cells depended on being run out of order.** The cell printing `avg_daily` came *before* the cell that creates it, so a fresh top-to-bottom run crashed with `NameError`. The script now computes everything in order.
3. **Unseeded randomness.** `df.sample(frac=1)` shuffled differently on every run, so the Group A/B numbers changed each time. The split now uses a fixed seed (`SEED = 42`).
4. **The "split of the days" actually split rows.** The heading said it split days, but the code shuffled individual sales rows, scattering one day's sales across both groups. It now splits whole days.
5. **Missing data file.** The notebook depended on `coffee_sales.csv` that wasn't in any repository. It is now committed in `data/raw/`.
6. **No pinned environment.** Library versions are now fixed in `requirements.txt`.
7. **Charts needed a screen.** `plt.show()` was replaced by saving the chart to `output/`, using a non-interactive backend, so it runs anywhere.
8. **Wrong takeaway.** The notebook concluded that Drip Coffee brings in the most revenue. The data shows the opposite: Latte is highest ($697.50) and Drip Coffee is lowest ($396.00). The data also covers 10 days (5–14 Jan 2026), not a full month. The takeaway is now computed from the data rather than typed by hand.

## Results

See `output/summary.txt`. In short: average daily revenue is $158.25, and Latte brings in the most total revenue over the 10 days.

## Verification

The repository was copied into a brand-new folder, the environment was installed from `requirements.txt`, and `python src/analysis.py` was run twice. Both runs produced byte-identical files matching those in `output/`.

## Use of AI

I used an AI assistant (Claude) to help identify the reproducibility problems in the original notebook, write `src/analysis.py`, set up the folder structure, `requirements.txt` and `Makefile`, draft this README, and test the pipeline in a fresh folder. I reviewed every file and can explain each line.
