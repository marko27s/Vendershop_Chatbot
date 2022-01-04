# ChatBot via Terminal

## Installing Dependencies
```
git clone https://github.com/devstore055/tele_bot.git
cd tele_bot
python3 -m venv venv3
. venv3/bin/activate
cd ..
git clone https://github.com/devstore055/flask_shop.git
cd flask_shop
pip install wheel
pip install -r reqiurements.txt
python setup.py sdist
pip install dist/flask_chatbot_app-1.0.tar.gz
cd ..
cd tele_bot
pip install -r reqiurements.txt
python main.py
```
