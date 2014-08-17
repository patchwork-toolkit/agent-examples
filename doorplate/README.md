## DoorPlate Actuator Example

This example is rather specific and uses custom hardware and software in our office. Briefly, this agent is able to receive a message from DGW API and pass it further to the propriatory API over the HTTP to change the message on the electronic screen mounted above the office door. Anyway the example can be considered as an example of connecting a device to DGW via a network-based protocol.


### Prerequisites

You need to install the following dependency: https://github.com/jakubroztocil/httpie (HTTPie is a human friendly alternative to cURL).

You also need to obtain a USER_ID value, which is the identifier of a specific door plate on the floor.


### Testing the agent

Run the script from the command line:

    chmod +x ./set_message.sh
    USER_ID=<your id here> ./set_message.sh

Then type any string and press enter. If everything goes fine you should hear the synthesized voice speaking provided string.


### Device Gateway configuration

Here's an example of a device configuration for the Device Gateway (DGW). You need to create a `t2l.json` file (or any other unique name) in the `devices` configuration folder of the DWG.

    {
      "name": "T2L",
      "description": "Relies on http://mclab.de/t2l/index.php for showing messages above the door",
      "meta": {},
      "ttl": 60,
      "resources": [
        {
          "type": "Resource",
          "name": "Screen0",
          "meta": {},
          "agent": {
            "type": "task",
            "dir": null,
            "exec": "USER_ID=<your id here> /path/to/tts-actuator/say.sh"
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

In the example above a "T2L" (should be unique for DGW) is declared with a single resource named "Screen0". Consumers of the DGW API will be able to perform a HTTP PUT request with a Content-Type equal "text/plain" and provide a message string in the HTTP request's body, which will be passed to a agent program (of type `task`, which means executed upon a request). The agent program's `exec` key should be an absolute path to the `set_message.sh` script (make sure the script is executable). `<your id here>` should be replaced with an identifier of your door plate.
