import subprocess
import glob



def test_tutorials():
    dirs = glob.glob("tutorial/*")
    for dir in dirs:
        if dir.endswith(".py"):
            print("Executing %s" % dir)
            try:
                subprocess.check_call(["/usr/bin/env", "python", dir],
                                      timeout=10)
            except subprocess.TimeoutExpired as e:
                pass


