'''
Cricket Player Performance analyzer 

This program generates each-player performance statistics by processing ball-by-ball match summeries (collected per innings) for 
cricket players. The input data is provided in CSV format, with Player Name, Runs, Balls, and Match Number on each line. Total runs, 
total balls played, number of innings, batting average, strike rate, best snumber of 50s, 100s, and also 0 scores are all calculated 
by the analyzer, which combines multiple matches per player. The user can search for a specific player's detailed record, view the top 
N players by total runs or strike rate, request a complete report of all players, and write a detailed summery to an output file. 

This problem is exact: interactive searches and submission file output are supported, the input format is specified, and the 
putputs are calculated systematically. Conditions, sequences, loops (for and while), functions, tuple/list/string operations, 
user input handing, and file I/O are all demonstrated in the applications. 
'''
# This program reads a CSV input file (match.csv) with lines of the form: 
#    Playername, Runs, Balls, MatchNumber
# Example:
#    Srikshitha, 45, 38, 1
#    Srikshitha, 72, 60, 2

# For each player the program will:
#    - total balls and runs in all games
#    - count innings, dot balls (0), 50s and 100s 
#    - compute batting average (runs / innings) 
#    - compute strike rate (runs * 100 / balls) when balls > 0 
#    - it will find the highest score 

# The program also demonstrates: 
#    - function calls and calculations
#    - using if, elif, and else to branch
#    - sequence operations on string, lists, and tuples
#    - for loop for understanding lists and repeated sequences
#    - while loop for a straightforward responsive display
#    - simplifying user-defined functions
#    - writing a full output file afer receiving from a file 

# ====================



import sys         # Importing namespaces (sys used if we want to exit early)
from typing import Dict, List, Tuple  # For type hints (clarity)

# Configurable filenames (change if you want)
INPUT_FILENAME = "cps109_a1_input.txt"
OUTPUT_FILENAME = "Cricket_Player_Performance_Analyzer_output.txt"

# Data structures:
# players: Dict[str, List[Tuple[int, int, int]]]
# mapping player name -> list of tuples (runs, balls, match_number)
players: Dict[str, List[Tuple[int, int, int]]] = {}

# -------------------- Helper functions --------------------

def parse_line(line: str) -> Tuple[str, int, int, int]:
    """
    Parse a CSV line of the form:
      PlayerName, Runs, Balls, MatchNumber
    and return (player_name, runs, balls, match_number)
    Raises ValueError on malformed data.
    """
    # Strip and split by comma
    parts = [p.strip() for p in line.strip().split(',')]
    if len(parts) != 4:
        raise ValueError(f"Expected 4 fields, got {len(parts)}: {line!r}")
    name = parts[0]
    # Convert numeric fields and validate
    try:
        runs = int(parts[1])
        balls = int(parts[2])
        match_no = int(parts[3])
    except ValueError as e:
        raise ValueError(f"Numeric conversion failed for line: {line!r}") from e
    if runs < 0 or balls < 0 or match_no < 0:
        raise ValueError(f"Negative values not allowed: {line!r}")
    return (name, runs, balls, match_no)

def add_record(player_dict: Dict[str, List[Tuple[int,int,int]]],
               record: Tuple[str,int,int,int]) -> None:
    """
    Add a single parsed record to the players dictionary.
    record is (name, runs, balls, match_no)
    """
    name, runs, balls, match_no = record
    # Initialize list if first time seeing player
    if name not in player_dict:
        player_dict[name] = []
    player_dict[name].append((runs, balls, match_no))

def compute_player_stats(records: List[Tuple[int,int,int]]) -> Dict[str, float]:
    """
    Given a list of records for a single player (runs, balls, match_no),
    return a stats dictionary containing:
      - innings, total_runs, total_balls, average, strike_rate,
      - fifties, hundreds, highest_score, ducks
    """
    innings = len(records)
    total_runs = sum(r for (r, b, m) in records)
    total_balls = sum(b for (r, b, m) in records)
    highest_score = max((r for (r, b, m) in records), default=0)
    ducks = sum(1 for (r, b, m) in records if r == 0)
    fifties = sum(1 for (r, b, m) in records if 50 <= r < 100)
    hundreds = sum(1 for (r, b, m) in records if r >= 100)

    # Batting average: runs / innings (assuming out each innings)
    average = (total_runs / innings) if innings > 0 else 0.0

    # Strike rate: runs per 100 balls
    strike_rate = (total_runs * 100.0 / total_balls) if total_balls > 0 else 0.0

    return {
        'innings': innings,
        'total_runs': total_runs,
        'total_balls': total_balls,
        'average': average,
        'strike_rate': strike_rate,
        'fifties': fifties,
        'hundreds': hundreds,
        'highest_score': highest_score,
        'ducks': ducks
    }

def build_all_stats(player_dict: Dict[str, List[Tuple[int,int,int]]]) -> Dict[str, Dict[str,float]]:
    """
    Compute stats for every player and return a mapping
    player -> stats_dict
    """
    stats = {}
    for player, recs in player_dict.items():
        stats[player] = compute_player_stats(recs)
    return stats

def format_player_summary(name: str, stats: Dict[str,float]) -> str:
    """
    Return a readable one-line summary for a player.
    """
    return (f"{name}: Runs={stats['total_runs']}, Balls={stats['total_balls']}, "
            f"Innings={stats['innings']}, Avg={stats['average']:.2f}, SR={stats['strike_rate']:.2f}, "
            f"Ht={stats['highest_score']}, 50s={stats['fifties']}, 100s={stats['hundreds']}, Ducks={stats['ducks']}")

def write_report(filename: str, stats_map: Dict[str, Dict[str,float]]) -> None:
    """
    Write a detailed report to filename. The report lists each player's stats,
    sorted by total runs descending.
    """
    # Sort players by total_runs descending
    sorted_players = sorted(stats_map.items(), key=lambda kv: kv[1]['total_runs'], reverse=True)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Cricket Player Performance Analyzer - Detailed Report\n")
        f.write("----------------------------------------------------\n\n")
        f.write(f"Total players: {len(sorted_players)}\n\n")
        for name, st in sorted_players:
            f.write(format_player_summary(name, st) + "\n")
        # Provide some top-N summaries
        f.write("\nTop 5 by Runs:\n")
        for (name, st) in sorted_players[:5]:
            f.write(f"  {name} - {st['total_runs']} runs, Avg {st['average']:.2f}, SR {st['strike_rate']:.2f}\n")
    print(f"Report written to {filename}")

# -------------------- File reading and main logic --------------------

def load_input_file(filename: str, player_dict: Dict[str, List[Tuple[int,int,int]]]) -> List[str]:
    """
    Read the input file and populate player_dict. Returns a list of malformed lines encountered.
    """
    errors = []
    try:
        with open(filename, 'r', encoding='utf-8') as fh:
            for lineno, line in enumerate(fh, start=1):
                # Skip blank lines
                if not line.strip():
                    continue
                try:
                    rec = parse_line(line)
                    add_record(player_dict, rec)
                except ValueError as e:
                    # Record the error but continue procesing
                    errors.append(f"Line {lineno}: {e}")
    except FileNotFoundError:
        print(f"Input file '{filename}' not found. Please ensure it exists in the current directory.")
        sys.exit(1)
    return errors

def show_top_n(stats_map: Dict[str, Dict[str,float]], key: str, n: int=5) -> None:
    """
    Show top-n players sorted by stats_map[player][key] descending.
    Valid keys: 'total_runs', 'average', 'strike_rate', 'highest_score'
    """
    if key not in ('total_runs', 'average', 'strike_rate', 'highest_score'):
        print("Invalid sort key. Choose from total_runs, average, strike_rate, highest_score.")
        return
    sorted_players = sorted(stats_map.items(), key=lambda kv: kv[1][key], reverse=True)
    print(f"\nTop {n} players by {key.replace('_', ' ')}:")
    for i, (name, st) in enumerate(sorted_players[:n], start=1):
        print(f" {i}. {format_player_summary(name, st)}")

def interactive_menu(stats_map: Dict[str, Dict[str,float]]) -> None:
    """
    Simple interactive menu loop allowing the user to:
      - view all players
      - view top N by a key
      - search for a player
      - write report to file
      - quit
    Demonstrates use of a while loop and conditions.
    """
    prompt = ("\nMenu:\n"
              "  1 - Show all player summaries\n"
              "  2 - Show top N players by a metric (runs/avg/sr/hs)\n"
              "  3 - Search for a player\n"
              "  4 - Write full report to file\n"
              "  5 - Quit\n"
              "Enter choice (1-5): ")
    while True:
        choice = input(prompt).strip()
        if choice == '1':
            # Print all players sorted by name
            for name in sorted(stats_map.keys()):
                print(format_player_summary(name, stats_map[name]))
        elif choice == '2':
            try:
                metric = input("Metric (runs/avg/sr/hs) default runs: ").strip().lower() or 'runs'
                key_map = {'runs': 'total_runs', 'avg': 'average', 'sr': 'strike_rate', 'hs': 'highest_score'}
                key = key_map.get(metric, 'total_runs')
                n_str = input("How many top players to show? [default 5]: ").strip()
                n = int(n_str) if n_str else 5
                show_top_n(stats_map, key, n)
            except ValueError:
                print("Invalid number for N. Try again.")
        elif choice == '3':
            query = input("Enter player name to search (case sensitive): ").strip()
            if query in stats_map:
                print(format_player_summary(query, stats_map[query]))
                # show per-innings breakdown as an example of additional info
                print("Per-innings breakdown (most recent first):")
                # We need access to the original records for this; we reconstruct from global players dict
                recs = players.get(query, [])
                # Sort records by match number descending
                recs_sorted = sorted(recs, key=lambda t: t[2], reverse=True)
                for (r, b, m) in recs_sorted:
                    print(f"  Match {m}: Runs={r}, Balls={b}, SR={(r*100.0/b) if b>0 else 0.0:.2f}")
            else:
                # Provide fuzy-ish suggestions using simple substring search
                suggestions = [p for p in stats_map.keys() if query.lower() in p.lower()]
                if suggestions:
                    print("No exact match. Did you mean:")
                    for s in suggestions:
                        print("  -", s)
                else:
                    print("Player not found.")
        elif choice == '4':
            write_report(OUTPUT_FILENAME, stats_map)
        elif choice == '5':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

# -------------------- Program entry point --------------------

def main() -> None:
    """
    Main function: load data, compute stats, interact with user.
    """
    print("Cricket Player Performance Analyzer")
    print("Loading data from", INPUT_FILENAME)
    # Load input file and populate players dict
    errors = load_input_file(INPUT_FILENAME, players)

    if errors:
        print("Some lines in the input file were malformed and skipped:")
        for err in errors:
            print(" ", err)

    # Build statistics for all players
    stats_map = build_all_stats(players)

    # Print a concise summary to the terminal
    print("\nSummary of players loaded:", len(stats_map))
    # Show top 5 by runs automaticaly
    if stats_map:
        show_top_n(stats_map, 'total_runs', 5)
    else:
        print("No player data found in the input file. Exiting.")
        return

    # Write initial report automatically
    write_report(OUTPUT_FILENAME, stats_map)

    # Enter an interactive menu for further user queries
    interactive_menu(stats_map)

# Run the main function when this file is executed
if __name__ == "__main__":
    main()
