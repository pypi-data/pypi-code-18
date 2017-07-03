import psutil

from dashbase.cli.constants import DASHBASE_PROCESS_PREFIX


def get_dashbase_process(type, name):
    for proc in psutil.process_iter():
        try:
            if proc.name() == "java" and DASHBASE_PROCESS_PREFIX in " ".join(proc.cmdline()):
                cmd = proc.cmdline()
                process_type = cmd[1].split("-")[2]
                process_name = "-".join(cmd[1].split("-")[3:])
                if name == process_name and type == process_type:
                    return proc

        except psutil.NoSuchProcess:
            pass

    return None


def get_process_env(pid):
    if not psutil.pid_exists(pid):
        raise psutil.NoSuchProcess
    proc = psutil.Process(pid)
    return proc.environ()
