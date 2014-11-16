## Raspberry Pi GPIO agent

This agent pulls GPIO pin on a Raspberry Pi and outputs its state either as a simple bool, or as a JSON/SenML.

### Prerequisites

The agent code uses the [Adafruit library code for Raspberry Pi](https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code), which is already pre-installed on many rpi distributions (e.g., raspbian). To manually install it, please refere to the Adafruit's [guide](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/adafruit-pi-code).

### Using RPi GPIO agent

```
$ python rpi-gpio.py -h
usage: rpi-gpio.py [-h] [-p PIN] [-j JSON] [-f FREQ] [-n NAME]
                   [--pull_up PULL_UP] [--pull_down PULL_DOWN]

optional arguments:
  -h, --help            show this help message and exit
  -p PIN, --pin PIN     GPIO pin (BCM) to read data from
  -j JSON, --json JSON  Output in SenML
  -f FREQ, --freq FREQ  Pulling frequency, msec
  -n NAME, --name NAME  Sensor name (URI) for SenML output
  --pull_up PULL_UP     Whether to create an internal pull up resistor
  --pull_down PULL_DOWN
                        Whether to create an internal pull down resistor
```

To access the GPIO pin, you need to run the agent with sudo:

```
$ sudo python rpi-gpio.py -p 18
False
...
```

By default, the agent simple outputs boolean `True` or `False`. Use `-j` to output in JSON ([SenML](http://www.ietf.org/internet-drafts/draft-jennings-core-senml-00.txt)):

```
$ sudo python rpi-gpio.py -p 18 -n "http://demo-rpi/gpio/18" -j true
{"bt": 1416143778, "bn": "http://demo-rpi/gpio/18", "e": [{"bv": false}]}
...
```

For some sensors like [magnetic contac switch](http://www.adafruit.com/products/375) it might be necessarry to activate the internal resistor at RPi (pull-up/down):

```
$ $ sudo python rpi-gpio.py -p 23 -n "http://demo-rpi/gpio/23" -j true --pull_up true
{"bt": 1416144524, "bn": "http://demo-rpi/gpio/23", "e": [{"bv": true}]}
...
```

### Device Gateway configuration

Here's an example of a device configuration for the Device Gateway (DGW). You need to create a `airsensor.json` file (or any other unique name) in the `devices` configuration folder of the DWG.

```json
{
  "name": "Motion",
  "description": "Motion detection",
  "meta": {},
  "ttl": 60,
  "resources": [
    {
      "type": "Resource",
      "name": "PIR",
      "meta": {},
      "agent": {
        "type": "service",
        "dir": null,
        "exec": "sudo python /path/to/rpi-gpio.py -p 18 -n http://demo-rpi/gpio/18 -j true"
      },
      "representation": {},
      "protocols": [
        {
          "type": "REST",
          "methods": [
            "GET"
          ],
          "content-types": [
            "application/senml+json"
          ]
        },
        {
          "type": "MQTT",
          "methods": [
            "PUB"
          ],
          "content-types": [
            "application/senml+json"
          ]
        }
      ]
    }
  ]
}
```

In the example above, a "Motion" (should be unique for DGW) is declared with a single resource named "PIR". Consumers of the DGW API will be able to perform a HTTP GET request with a Content-Type "application/senml+json" to obtained the latest GPIO reading (in this case, PIR sensor). The same value can be obtained by subscribing to the MQTT topic.

The agent is of type `service`, which means continuous execution or output of data. The agent program's `exec` key should be an absolute path to the `rpi-gpio.py` executable (make sure the program is executable).
