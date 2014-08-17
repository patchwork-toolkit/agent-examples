## Motion Detector Device Example

This is an example of a sensor that can detect movement in the visible area using snapshots from a USB camera.


### Prerequisites

On OSX you need to install the following dependencies:

    brew install imagesnap
    brew install imagemagick
    pip install PIL

Other platforms: to be done soon.


### Testing the agent

Run the script from the command line:

    python simple.py

Then type any string and press enter. If everything goes fine you should hear the synthesized voice speaking provided string.


### Device Gateway configuration

Here's an example of a device configuration for the Device Gateway (DGW). You need to create a `t2l.json` file (or any other unique name) in the `devices` configuration folder of the DWG.

    {
      "name": "Alarm",
      "description": "Detects movement in the office using USB camera and simple pixel-wise snapshots comparison",
      "meta": {
      },
      "ttl": 120,
      "resources": [
        {
          "type": "Resource",
          "name": "MotionDetector",
          "agent": {
            "type": "service",
            "dir": null,
            "exec": "python simple.py"
          },
          "representation": {
            "application/json": {
              "$schema": "http://json-schema.org/schema",
              "type": "object",
              "description": "Movement",
              "properties": {
                "movement": "boolean",
                "measured": "datetime"
              },
              "required": [
                "movement",
                "measured"
              ]
            }
          },
          "protocols": [
            {
              "type": "REST",
              "methods": [
                "GET"
              ],
              "content-types": [
                "application/json"
              ]
            },
            {
              "type": "MQTT",
              "methods": [
                "SUB"
              ],
              "content-types": [
                "application/json"
              ]
            }
          ]
        }
      ]
    }

In the configuration above a single device `Alarm` with a single resource `MotionDetector` are defined. The data from the resource will be published to MQTT broker and available for the HTTP GET requests.
