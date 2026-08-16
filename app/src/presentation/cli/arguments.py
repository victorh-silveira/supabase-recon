"""CLI argument parsing for Supabase Recon Analyzer."""

import argparse


def parse_args() -> argparse.Namespace:
    """Parse and return command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Analyzes Lovable/Supabase app, generates swagger.yaml and tests endpoints",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python run.py --url https://application.lovable.app\n"
            "  python run.py --url https://application.lovable.app --skip-download\n"
            "  python run.py --url https://application.lovable.app --no-test\n"
            "  python run.py --url https://application.lovable.app --methods get,post"
        ),
    )
    parser.add_argument("--url", required=True, help="Target Application URL (e.g. https://myapp.lovable.app)")
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Skip downloading assets if the output folder already exists",
    )
    parser.add_argument("--no-test", action="store_true", help="Skip the endpoint reliability testing phase")
    parser.add_argument(
        "--methods",
        default="get,post",
        help="Comma-separated HTTP methods to test (default: get,post)",
    )
    return parser.parse_args()
