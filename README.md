# locker_server
This is a flask server managing the locker website project.

To run it on linux machine configure first:

`pip install -r requirements.txt`

`export FLASK_APP=locker_server.py`

Then run:

`flask run --host=0.0.0.0`

Then access the website via http://127.0.0.1:5000/ if you are on the same machine as the one running the server
or else via http://<machine_ip>:5000/. 