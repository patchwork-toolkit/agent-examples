## Local System Sensors Example

This is an example of a sensor platfomr you can connect to the Patchwork Toolkit. Obviously this example can be used on POSIX operating system.


### Testing the agents

Run the script from the command line:

    chmod +x ./*.sh
    ./processes.sh
    ./uptime.sh
    python diskspace.py


### Device Gateway configuration

Here's an example of a device configuration for the Device Gateway (DGW). You need to create a `system.json` file (or any other unique name) in the `devices` configuration folder of the DWG.

    {
      "name": "System",
      "description": "This device reports system metrics from a computer running a gateway",
      "meta": {},
      "ttl": 30,
      "resources": [
        {
          "type": "Resource",
          "name": "PS",
          "meta": {},
          "agent": {
            "type": "timer",
            "interval": 5,
            "dir": null,
            "exec": "/path/to/processes.sh"
          },
          "representation": {
            "application/json": {
              "$schema": "http://json-schema.org/draft-04/schema#",
              "title": "ProcessCount",
              "description": "Total number of processes at the certain time",
              "type": "object",
              "properties": {
                "count": {
                  "description": "Number of processes",
                  "type": "integer"
                },
                "timestamp": {
                  "description": "Linux timestamp of count measurement time",
                  "type": "integer"
                }
              },
              "required": [
                "count",
                "timestamp"
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
            }
          ]
        },
        {
          "type": "Resource",
          "name": "LoadAverage",
          "meta": {},
          "agent": {
            "type": "timer",
            "interval": 30,
            "dir": null,
            "exec": "/path/to/loadaverage.sh"
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
                "GET"
              ],
              "content-types": [
                "text/plain"
              ]
            }
          ]
        },
        {
          "type": "Resource",
          "name": "DiskUsage",
          "meta": {},
          "agent": {
            "type": "task",
            "interval": null,
            "dir": null,
            "exec": "python /path/to/diskspace.py"
          },
          "representation": {
            "application/json": {
              "$schema": "http://json-schema.org/draft-04/schema#",
              "title": "DiskUsage",
              "description": "Disk usage document description",
              "type": "object",
              "properties": {
                "total": {
                  "description": "Total disk usage",
                  "type": "integer"
                },
                "free": {
                  "description": "Free disk space",
                  "type": "integer"
                },
                "used": {
                  "description": "Used disk space",
                  "type": "integer"
                }
              },
              "required": [
                "total",
                "free",
                "used"
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
            }
          ]
        }
      ]
    }

In the example above we define device `System` with 3 resources: `PS`, `LoadAverage` and `DiskUsage`. Each of this resources exposed as RESTful service that supports only GET method. `PS` and `LoadAverage` agents are defined as timer with specific intervals. This means that requests will read data only from the timer output cache (no process will initiated upon the request).