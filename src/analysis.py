"""Coffee cart sales analysis: reproducible version of messy_analysis.ipynb.

Run from the repository root with:
    python src/analysis.py

Reads data/raw/coffee_sales.csv (never modified) and writes all results to output/.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # draw charts without needing a screen, so it runs anywhere
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

# --- Paths: built relative to this file, so they work on any machine -----------
ROOT = Path(__file__).resolve().parent.parent
RAW_DATA = ROOT / "data" / "raw" / "coffee_sales.csv"
OUTPUT_DIR = ROOT / "output"

# --- Fixed random seed, so the "random" split is the same on every run ----------
SEED = 42


def load_data(path: Path) -> pd.DataFrame:
    """Load the raw sales data and add a revenue column."""
    df = pd.read_csv(path)
    df["revenue"] = df["quantity"] * df["unit_price"]
    return df


def daily_revenue(df: pd.DataFrame) -> pd.Series:
    """Total revenue for each date."""
    return df.groupby("date")["revenue"].sum()


def random_day_split(daily: pd.Series, seed: int) -> tuple[pd.Series, pd.Series]:
    """Randomly split the DAYS 50/50 (seeded), as the original heading intended."""
    rng = np.random.default_rng(seed)
    days = daily.index.to_numpy()
    shuffled = rng.permutation(days)
    half = len(shuffled) // 2
    group_a_days = sorted(shuffled[:half])
    group_b_days = sorted(shuffled[half:])
    return daily.loc[group_a_days], daily.loc[group_b_days]


def revenue_by_product(df: pd.DataFrame) -> pd.Series:
    """Total revenue for each product, highest first."""
    return df.groupby("product")["revenue"].sum().sort_values(ascending=False)


def save_bar_chart(by_product: pd.Series, path: Path) -> None:
    """Save the revenue-by-product bar chart."""
    fig, ax = plt.subplots(figsize=(6, 4))
    by_product.plot(kind="bar", ax=ax)
    ax.set_ylabel("Total revenue ($)")
    ax.set_title("Revenue by product")
    fig.tight_layout()
    # Removing the "Software" tag keeps the PNG identical across runs
    fig.savefig(path, dpi=100, metadata={"Software": None})
    plt.close(fig)


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    df = load_data(RAW_DATA)

    daily = daily_revenue(df)
    avg_daily = daily.mean()

    group_a, group_b = random_day_split(daily, SEED)

    by_product = revenue_by_product(df)
    top_product = by_product.index[0]

    # --- Save results -----------------------------------------------------------
    daily.to_csv(OUTPUT_DIR / "daily_revenue.csv", header=["revenue"])
    by_product.to_csv(OUTPUT_DIR / "revenue_by_product.csv", header=["revenue"])
    save_bar_chart(by_product, OUTPUT_DIR / "revenue_by_product.png")

    first_day, last_day = daily.index.min(), daily.index.max()
    summary_lines = [
        "Coffee Cart Sales Analysis",
        f"Data covers {len(daily)} days: {first_day} to {last_day}",
        "",
        f"Average daily revenue: ${avg_daily:.2f}",
        "",
        f"Random 50/50 split of the days (seed={SEED}):",
        f"  Group A days: {', '.join(group_a.index)}",
        f"  Group A mean daily revenue: ${group_a.mean():.2f}",
        f"  Group B days: {', '.join(group_b.index)}",
        f"  Group B mean daily revenue: ${group_b.mean():.2f}",
        "",
        "Total revenue by product:",
        *[f"  {product}: ${revenue:.2f}" for product, revenue in by_product.items()],
        "",
        f"Takeaway: {top_product} brings in the most total revenue over these "
        f"{len(daily)} days.",
    ]
    summary = "\n".join(summary_lines) + "\n"
    (OUTPUT_DIR / "summary.txt").write_text(summary, encoding="utf-8")

    print(summary)
    print(f"Results written to {OUTPUT_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
