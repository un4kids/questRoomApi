import paho.mqtt.client as paho
import os
from time import sleep


class WebPosterMqttCli(object):
    def __init__(self, logger):
        """ basic topics """
        self.web_poster_user = os.environ.get("WEB_POSTER_MQTT_USER")
        self.web_poster_pwd = os.environ.get("WEB_POSTER_MQTT_USER_PASSWORD")

        self.broker_url = os.environ.get("BROKER_HOST")
        self.broker_webs_port = int(os.environ.get("BROKER_WEBSOCKET_PORT"))
        self.broker_port = int(os.environ.get("BROKER_PORT"))

        self.kill = False
        self.connect = False
        self.logger = logger

    # ***                            SUBSCRIBERS                             ***
    def on_message(self, client, userdata, msg):
        self.logger.info("\n[???] [{0}], [{1}] - [{2}]\n".format(client._client_id, msg.topic, msg.payload))

    def on_log(self, client, userdata, level, buf):
        self.logger.info("\n[*] [{0}] [{1}] [{2}]\n".format(client._client_id.decode(), level, buf))

    def _broker_auth(self, client):
        client.username_pw_set(username=self.web_poster_user, password=self.web_poster_pwd)

    def on_disconnect(self, client, userdata, rc=0):
        client.disconnect()
        client.loop_stop()
        self.logger.info("\n[*] [DISCONNECT] [{0}]\n".format(client._client_id.decode()))

    # ***                            CLIENT CONFIGS                            ***
    def bootstrap(self):
        mqtt_websocket_cli = paho.Client(client_id="web_poster_cli", clean_session=True,
                                         protocol=paho.MQTTv311, transport='websockets')
        self._broker_auth(mqtt_websocket_cli)
        mqtt_websocket_cli.on_message = self.on_message
        mqtt_websocket_cli.on_log = self.on_log
        mqtt_websocket_cli.on_disconnect = self.on_disconnect
        result_of_connection = mqtt_websocket_cli.connect(self.broker_url, self.broker_webs_port)
        if result_of_connection == 0:
            mqtt_websocket_cli.loop_start()
        return mqtt_websocket_cli
