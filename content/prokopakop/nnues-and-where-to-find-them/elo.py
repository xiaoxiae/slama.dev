#!/usr/bin/env python3
"""Generate Elo rating visualizations from PGN file."""

import re
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np


def parse_pgn(pgn_path: Path, player: str = "prokopakop") -> dict:
    """Parse PGN file and extract rating history for a player."""
    games = {"bullet": [], "blitz": []}

    with open(pgn_path) as f:
        content = f.read()

    # Split into individual games by double newlines followed by [Event
    game_blocks = re.split(r"\n\n+(?=\[Event)", content)

    for block in game_blocks:
        if not block.strip():
            continue

        # Extract headers
        headers = {}
        for match in re.finditer(r'\[(\w+)\s+"([^"]+)"\]', block):
            headers[match.group(1)] = match.group(2)

        # Skip if not rated or missing data
        event = headers.get("Event", "")
        if "casual" in event.lower():
            continue

        # Determine game type
        time_control = headers.get("TimeControl", "")
        if "bullet" in event.lower():
            game_type = "bullet"
        elif "blitz" in event.lower():
            game_type = "blitz"
        else:
            # Infer from time control (base time in seconds)
            try:
                base_time = int(time_control.split("+")[0])
                if base_time < 180:
                    game_type = "bullet"
                else:
                    game_type = "blitz"
            except (ValueError, IndexError):
                continue

        # Find player's side and rating
        white = headers.get("White", "")
        black = headers.get("Black", "")

        if white == player:
            elo = headers.get("WhiteElo")
            rating_diff = headers.get("WhiteRatingDiff")
        elif black == player:
            elo = headers.get("BlackElo")
            rating_diff = headers.get("BlackRatingDiff")
        else:
            continue

        if not elo or not rating_diff:
            continue

        try:
            elo = int(elo)
            rating_diff = int(rating_diff)
        except ValueError:
            continue

        # Post-game rating = pre-game elo + rating diff
        post_rating = elo + rating_diff

        # Parse timestamp
        utc_date = headers.get("UTCDate", "")
        utc_time = headers.get("UTCTime", "")

        if utc_date and utc_time:
            try:
                timestamp = datetime.strptime(
                    f"{utc_date} {utc_time}", "%Y.%m.%d %H:%M:%S"
                )
            except ValueError:
                continue
        else:
            continue

        games[game_type].append({"timestamp": timestamp, "rating": post_rating})

    # Sort by timestamp (oldest first for plotting)
    for game_type in games:
        games[game_type].sort(key=lambda x: x["timestamp"])

    return games


def smooth(data: list, window: int = 50) -> np.ndarray:
    """Apply exponential moving average smoothing."""
    arr = np.array(data, dtype=float)
    alpha = 2 / (window + 1)
    smoothed = np.zeros_like(arr)
    smoothed[0] = arr[0]
    for i in range(1, len(arr)):
        smoothed[i] = alpha * arr[i] + (1 - alpha) * smoothed[i - 1]
    return smoothed


def create_rating_plot(
    games: list,
    title: str,
    output_path: Path,
    color: str = "#629924",
    annotations: list[tuple[datetime, str]] | None = None,
):
    """Create a Lichess-style rating plot."""
    if not games:
        print(f"No games for {title}, skipping.")
        return

    timestamps = [g["timestamp"] for g in games]
    ratings = [g["rating"] for g in games]

    # Apply smoothing
    smoothed_ratings = smooth(ratings, window=50)

    # Build a lookup for smoothed rating by timestamp
    ts_to_smoothed = dict(zip(timestamps, smoothed_ratings))

    # Create figure with Lichess-like styling
    fig, ax = plt.subplots(figsize=(10, 4))

    # Plot the smoothed rating line
    ax.plot(timestamps, smoothed_ratings, color=color, linewidth=1.5, zorder=3)

    # Fill area under the curve
    ax.fill_between(timestamps, smoothed_ratings, alpha=0.3, color=color, zorder=2)

    # Styling to match Lichess
    ax.set_facecolor("#161512")
    fig.patch.set_facecolor("#161512")

    # Grid
    ax.grid(True, alpha=0.2, color="#ffffff", zorder=1)

    # Axis styling
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_color("#ffffff")
    ax.spines["left"].set_color("#ffffff")
    ax.spines["bottom"].set_alpha(0.3)
    ax.spines["left"].set_alpha(0.3)

    ax.tick_params(colors="#bababa", which="both")

    # Format x-axis dates
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45, ha="right")

    # Labels
    ax.set_ylabel("Rating", color="#bababa", fontsize=10)

    # Title
    ax.set_title(title, color="#bababa", fontsize=12, pad=10)

    # Add current rating annotation
    current_rating = ratings[-1]
    ax.annotate(
        f"{current_rating}",
        xy=(timestamps[-1], current_rating),
        xytext=(5, 0),
        textcoords="offset points",
        color=color,
        fontsize=10,
        fontweight="bold",
        va="center",
    )

    # Set y-axis limits with some padding
    min_rating = min(ratings)
    max_rating = max(ratings)
    padding = (max_rating - min_rating) * 0.25 or 50
    ax.set_ylim(min_rating - padding, max_rating + padding)

    # Add custom annotations
    if annotations:
        for ann_date, ann_text in annotations:
            # Find closest timestamp to annotation date
            closest_ts = min(
                timestamps, key=lambda t: abs((t - ann_date).total_seconds())
            )
            rating_at_point = ts_to_smoothed[closest_ts]

            # Draw vertical line
            ax.axvline(x=ann_date, color="#bababa", linestyle="--", alpha=0.5, zorder=2)

            # Add text annotation at the bottom with horizontal offset
            ax.text(
                ann_date + timedelta(days=2),
                min_rating - padding * 0.8,
                ann_text,
                color="#bababa",
                fontsize=11,
                fontweight="bold",
                ha="left",
                va="bottom",
            )

    plt.tight_layout()
    plt.savefig(
        output_path, format="svg", facecolor="#161512", edgecolor="none", dpi=100
    )
    plt.close()

    print(
        f"Saved {output_path} ({len(games)} games, rating: {ratings[0]} -> {current_rating})"
    )


def main():
    script_dir = Path(__file__).parent
    pgn_path = script_dir / "games.pgn"

    print(f"Parsing {pgn_path}...")
    games = parse_pgn(pgn_path)

    print(
        f"Found {len(games['bullet'])} bullet games, {len(games['blitz'])} blitz games"
    )

    # Annotations to highlight on both charts
    annotations = [
        (datetime(2025, 10, 26, 12), "NNUE added"),
    ]

    # Generate plots
    create_rating_plot(
        games["bullet"],
        "Prokopakop Bullet Rating",
        script_dir / "elo-bullet.svg",
        color="#56b4e9",  # Blue for bullet
        annotations=annotations,
    )

    create_rating_plot(
        games["blitz"],
        "Blitz Rating",
        script_dir / "elo-blitz.svg",
        color="#e69f00",  # Orange for blitz
        annotations=annotations,
    )


if __name__ == "__main__":
    main()
