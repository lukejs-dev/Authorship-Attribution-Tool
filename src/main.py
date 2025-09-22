# src/main.py
import argparse
import sys
import time
from src.analyzer import AuthorshipAnalyzer

def main():
    """Main function to run the command-line interface."""
    parser = argparse.ArgumentParser(
        description="A command-line tool for Discord authorship attribution using stylometry.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--channels',
        type=str,
        required=True,
        help="Path to the directory containing Discord channel export CSVs."
    )
    parser.add_argument(
        '--target',
        type=str,
        required=True,
        help="Path to the directory containing the unknown text file(s) to analyze."
    )
    parser.add_argument(
        '--top-n',
        type=int,
        default=20,
        help="Number of top results to display (default: 20)."
    )

    args = parser.parse_args()
    start_time = time.time()
    
    try:
        analyzer = AuthorshipAnalyzer(channels_dir=args.channels, target_dir=args.target)
        analyzer.run()
        analyzer.display_results(top_n=args.top_n)

    except Exception as e:
        print(f"\n❌ An error occurred: {e}", file=sys.stderr)
        sys.exit(1)
    
    print(f"\n✅ Analysis complete. Total execution time: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()