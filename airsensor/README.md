## AirSensor agent

This agent requires a hardware (usually in the USB stick form factor) produced by AppliedSensor (http://www.appliedsensor.com/products/indoor-air-monitor.html) and also known as:

* Voltcraft CO-20 USB
* MSR CO2 Air Guard USB
* Butterfly Indoor Air Monitor USB
* Dwyer AQStick model ASQ-1
* eNasco Indoor Air monitor USB
* FRAKTA CO2-Air Gard USB
* Sentinel-Haus Institut RaumluftWächter

### Prerequisites

The agent code requires `libusb` to be installed. Under Ubuntu Linux you can install `libusb` using the following command:

    sudo apt-get install libusb-dev

### Building from source

    gcc -o airsensor airsensor.c -lusb

### Using AirSensor agent

```
$ ./airsensor -help
AirSensor [options]
Options:
-d = debug printout
-v = Print VOC value only, nothing returns if value out of range (450-2000)
-j = Print event in the SenML format
-o = One value and then exit
-h = Help, this printout
```

Running with debug option:

    $ ./airsensor -d
    2014-10-27 21:52:51, DEBUG: Active
    2014-10-27 21:52:51, DEBUG: Init USB
    2014-10-27 21:53:02, DEBUG: USB device found
    ...

If you receive this error then you need to use `sudo` to make the agent claim the USB port:
    
    Error: claim failed with error:  -1

```
$ sudo ./airsensor -d
2014-10-27 21:53:23, DEBUG: Active
2014-10-27 21:53:23, DEBUG: Init USB
2014-10-27 21:53:34, DEBUG: USB device found
2014-10-27 21:53:34, DEBUG: Read any remaining data from USB
2014-10-27 21:53:35, DEBUG: Return code from USB read:  -110
2014-10-27 21:53:35, DEBUG: Write data to device
2014-10-27 21:53:35, DEBUG: Return code from USB write:  16
2014-10-27 21:53:35, DEBUG: Read USB
2014-10-27 21:53:35, DEBUG: Return code from USB read:  16
2014-10-27 21:53:36, DEBUG: Read USB [flush]
2014-10-27 21:53:36, DEBUG: Return code from USB read:
2014-10-27 21:53:35, VOC: 450, RESULT: OK
```

Once you are sure the agent is working you can run it without `-d` but with `-v` option to omit the "noise" in the output:

```
$ sudo ./airsensor -v
495
490
487
...
```


### Device Gateway configuration

Here's an example of a device configuration for the Device Gateway (DGW). You need to create a `airsensor.json` file (or any other unique name) in the `devices` configuration folder of the DWG.

    {
      "name": "AirSensor",
      "description": "Measures quality of the air (VOC).",
      "meta": {},
      "ttl": 60,
      "resources": [
        {
          "type": "Resource",
          "name": "VOC",
          "meta": {},
          "agent": {
            "type": "service",
            "dir": null,
            "exec": "/path/to/airsensor -v"
          },
          "representation": {
            "text/plain": {
              "type": "integer"
            }
          },
          "protocols": [
            {
              "type": "REST",
              "methods": [
                "GET"
              ],
              "content-types": [
                "text/plain"
              ]
            }
          ]
        }
      ]
    }

In the example above a "AirSensor" (should be unique for DGW) is declared with a single resource named "VOC". Consumers of the DGW API will be able to perform a HTTP PUT request with a Content-Type equal "text/plain" and provide a message string in the HTTP request's body, which will be passed to a agent program (of type `service`, which means continuous execution or output of data). The agent program's `exec` key should be an absolute path to the `airsensor` executable (make sure the program is executable).
