import subprocess
import sys


def test_gen_wrappers():
    # Verifies that gen_wrappers can be executed.
    subprocess.check_call([sys.executable,
                           "scripts/gen_wrappers.py", "/tmp/generated_wrappers.pxi"])
