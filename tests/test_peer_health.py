import io
import runpy
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

SCRIPT = str(Path(__file__).resolve().parents[1] / "scripts/peer-health.py")

class PeerHealthTests(unittest.TestCase):
    def audit(self, data, rc=0):
        out = io.StringIO()
        result = subprocess.CompletedProcess(["wg"], rc, stdout=data)
        with patch.object(sys, "argv", ["peer-health.py"]), patch("subprocess.run", return_value=result), patch("time.time", return_value=1000000), redirect_stdout(out):
            runpy.run_path(SCRIPT, run_name="__main__")
        return out.getvalue()

    def test_recent_and_never(self):
        out = self.audit("FAKEKEY_A\t999940\nFAKEKEY_B\t0\n")
        self.assertIn("Peer 1: 1 minutes ago", out)
        self.assertIn("Peer 2: never recorded", out)
        self.assertIn("Handshakes within 180 seconds: 1", out)
        self.assertNotIn("FAKEKEY_A", out)

    def test_old_and_future(self):
        out = self.audit("FAKEKEY_A\t999600\nFAKEKEY_B\t1000100\n")
        self.assertIn("clock mismatch", out)
        self.assertIn("Handshakes within 180 seconds: 0", out)

    def test_empty(self):
        self.assertIn("Total peers: 0", self.audit(""))

    def test_invalid_timestamp(self):
        with self.assertRaises(SystemExit):
            self.audit("FAKEKEY\tinvalid\n")

    def test_wireguard_failure(self):
        with self.assertRaises(SystemExit):
            self.audit("", rc=1)

if __name__ == "__main__":
    unittest.main()
