import os
import time
from smp4.core.mp_utils import get_sims_documents_directory

DEBUG_MODE = True
FORCE_RETURN = False

class Timer():
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.t1 = time.time()

    def __exit__(self, *args):
        self.t2 = time.time()
        if (self.t2 - self.t1) * 1000 > 0:
            debug_log(self.name, "time: {}".format((self.t2 - self.t1) * 1000))




def debug_log(filename, string, force=False):
    global DEBUG_MODE
    global FORCE_RETURN
    if FORCE_RETURN:
        return

    if DEBUG_MODE is False and force is False:
        return

    if filename == "locks":
        return

    logs_directory = "{}smp4_logs/".format(get_sims_documents_directory())

    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)

    with open("{}{}.txt".format(logs_directory, filename), 'a') as stream:
        stream.write("{} - {}".format(time.ctime(), str(string) + "\n"))
