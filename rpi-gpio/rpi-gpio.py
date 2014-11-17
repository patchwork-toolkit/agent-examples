import sys
import time
import json
import argparse
import RPi.GPIO as io
 
def read(pin, name, freq, senml):
    while True:
        ts = int(time.mktime(time.gmtime()))
        try:
            bv = False
            if io.input(pin):
                bv = True

            if senml:
                print json.dumps({"bt": ts, "e": [{"n": name, "bv": bv}]})
            else:
                print bv
            sys.stdout.flush()
        except:
            pass
        time.sleep(freq)

def setup(pin, pull_up, pull_down):
    io.setmode(io.BCM)

    if pull_up:
        io.setup(pin, io.IN, pull_up_down=io.PUD_UP)
    elif pull_down:
        io.setup(pin, io.IN, pull_up_down=io.PUD_DOWN)
    else:
        io.setup(pin, io.IN)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pin", help="GPIO pin (BCM) to read data from", type=int)
    parser.add_argument("-j", "--json", help="Output in SenML", type=bool)
    parser.add_argument("-f", "--freq", help="Pulling frequency, msec", type=int)
    parser.add_argument("-n", "--name", help="Sensor name (URI) for SenML output", type=str)
    parser.add_argument("--pull_up", dest="pull_up", help="Whether to create an internal pull up resistor", type=bool)
    parser.add_argument("--pull_down", dest="pull_down", help="Whether to create an internal pull down resistor", type=bool)
    parser.set_defaults(freq=1000)
    parser.set_defaults(pull_up=False)
    parser.set_defaults(pull_down=False)

    args = parser.parse_args()

    if args.freq <= 0:
        print "freq should be >= 0"
        sys.exit(1)
    freq = args.freq / 1000.0

    setup(args.pin, args.pull_up, args.pull_down)
    read(args.pin, args.name, freq, args.json)