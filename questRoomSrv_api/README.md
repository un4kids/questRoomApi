<div align="center">
  <h1>Api</h1>
  <p>Flask restful api implementation for quest_room_srv_api</p>

</div>

## ✨ Features / Tech stack
-   Flask
- 📦 Flask-restful
- 🌍 Python
- 🛡 Paho-mqtt client
-   Nginx
-   PostgreSQL
- 📦 SQLAlchemy
-   Alpine linux

## 🔨 Install
<p>When questRoomSrv_api container run for first time you may need to migrate db handly.</p>

0. Migrate DB tables:
      - Enter api container:
        ```
        docker exec -it questRoomSrv_api /bin/ash
        ```
      - Migrarate DB tables:
          ```
          flask db migrate
          ```
      - Upgrade DB tables:
          ```
          flask db upgrade
          ```
      !!! In case of `sqlalchemy-utils` error check [this](https://stackoverflow.com/questions/54055469/how-to-use-sqlalchemy-utils-in-a-sqlalchemy-model):


## 🤝 Contact

Email us at [brainhublab@gmail.com](mailto:brainhublab@gmail.com)
