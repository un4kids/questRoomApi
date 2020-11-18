from . import api
# from flask import current_app as app
from ... import db
from ...models.quests import Quest
from ..utils import parser, is_there_an_object, auth_check
from flask_restful import Resource
# from ..mqtt_client.mqtt_client_publisher import MqttClientPub
# import json

# Parse arguments from requests
# official documentation: https://flask-restful.readthedocs.io/en/latest/reqparse.html

q_parser = parser.copy()
q_parser.add_argument("title",
                      required=True,
                      location="json",
                      type=str,
                      help="title field cannot be blank")
q_parser.add_argument("mac_addr",
                      required=False,
                      location="json",
                      type=str)
q_parser.add_argument("index",
                      required=True,
                      location="json",
                      type=int,
                      help="index address field cannot be blank")
q_parser.add_argument("config",
                      required=True,
                      location="json",
                      type=dict,
                      help="config field cannot be blank")


class Quests(Resource):
    @auth_check
    def get(self):
        all_quests = Quest.query.order_by("updated_on")
        return [x.toDict() for x in all_quests], 200

    @auth_check
    def post(self):
        args = q_parser.parse_args()
        if args["mac_addr"] is None:
            return {
                "message": "mac_addr is required!"
            }, 400
        quest_by_mac = Quest.query.filter_by(mac_addr=args["mac_addr"]).first()
        quest_by_index = Quest.query.filter_by(index=args["index"]).first()

        if quest_by_index is not None:
            return {
                "message": "index already in use!"
            }, 400

        if quest_by_mac is not None:
            return {
                "message": "Quest with mac_addr: '{}' already exist!".format(args["mac_addr"])
            }, 409

        new_quest = Quest(
            title=args["title"],
            mac_addr=args["mac_addr"],
            index=args["index"],
            config=args["config"]
        )
        db.session.add(new_quest)
        db.session.commit()

        new_quest_info = new_quest.toDict()
        return new_quest_info, 201


api.add_resource(Quests, "/api/quests/")


class CQuest(Resource):
    @auth_check
    def get(self, id):
        quest = Quest.query.filter_by(id=id).first()
        if is_there_an_object(quest):
            return quest.toDict(), 200
        else:
            return {
                "message": "Obj not found!"
            }, 404

    @auth_check
    def put(self, id):
        args = q_parser.parse_args()
        quest_to_update = Quest.query.filter_by(id=id).first()
        obj_by_index = Quest.query.filter_by(index=args["index"]).first()
        if obj_by_index is not None:
            if obj_by_index.id != id:
                return {
                    "message": "Index already in use!"
                }, 409

        if is_there_an_object(quest_to_update):
            quest_to_update.title = args["title"]
            quest_to_update.index = args["index"]
            quest_to_update.config = args["config"]

            db.session.commit()
            new_data = quest_to_update.toDict()
            return new_data, 200
        else:
            return {
                "message": "Obj not found!"
            }, 404

    @auth_check
    def delete(self, id):
        quest = Quest.query.filter_by(id=id).first()
        if quest:
            """ Remove quest from db """
            db.session.delete(quest)
            db.session.commit()
            return {"message": "ok"}, 200
        else:
            return {"message": "Not Found"}, 404


api.add_resource(CQuest, "/api/quests/<int:id>/")
