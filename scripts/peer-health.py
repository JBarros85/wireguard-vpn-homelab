#!/usr/bin/env python3
"""Read-only, privacy-safe WireGuard handshake audit."""
import argparse
import subprocess
import sys
import time

parser = argparse.ArgumentParser(description="Privacy-safe WireGuard peer check")
parser.add_argument("interface", nargs="?", default="wg0")
parser.add_argument("--recent-seconds", type=int, default=180)
parser.add_argument("--require-recent", action="store_true")
args = parser.parse_args()
if not 1 <= args.recent_seconds <= 86400:
    parser.error("--recent-seconds must be between 1 and 86400")
interface = args.interface
result = subprocess.run(["wg", "show", interface, "latest-handshakes"], capture_output=True, text=True)
if result.returncode:
    sys.exit("ERROR: unable to read WireGuard handshake state")
now = int(time.time())
peers = 0
recent = 0
for line in result.stdout.splitlines():
    fields = line.split()
    if len(fields) != 2:
        continue
    peers += 1
    try:
        timestamp = int(fields[1])
    except ValueError:
        sys.exit("ERROR: invalid handshake timestamp")
    if timestamp == 0:
        status = "never recorded"
    elif timestamp > now:
        status = "clock mismatch"
    else:
        age = now - timestamp
        status = f"{age // 60} minutes ago"
        if age <= args.recent_seconds:
            recent += 1
    print(f"Peer {peers}: {status}")
print(f"Total peers: {peers}")
print(f"Handshakes within {args.recent_seconds} seconds: {recent}")
if args.require_recent and recent == 0:
    sys.exit(2)
print("Peer keys and endpoints intentionally omitted")
