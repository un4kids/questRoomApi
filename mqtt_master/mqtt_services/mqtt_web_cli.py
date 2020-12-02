import paho.mqtt.client as paho
import os
from time import sleep


class MqttCtrlWebClient(object):
    def __init__(self, mqtt_master, logger):
        """ basic topics """
        self.mqtt_mstr = mqtt_master
        self.quest_modeIn = os.environ.get("QUEST_MODE_IN")

        self.com_user = os.environ.get("COM_MQTT_USER")
        self.com_pwd = os.environ.get("COM_MQTT_PASSWORD")

        self.broker_url = os.environ.get("BROKER_HOST")
        self.broker_webs_port = int(os.environ.get("BROKER_WEBSOCKET_PORT"))

        self.kill = False
        self.connect = False
        self.logger = logger

    # ***                            SUBSCRIBERS                             ***
    def on_connect(self, client, userdata, flags, rc):
        """ Create the required subscribers """
        client.subscribe("ui/" + self.quest_modeIn.format("+"))
        client.message_callback_add("ui/" + self.quest_modeIn.format("+"),
                                    self.on_message_ui_mode_in)

    def on_message_ui_mode_in(self, client, userdata, msg):
        self._mqttPubMsg(self.mqtt_mstr, msg.topic[3:], msg.payload.decode())

    def on_message(self, client, userdata, msg):
        self.logger.info("\n[???] [{0}], [{1}] - [{2}]\n".format(client._client_id, msg.topic, msg.payload))

    def on_log(self, client, userdata, level, buf):
        self.logger.info("\n[*] [{0}] [{1}] [{2}]\n".format(client._client_id.decode(), level, buf))

    def _broker_auth(self, client):
        client.username_pw_set(username=self.com_user, password=self.com_pwd)

    def on_disconnect(self, client, userdata, rc=0):
        """ Unsubscribe topics and disconnect"""
        sub_topics = ["ui/" + self.quest_modeIn.format("+"), ]

        for topic in sub_topics:
            client.unsubscribe(topic)
        client.disconnect()
        client.loop_stop()
        self.logger.info("\n[*] [DISCONNECT] [{0}]\n".format(client._client_id.decode()))

    # ***                            CLIENT CONFIGS                            ***
    def bootstrap(self):
        mqtt_websocket_cli = paho.Client(client_id="web_cli", clean_session=False,
                                         protocol=paho.MQTTv311, transport='websockets')
        self._broker_auth(mqtt_websocket_cli)
        mqtt_websocket_cli.on_connect = self.on_connect
        mqtt_websocket_cli.on_message = self.on_message
        mqtt_websocket_cli.on_log = self.on_log
        mqtt_websocket_cli.on_disconnect = self.on_disconnect
        result_of_connection = mqtt_websocket_cli.connect(self.broker_url, self.broker_webs_port)
        if result_of_connection == 0:
            mqtt_websocket_cli.loop_start()
        return mqtt_websocket_cli

    def _mqttPubMsg(self, client, topic, data):
        while True:
            sleep(2)
            try:
                client.publish(topic, data, qos=1)
                break
            except Exception as e:
                raise e
                continue
            else:
                self.logger.debug("\n[!] Attempting to connect!\n")
