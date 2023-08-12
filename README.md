# ChatBot via Terminal

## Installing Dependencies
```
git clone 
python3 -m venv venv3
. venv3/bin/activate
pip install --upgrade pip
cd ..
git clone
cd flask_shop
git checkout main
pip install wheel
pip install -r requirements.txt 
source .env
python setup.py sdist
pip install dist/flask_chatbot_app-1.0.tar.gz
cd ..
cd tele_bot
source .env
pip install -r requirements.txt 
flask run --host=0.0.0.0 --port=5004
```

## Visit the Chat
http://localhost:5004/chat