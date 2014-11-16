## Raspberry Pi BPM180 agent

This agent reads data from the [BMP180 Barometric Pressure/Temperature/Altitude Sensor](http://www.adafruit.com/product/1603) sensors on Raspberry Pi and outputs it either as plain/text, or as a JSON/SenML.

### Prerequisites

The agent code uses the [Adafruit python library for BMP085/BMP180](https://github.com/adafruit/Adafruit_Python_BMP), which is already pre-installed on many rpi distributions (e.g., raspbian). To manually install it, please refere to the Adafruit's [guide](https://learn.adafruit.com/using-the-bmp085-with-raspberry-pi/using-the-adafruit-bmp-python-library).

### Using RPi BPM180 agent

```
$ python rpi-bpm180.py -h
usage: rpi-bpm180.py [-h] [-j JSON] [-f FREQ] [-s SENSOR] [-bn BASENAME]

optional arguments:
  -h, --help            show this help message and exit
  -j JSON, --json JSON  Output in SenML
  -f FREQ, --freq FREQ  Pulling frequency, msec
  -s SENSOR, --sensor SENSOR
                        Sensor (all if not specified): temp|pres|alt|slpres
  -bn BASENAME, --basename BASENAME
                        Sensor BaseName (URI) for SenML output
```

To access the I2C sensor, you need to run the agent with sudo:

```
$ sudo python rpi-bpm180.py
19.30 98273.00 256.82 98285.00
...
```

By default, the agent outputs all sensor measurements in the space-separated plain/text format:

```
temperature(C) pressure(Pa) altitude(m) sealevel_pressure(Pa)
```

Use `-j` to obtain the same output in JSON ([SenML](http://www.ietf.org/internet-drafts/draft-jennings-core-senml-00.txt)):

```
$ sudo python rpi-bpm180.py -bn "http://demo-bpm180/" -j true
{"bt": 1416150348, "bn": "http://demo-bpm180/", "e": [{"v": 19.3, "u": "degC", "n": "temperature"}, {"v": 98274, "u": "Pa", "n": "pressure"}, {"v": 256.65181932422746, "u": "m", "n": "altitude"}, {"v": 98274.0, "u": "Pa", "n": "sealevel_pressure"}]}
...
```

The agent also allows to obtain a measurement of a specific sensor (parameter`-s temp|pres|alt|slpres`):

```
$ sudo python rpi-bpm180.py -s temp
19.30
...
```

And the same in SenML:

```
$ sudo python rpi-bpm180.py -bn "http://demo-bpm180/" -s temp -j true
{"bt": 1416151230, "e": [{"v": 19.3, "u": "degC", "n": "http://demo-bpm180/temperature"}]}
```

### Device Gateway configuration

Here's an example of a device configuration for the Device Gateway (DGW). You need to create a `bpm-180.json` file (or any other unique name) in the `devices` configuration folder of the DWG.

```json
{
  "name": "Barometer",
  "description": "Barometric sensor BPM180",
  "meta": {},
  "ttl": 60,
  "resources": [
    {
      "type": "Resource",
      "name": "Temperature",
      "meta": {},
      "agent": {
        "type": "service",
        "dir": null,
        "exec": "sudo python /path/to/rpi-bpm180.py -bn http://demo-bpm180/ -s temp -j true"
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
    },
    {
      "type": "Resource",
      "name": "Pressure",
      "meta": {},
      "agent": {
        "type": "service",
        "dir": null,
        "exec": "sudo python /path/to/rpi-bpm180.py -bn http://demo-bpm180/ -s pres -j true"
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
    },
    {
      "type": "Resource",
      "name": "Altitude",
      "meta": {},
      "agent": {
        "type": "service",
        "dir": null,
        "exec": "sudo python /path/to/rpi-bpm180.py -bn http://demo-bpm180/ -s alt -j true"
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
    },
    {
      "type": "Resource",
      "name": "SealevelPressure",
      "meta": {},
      "agent": {
        "type": "service",
        "dir": null,
        "exec": "sudo python /path/to/rpi-bpm180.py -bn http://demo-bpm180/ -s slpres -j true"
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
    },
  ]
}
```

In the example above, a "Barometer" (should be unique for DGW) device is declared with three resources: "Templerature", "Pressure", "Altitude", "SealevelPressure". Consumers of the DGW API will be able to perform a HTTP GET request with a Content-Type "application/senml+json" to obtained the latest sensor measurements. The same values can be obtained by subscribing to the corresponding MQTT topics.

The agent is of type `service`, which means continuous execution and output of data. The agent program's `exec` key should be an absolute path to the `rpi-bpm180.py` executable (make sure the program is executable).
