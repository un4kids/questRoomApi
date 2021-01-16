#!/bin/ash

set -e

if ( [ -z "${CONTROLLER_MQTT_USER}" ] || [ -z "${CONTROLLER_MQTT_PASSWORD}" ] ); then
  echo "Missing Controller user or password not defined"
  exit 1
fi
if ( [ -z "${COM_MQTT_USER}" ] || [ -z "${COM_MQTT_PASSWORD}" ] ); then
  echo "Missing Communication service user or password not defined"
  exit 1
fi
if ( [ -z "${UI_MQTT_USER}" ] || [ -z "${UI_MQTT_PASSWORD}" ] ); then
  echo "Missing UI user or password not defined"
  exit 1
fi
if ( [ -z "${WEB_POSTER_MQTT_USER}" ] || [ -z "${WEB_POSTER_MQTT_USER_PASSWORD}" ] ); then
  echo "Missing WEB POSTER user or password not defined"
  exit 1
fi

# create mosquitto passwordfile
touch passwordfile
mosquitto_passwd -b passwordfile $CONTROLLER_MQTT_USER $CONTROLLER_MQTT_PASSWORD
echo "=======>> CONTROLLER_MQTT_USER CONTROLLER_MQTT_PASSWORD defined"
mosquitto_passwd -b passwordfile $COM_MQTT_USER $COM_MQTT_PASSWORD
echo "=======>> COM_MQTT_USER COM_MQTT_PASSWORD defined"
mosquitto_passwd -b passwordfile $UI_MQTT_USER $UI_MQTT_PASSWORD
echo "=======>> UI_MQTT_USER UI_MQTT_PASSWORD defined"
mosquitto_passwd -b passwordfile $WEB_POSTER_MQTT_USER $WEB_POSTER_MQTT_USER_PASSWORD
echo "=======>> WEB_POSTER_MQTT_USER WEB_POSTER_MQTT_USER_PASSWORD defined"

exec "$@"
