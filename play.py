#!/usr/bin/env python3
"""One-command runner to launch the Murder Mystery Engine CLI."""

import sys
from src.cli import run_interactive_cli, run_demo_simulation

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_demo_simulation()
    else:
        run_interactive_cli()
