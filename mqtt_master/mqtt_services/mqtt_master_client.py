import paho.mqtt.client as paho
import signal
import os
import json
from time import sleep
import sys
sys.path.insert(0, os.path.abspath('..'))
from http_requests.requestss import ApiRequests as api_req
from .logger import reg_logger
from .mqtt_web_cli import MqttCtrlWebClient

web_cli = MqttCtrlWebClient


class MqttMasterClient(object):
    def __init__(self, listener=False):
        """ take the basic topic names from envoirnment file"""
        self.mqtt_master_cli_id = os.environ.get("MQTT_MASTER_CLI_ID")
        self.com_user = os.environ.get("COM_MQTT_USER")
        self.com_pwd = os.environ.get("COM_MQTT_PASSWORD")
        self.broker_url = os.environ.get("BROKER_HOST")
        self.broker_port = int(os.environ.get("BROKER_PORT"))

        self.quest_auth = os.environ.get("QUEST_AUTH_TOPIC")
        self.quest_authCheck = os.environ.get("QUEST_AUTH_CHECK_TOPIC")
        self.quest_healthcheck = os.environ.get("QUEST_HEALTH_CHECK_TOPIC")
        self.quest_modeIn = os.environ.get("QUEST_MODE_IN")

        self.connect = False
        self.kill = False
        self.listener = listener
        self.logger = reg_logger()

    # ***                            SUBSCRIBERS                             ***
    def on_connect(self, client, userdata, flags, rc):
        self.connect = True
        if self.listener:
            self.mqttc.subscribe(self.quest_auth)
            self.mqttc.subscribe(self.quest_healthcheck.format('+'))

            self.mqttc.message_callback_add(self.quest_auth,
                                            self.on_message_from_quest_auth)
            self.mqttc.message_callback_add(self.quest_healthcheck.format('+'),
                                            self.on_message_from_quest_healthcheck)
        self.web_client = web_cli(self.mqttc, self.logger).bootstrap()

    # ***                              CALLBACKS                               ***
    def on_message(self, client, userdata, msg):
        self.logger.info("\n[???] [{0}], [{1}] - [{2}]\n".format(client._client_id,
                                                                 msg.topic,
                                                                 msg.payload))

    def on_message_from_quest_auth(self, client, userdata, msg):
        """ calback handling new quest registration
                - create quest object in API
        """
        quest_data = json.loads(msg.payload.decode())
        title = quest_data["title"]
        mac = quest_data["mac_addr"]
        quest_index = quest_data["quest_index"]

        post_data = {"title": title,
                     "mac_addr": mac,
                     "quest_index": quest_index}

        new_quest = api_req(data=post_data).post_quest()
        self._mqttPubMsg(self.mqttc,
                         self.quest_authCheck.format(mac),
                         json.dumps({"status": new_quest.status_code}))
        self.logger.info("\n[*] [API] [{0}] [{1}] [{2}]\n".format(new_quest.request.method,
                                                                  new_quest.url,
                                                                  new_quest.status_code))

    def on_message_from_quest_healthcheck(self, client, userdata, msg):
        """ callback handling controllers healthCheck messages (send to UI over websocket) """
        self._mqttPubMsg(self.web_client, 'ui/' + msg.topic, msg.payload)

    # ***                               UTILS                                ***
    def on_log(self, client, userdata, level, buf):
        self.logger.info("\n[*] [{0}] [{1}] [{2}]\n".format(client._client_id.decode(), level, buf))

    def _broker_auth(self, client):
        client.username_pw_set(username=self.com_user, password=self.com_pwd)

    def on_disconnect(self, client, userdata, rc=0):
        self.logger.info("\n[*] [DISCONNECT] [{0}]\n".format(client._client_id.decode()))

    def bootstrap_mqtt(self):
        self.mqttc = paho.Client(self.mqtt_master_cli_id, protocol=paho.MQTTv311)
        self._broker_auth(self.mqttc)
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message
        self.mqttc.on_log = self.on_log
        self.mqttc.on_disconnect = self.on_disconnect
        result_of_connection = self.mqttc.connect(self.broker_url, self.broker_port)
        if result_of_connection == 0:
            self.connect = True
        return self

    def seppuku(self, signum, frame):
        self.kill = True

    def start(self):
        self.logger.info("{0}".format("\n[*] [Query listeners are Up!]\n"))
        signal.signal(signal.SIGINT, self.seppuku)
        signal.signal(signal.SIGTERM, self.seppuku)

        while not self.kill:
            self.mqttc.loop()
        else:
            self.web_client.disconnect()
            self.web_client.loop_stop()
            self.mqttc.disconnect()
            self.mqttc.loop_stop()

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
