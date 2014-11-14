import os
import sys
import subprocess
import json
import time

#from PIL import Image


# Current script's directory used to store captures
WORKING_DIR = os.path.dirname(os.path.realpath(__file__))


def log(msg):
    """Output log message to stderr, as stdout is reserved for data communication"""
    sys.stderr.write("[%s]: %s\n" % (__file__, msg))


def out(msg):
    """Output log message to stdout"""
    sys.stdout.write("%s\n" % msg)


def main():
    """Main entry point"""

    log("Agent started")

    while(True):
        command = "cd %s && ls -1 | wc -l" % WORKING_DIR
        output = subprocess.check_output(command, shell=True).replace(" ", "").replace("\n", "")
        data = dict(name="Test", output=output, ts=int(time.time()))
        log("Fake data: %r" % data)
        out(json.dumps(data))
        sys.stdout.flush()
        time.sleep(3)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        log("Agent exit")
