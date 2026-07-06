import json
import os
import csv

DATA_FOLDER = "cricsheet_data"
OUTPUT_CSV = "sample_matches.csv"

def process_match(filepath, writer):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    info = data.get("info", {})
    match_date = info.get("dates", ["unknown"])[0]
    teams = info.get("teams", ["Team A", "Team B"])

    # Track batting and bowling stats per player for this match
    batting_stats = {}
    bowling_stats = {}

    innings_list = data.get("innings", [])

    for innings in innings_list:
        batting_team = innings.get("team")
        opponent = [t for t in teams if t != batting_team]
        opponent = opponent[0] if opponent else "Unknown"

        overs = innings.get("overs", [])

        for over in overs:
            deliveries = over.get("deliveries", [])
            for delivery in deliveries:
                batter = delivery.get("batter")
                bowler = delivery.get("bowler")
                runs = delivery.get("runs", {})
                batter_runs = runs.get("batter", 0)
                total_runs = runs.get("total", 0)

                # Batting stats
                if batter not in batting_stats:
                    batting_stats[batter] = {
                        "runs": 0, "balls": 0, "opponent": opponent
                    }
                batting_stats[batter]["runs"] += batter_runs
                # Wides don't count as a ball faced
                extras = delivery.get("extras", {})
                if "wides" not in extras:
                    batting_stats[batter]["balls"] += 1

                # Bowling stats
                if bowler not in bowling_stats:
                    bowling_stats[bowler] = {
                        "runs_conceded": 0, "balls": 0, "wickets": 0, "opponent": batting_team
                    }
                bowling_stats[bowler]["runs_conceded"] += total_runs
                if "wides" not in extras and "noballs" not in extras:
                    bowling_stats[bowler]["balls"] += 1

                wickets = delivery.get("wickets", [])
                for w in wickets:
                    bowling_stats[bowler]["wickets"] += 1

    # Write batting rows
    for player, stats in batting_stats.items():
        writer.writerow([
            player, match_date, stats["opponent"],
            stats["runs"], stats["balls"], 0, 0, 0
        ])

    # Write bowling rows (merge with batting where possible, else separate row)
    for player, stats in bowling_stats.items():
        overs_bowled = round(stats["balls"] / 6, 1)
        writer.writerow([
            player, match_date, stats["opponent"],
            0, 0, stats["wickets"], overs_bowled, stats["runs_conceded"]
        ])


def main():
    files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".json")]
    print(f"Found {len(files)} match files.")

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["player", "match_date", "opponent", "runs", "balls", "wickets", "overs", "runs_conceded"])

        count = 0
        for filename in files:
            filepath = os.path.join(DATA_FOLDER, filename)
            try:
                process_match(filepath, writer)
                count += 1
            except Exception as e:
                print(f"Skipped {filename}: {e}")

        print(f"Processed {count} matches successfully.")
        print(f"Output written to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()