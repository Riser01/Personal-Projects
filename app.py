#!/usr/bin/env python3
"""One-command runner to launch the Murder Mystery Engine Web Arena."""

import uvicorn

if __name__ == "__main__":
    print("\n🕵️ Launching Murder Mystery Engine Web Arena...")
    print("👉 Open your browser at http://127.0.0.1:8000\n")
    uvicorn.run("src.server:app", host="127.0.0.1", port=8000, reload=False)
