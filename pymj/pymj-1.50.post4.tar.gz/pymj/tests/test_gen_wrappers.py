import subprocess


def test_gen_wrappers():
    # Verifies that gen_wrappers can be executed.
    subprocess.check_call(["/usr/bin/env", "python",
                           "scripts/gen_wrappers.py", "/tmp/generated_wrappers.pxi"])


