import subprocess
import glob
import os.path
import pymj
import sys
pymj_root = os.path.dirname(os.path.dirname(pymj.__file__))


def test_examples():
    scripts = glob.glob("%s/examples/*.py" % pymj_root)
    env = os.environ.update({'TESTING': 'true'})
    assert len(scripts) > 0, 'No example scripts found!'
    for tutorial_script in scripts:
        print("Executing %s" % tutorial_script)

        subprocess.check_call([sys.executable, tutorial_script], env=env)
