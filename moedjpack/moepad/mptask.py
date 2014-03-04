from moedjpack.moepad.mpcelery import app
from mputils import logger
from update import UpdateItems, SendItem


@app.task
def send():
    sender = SendItem()
    sender.sendRoutine()


@app.task
def updateitem():
    update = UpdateItems(20)
    update.updateRoutine()


@app.task
def justtest():
    logger.info("justtest")


@app.task
def nighttest():
    logger.info("nighttest")
