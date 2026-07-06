import csv

player_name = input("Enter player name: ")

matches = []

with open("sample_matches.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        if row["player"].lower() == player_name.lower():
            matches.append(row)

if not matches:
    print("No data found for this player.")
else:
    total_runs = sum(int(match["runs"]) for match in matches)
    total_balls = sum(int(match["balls"]) for match in matches)

    average_runs = total_runs / len(matches)
    strike_rate = (total_runs / total_balls) * 100 if total_balls > 0 else 0

    print("\nPlayer:", player_name)
    print("Matches analyzed:", len(matches))
    print("Average runs:", round(average_runs, 2))
    print("Strike rate:", round(strike_rate, 2))

    if average_runs >= 40:
        print("Insight: Good recent batting form.")
    elif average_runs >= 20:
        print("Insight: Average form, needs consistency.")
    else:
        print("Insight: Poor recent form, needs improvement.")