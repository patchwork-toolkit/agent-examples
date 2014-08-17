## Text-to-Speech Actuator Example

This is an example of an actuator you can connect to the Patchwork Toolkit. Obviously this actuator can be used on POSIX operating system and requires a 3rd part package to be installed additionally.


### Prerequisites

On OSX you don't have to install anything, the script will use a built-in `say` command.

On Linux machine you have to install a "espeak" package and make sure you have `espeak` command in the system's path.


### Testing the agent

Run the script from the command line:

    chmod +x ./say.sh
    ./say.sh

Then type any string and press enter. If everything goes fine you should hear the synthesized voice speaking provided string.


### Device Gateway configuration

Here's an example of a device configuration for the Device Gateway (DGW). You need to create a `audio-device.json` file (or any other unique name) in the `devices` configuration folder of the DWG.

    {
      "name": "AudioDevice",
      "description": "This actuator allows to generate speech from a given text and play on the speakers connected to the gateway",
      "meta": {},
      "ttl": 60,
      "resources": [
        {
          "type": "Resource",
          "name": "TTS",
          "meta": {},
          "agent": {
            "type": "task",
            "dir": null,
            "exec": "/path/to/speakers/say.sh"
          },
          "representation": {
            "text/plain": {
              "type": "string"
            }
          },
          "protocols": [
            {
              "type": "REST",
              "methods": [
                "PUT"
              ],
              "content-types": [
                "text/plain"
              ]
            }
          ]
        }
      ]
    }

In the example above a "AudioDevice" (should be unique for DGW) is declared with a single resource named "TTS". Consumers of the DGW API will be able to perform a HTTP PUT request with a Content-Type equal "text/plain" and provide a message string in the HTTP request's body, which will be passed to a agent program (of type `task`, which means executed upon a request). The agent program's `exec` key should be an absolute path to the `say.sh` script (make sure the script is executable).
