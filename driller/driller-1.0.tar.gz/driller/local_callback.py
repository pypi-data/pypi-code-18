import os
import sys
import signal
import logging
import driller #pylint:disable=relative-import,unused-import
import subprocess
import multiprocessing

l = logging.getLogger("local_callback")

def _run_drill(drill, fuzz, _path_to_input_to_drill):
    _binary_path = fuzz.binary_path
    _fuzzer_out_dir = fuzz.out_dir
    _bitmap_path = os.path.join(_fuzzer_out_dir, 'fuzzer-master', "fuzz_bitmap")
    _timeout = drill._worker_timeout
    l.warning("starting drilling of %s, %s", os.path.basename(_binary_path), os.path.basename(_path_to_input_to_drill))
    args = (
        "timeout", "-k", str(_timeout+10), str(_timeout),
        sys.executable, os.path.abspath(__file__),
        _binary_path, _fuzzer_out_dir, _bitmap_path, _path_to_input_to_drill
    )

    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    print p.communicate()


class LocalCallback(object):
    def __init__(self, num_workers=1, worker_timeout=10*60):
        self._already_drilled_inputs = set()

        self._num_workers = num_workers
        self._running_workers = []
        self._worker_timeout = worker_timeout

    @staticmethod
    def _queue_files(fuzz, fuzzer='fuzzer-master'):
        '''
        retrieve the current queue of inputs from a fuzzer
        :return: a list of strings which represent a fuzzer's queue
        '''

        queue_path = os.path.join(fuzz.out_dir, fuzzer, 'queue')
        queue_files = filter(lambda x: x != ".state", os.listdir(queue_path))
        queue_files = [os.path.join(queue_path, q) for q in queue_files]

        return queue_files

    def driller_callback(self, fuzz):
        l.warning("Driller stuck callback triggered!")
        # remove any workers that aren't running
        self._running_workers = [x for x in self._running_workers if x.is_alive()]

        # get the files in queue
        queue = self._queue_files(fuzz)
        #for i in range(1, fuzz.fuzz_id):
        #    fname = "fuzzer-%d" % i
        #    queue.extend(self.queue_files(fname))

        # start drilling
        not_drilled = set(queue) - self._already_drilled_inputs
        if len(not_drilled) == 0:
            l.warning("no inputs left to drill")

        while len(self._running_workers) < self._num_workers and len(not_drilled) > 0:
            to_drill_path = list(not_drilled)[0]
            not_drilled.remove(to_drill_path)
            self._already_drilled_inputs.add(to_drill_path)

            proc = multiprocessing.Process(target=_run_drill, args=(self, fuzz, to_drill_path))
            proc.start()
            self._running_workers.append(proc)
    __call__ = driller_callback

    def kill(self):
        for p in self._running_workers:
            try:
                p.terminate()
                os.kill(p.pid, signal.SIGKILL)
            except OSError:
                pass

# this is for running with bash timeout
if __name__ == "__main__":
    if len(sys.argv) != 5:
        l.error("INTERNAL USE ONLY -- expecting 5 arguments for driller runner, got %d", len(sys.argv))

    binary_path, fuzzer_out_dir, bitmap_path, path_to_input_to_drill = sys.argv[1:5]

    fuzzer_bitmap = open(bitmap_path, "r").read()

    # create a folder
    driller_dir = os.path.join(fuzzer_out_dir, "driller")
    driller_queue_dir = os.path.join(driller_dir, "queue")
    try: os.mkdir(driller_dir)
    except OSError: pass
    try: os.mkdir(driller_queue_dir)
    except OSError: pass

    # get the input
    input_to_drill = open(path_to_input_to_drill, "r").read()

    d = driller.Driller(binary_path, input_to_drill, fuzzer_bitmap)
    count = 0
    for new_input in d.drill_generator():
        id_num = len(os.listdir(driller_queue_dir))
        fuzzer_from = path_to_input_to_drill.split("sync/")[1].split("/")[0] + path_to_input_to_drill.split("id:")[1].split(",")[0]
        filepath = "id:" + ("%d" % id_num).rjust(6, "0") + ",from:" + fuzzer_from
        filepath = os.path.join(driller_queue_dir, filepath)
        with open(filepath, "wb") as f:
            f.write(new_input[1])
        count += 1
    l.warning("found %d new inputs", count)
