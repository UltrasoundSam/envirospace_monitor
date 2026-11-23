# Deploy Helper Information

All of the items within this folder are supporting the deployment of the envirospace monitors within the field. A lot of this is stuff that is tied up within the operating system, so not really conducive for putting in the main repo, but can be useful to keep track of them to make sure deployment of subsequent devices is a bit easier.

## Systemctl Service - envirospace.service

In order to make sure that the main.py is always running, even if the Pi loses connectivity briefly or is restarted following a power loss, a envirospace.service file was created to orchestrate a systemctl service.

The service will run main.py via uv at start-up to make sure the script always starts, as well if the script fails for whatever reason, it will attempt to restart after 30 seconds. Systemctl also allows to put a burst limit (in our case, it gives up after 5 attempts).

The file should be placed in ```/etc/systemd/system/envirospace.service```

```bash
# Tell systemd about new script
sudo systemctl daemon-reload

# Enable startup
sudo systemctl enable envirospace

# Manually start it now
sudo systemctl start envirospace

# Check status to make sure that it is up
sudo systemctl status envirospace

# Any logs will be displaced in journalctl
journalctl -u envirospace -f
```

## Enviroment Variables - .env

Configuration and authentication values are stored in local .env files. These are obviously not stored within the repo, but a blank template has been included so that people know what needs to be specified.

```bash
MQTT_BROKER=
MQTT_PORT=
MQTT_BASE_TOPIC=envirospace/room101
MQTT_USERNAME=
MQTT_PASSWORD=
```

The MQTT base topic should be changed for different rooms. Currently, we have room101, but this should be changed for a new install.
