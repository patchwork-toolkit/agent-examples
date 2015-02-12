## Example Switch Service

This is an example of a device agent manipulating a device state (on/off switch) over HTTP can be implemented.

### Prerequisites

The agent requires sh/bash to run

### Agent code

The AGENT simply reads `stdin` and stores the provided state in a file, and then outputs the modified state to `stdout`

```bash
STATUS=/tmp/switch.status
while read in
do
  echo "$in" > $STATUS
  cat $STATUS
done
```

### Device Gateway configuration

Below is a simple configuration exposing this agent over HTTP

```json
{
  "name": "ExampleSwitch",
  "description": "Test switch service agent",
  "meta": {},
  "ttl": 120,
  "resources": [
    {
      "type": "Resource",
      "name": "Switch",
      "agent": {
        "type": "service",
        "dir": null,
        "exec": "/path/to/switch.sh"
      },
      "representation": {},
      "protocols": [
        {
          "type": "REST",
          "methods": [
            "GET",
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
```

### Example 

After the Device Gateway has been started, we can test the configured switch:
 
Modifying the switch state:

```
$ curl -X PUT -d "on" http://localhost:8080/rest/ExampleSwitch/Switch
```

Reading the current state:

```
$ curl -H "Content-Type:text/plain" http://localhost:8080/rest/ExampleSwitch/Switch
on
```