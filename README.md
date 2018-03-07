Pool automation control prototype

```
Raspberry PI 3
| 
+---usb--> Arduino Uno -> x10_serial -> x10 power line module -> x10 pool lights (A01/A02/A03; on/off)
+---usb--> Arduino Nano --analog--> ETape (water level)
+---gpio-> Relay board -> Jandy valve actuators (vacuum/skimmer and return/waterfall)
+---cli commands(autofill/lights/valves/etape)/cron(scheduled tasks)
+---Flask py web service <- web ui
```




