Copy the startup script from
```startupscript/```
to 
```/etc/systemd/system```.


You can now start/stop this service with ```systemctl start fridgetracker``` / ```systemctl stop frdigetracker```.
To enable this service when startup, run ```systemctl enable my-service```.