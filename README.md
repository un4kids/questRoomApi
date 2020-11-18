<div align="center">
  <a>
    <img width="230" src="./images/quest_mark.jpg">
  </a>
</div>
<div align="center">
  <h1>Quest Room SRV</h1>
  <p>Server side implementation for processes in quest room</p>

</div>

## ✨ Features / Tech stack
-   Communicate with hardware parts, store data and manage configurations
- 📦 Docker
- 📦 Docker-compose
- 🌍 Python
- 🛡 Eclipse Mosquitto broker
- 🛡 Paho-mqtt client
-   Alpine linux


## 📦 Install
0. Clone the project
1. Enter project directory
    ```
    cd project directory
    ```
2. If you want to change .env file and mosquitto configs:
    (for development you can miss this step and use default publish environment and configs)
    - run startup program (python v3)
    ```
    python /startup/startup.py
    ```
    - choose option '0' to autogenerate conf and env files
      - /.env
      - /mosquitto/config/access_control_list.acl
      - /mosquitto/config/mosquitto.conf

3. Build images in docker compose:
    ```
    docker-compose build
    ```
4. Run images:
    ```
    docker-compose up
    ```
5. Go to `questRoomSrv_api/README.md` for DB setup instructions

## Usage
1. View :
    - `tests/ctrl_mqtt_msgs_tests`(implement controller funcs)
    - `tests/insomnia.json`(exported insomnia requests)
    - `TopicShema.txt`(user - topic rules)

## 🤝 Contact

Email us at [brainhublab@gmail.com](mailto:brainhublab@gmail.com)
