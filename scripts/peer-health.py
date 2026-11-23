#!/usr/bin/env python3
"""Read-only, privacy-safe WireGuard handshake audit."""
import subprocess
import sys
import time

interface = sys.argv[1] if len(sys.argv) > 1 else "wg0"
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
        if age <= 180:
            recent += 1
    print(f"Peer {peers}: {status}")
print(f"Total peers: {peers}")
print(f"Handshakes within 180 seconds: {recent}")
print("Peer keys and endpoints intentionally omitted")
