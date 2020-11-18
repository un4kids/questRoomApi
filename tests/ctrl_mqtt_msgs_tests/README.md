<p>Test Controller funcs</p>


## ✨ Features / Tech stack
- 🛡 Paho-mqtt client
- 🌍 Python


## 🔨 Usage
<p>When the system is up mqtt_master_cli start listen the authentication topic for new controller to registrate (can test with quest_auth.py).
On message in "quest/auth" mqtt_master_cli will make POST request to the API
with the data from the message.
At end of request mqtt_master_cli will send status code from request
back to controller on the topic "quest/authCheck"
</p>

<p>quest_healthcheck.py publish data in 'quest/{mac)addr}/healthcheck'.
Only implement controller msg publishing process. I do nothing with it in backend (will be subscribed in UI)</p>

<p>quest_model_in.py publish data in 'quest/{mac)addr}/modelIn'.
Only implement controller msg publishing process. I do nothing with it in backend (will be subscribed in UI and another controllers)</p>



## 🤝 Contact

Email us at [brainhublab@gmail.com](mailto:brainhublab@gmail.com)
