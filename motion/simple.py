import argparse
import os
import sys
import StringIO
import subprocess
import json
import datetime
import time

from PIL import Image


# Current script's directory used to store captures
WORKING_DIR = os.path.dirname(os.path.realpath(__file__))

# File path to store currently captured image
CURRENT_CAPTURE = os.path.join(WORKING_DIR, "current.jpg")


def log(msg):
    """Output log message to stderr, as stdout is reserved for data communication"""
    sys.stderr.write("[%s]: %s\n" % (__file__, msg))


def out(msg):
    """Output log message to stdout"""
    sys.stdout.write("%s\n" % msg)


def find_program(program):
    """Checks if the program is installed and is executable"""
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def capture_test_image(args):
    """Performs guessing of the operating system/tools and forwards the call"""
    uname = os.uname()[0].lower()
    if uname == 'darwin':
        return darwin_capture_test_image(args)
    elif uname == 'windows':
        return windows_capture_test_image(args)
    else:
        raspistill = find_program("raspistill")
        if raspistill:
            return raspberry_capture_test_image(args)
        linux_capture_test_image(args)


def darwin_capture_test_image(args):
    os.system("imagesnap -q -d \"%s\" %s" % (args.deviceName, CURRENT_CAPTURE))
    os.system("convert -resize 100x75\! %s %s" %
              (CURRENT_CAPTURE, CURRENT_CAPTURE))
    im = Image.open(CURRENT_CAPTURE)
    buffer = im.load()
    return im, buffer


def raspberry_capture_test_image(args):
    command = "raspistill -w %s -h %s -t 0 -e bmp -o -" % (100, 75)
    imageData = StringIO.StringIO()
    imageData.write(subprocess.check_output(command, shell=True))
    imageData.seek(0)
    im = Image.open(imageData)
    buffer = im.load()
    imageData.close()
    return im, buffer


def linux_capture_test_image(args):
    raise NotImplementedError, "Linux support is not available yet"


def windows_capture_test_image(args):
    raise NotImplementedError, "Windows support is not available yet"


def save_image(args, width, height, diskSpaceToReserve):
    """Save a full size image to disk"""
    keep_disk_space_free(args.diskSpaceToReserve)
    time = datetime.datetime.now()
    filename = "%s/capture-%04d%02d%02d-%02d%02d%02d.jpg" % (
        WORKING_DIR, time.year, time.month, time.day, time.hour, time.minute, time.second)

    uname = os.uname()[0].lower()
    if uname == 'darwin':
        os.system("cp %s %s" % (CURRENT_CAPTURE, filename))
        log("Captured %s" % filename)
    elif uname == 'windows':
        raise NotImplementedError, "Windows support is not available yet"
    else:
        raspistill = find_program("raspistill")
        if raspistill:
            subprocess.call(
                "raspistill -w 1296 -h 972 -t 0 -e jpg -q 15 -o %s" % filename, shell=True)
            log("Captured %s" % filename)
            return
        raise NotImplementedError, "Linux support is not available yet"


def keep_disk_space_free(bytesToReserve):
    """Clean up the directory"""
    if (get_free_space() < bytesToReserve):
        for filename in sorted(os.listdir(WORKING_DIR)):
            if filename.startswith("capture") and filename.endswith(".jpg"):
                os.remove(filename)
                log("Deleted %s to avoid filling disk" % filename)
                if (get_free_space() > bytesToReserve):
                    return


def get_free_space():
    """Get available disk space"""
    st = os.statvfs(WORKING_DIR)
    du = st.f_bavail * st.f_frsize
    return du


class DateTimeEncoder(json.JSONEncoder):

    """Custom JSON encoder to serialize datetime in ISO format"""

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        else:
            return super(DateTimeEncoder, self).default(obj)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Perform simple movement detection')
    parser.add_argument('--deviceName',
                        dest='deviceName',
                        action='store',
                        default="",
                        help='video device name (if required)')
    parser.add_argument('--threshold',
                        dest='threshold',
                        action='store',
                        default=10,
                        help='how much a pixel has to change by to be marked as "changed"')
    parser.add_argument('--sensitivity',
                        dest='sensitivity',
                        action='store',
                        default=20,
                        help='how many changed pixels before capturing an image')
    parser.add_argument('--forceCapture',
                        dest='forceCapture',
                        action='store',
                        default=True,
                        help='whether to force an image to be captured every forceCaptureTime seconds')
    parser.add_argument('--forceCaptureTime',
                        dest='forceCaptureTime',
                        action='store',
                        default=3600,
                        help='interval for the force capturing of an image')

    parser.add_argument('--saveSnapshots',
                        dest='saveSnapshots',
                        action='store',
                        default=False,
                        help='interval for the force capturing of an image')
    parser.add_argument('--saveWidth',
                        dest='saveWidth',
                        action='store',
                        default=1280,
                        help='width of the captured image to store')
    parser.add_argument('--saveHeight',
                        dest='saveHeight',
                        action='store',
                        default=960,
                        help='height of the captured image to store')
    parser.add_argument('--diskSpaceToReserve',
                        dest='diskSpaceToReserve',
                        action='store',
                        default=(40 * 1024 * 1024),  # Keep 40 mb free on disk
                        help='disk space for storing captured images if enabled')

    args = parser.parse_args()

    log("Agent started")

    # Get first image
    image1, buffer1 = capture_test_image(args)

    # Reset last capture time
    lastCapture = time.time()

    while(True):
        # Get comparison image
        image2, buffer2 = capture_test_image(args)

        # Count changed pixels
        changedPixels = 0
        for x in xrange(0, 100):
            for y in xrange(0, 75):
                # Just check green channel as it's the highest quality channel
                pixdiff = abs(buffer1[x, y][1] - buffer2[x, y][1])
                if pixdiff > args.threshold:
                    changedPixels += 1

        # Check force capture
        if args.forceCapture:
            if time.time() - lastCapture > args.forceCaptureTime:
                changedPixels = args.sensitivity + 1

        # Save an image if pixels changed
        log("Pixels changed: %s, Sensitivity: %s" %
            (changedPixels, args.sensitivity))
        if changedPixels > args.sensitivity:
            lastCapture = time.time()
            if args.saveSnapshots:
                save_image(
                    args, saveWidth, saveHeight, args.diskSpaceToReserve)
            out(DateTimeEncoder().encode(
                dict(movement=True, measured=datetime.datetime.now())))

        # Swap comparison buffers
        image1 = image2
        buffer1 = buffer2

        time.sleep(3)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        log("Agent exit")
