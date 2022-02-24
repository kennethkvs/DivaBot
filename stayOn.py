from flask import Flask
from threading import Thread
from datetime import datetime

app = Flask('')

@app.route('/')
def home():
  return datetime.now().strftime("%A, %d-%m-%Y %H:%M:%S")

def run():
  app.run(host = "0.0.0.0", port = 8080)

def stayOn():
  t = Thread(target = run)
  t.start()