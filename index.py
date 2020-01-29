from flask import Flask
import logging
import os
from logging.handlers import TimedRotatingFileHandler
import dns.resolver

ENABLE_FILE_LOG = True
app = Flask(__name__)
_LOGGER = logging.getLogger('app.' + __name__)
_LOGGER.setLevel(level="DEBUG")
# create console/file handler
CH = logging.StreamHandler()

FORMATTER = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
CH.setLevel(level="DEBUG")
CH.setFormatter(FORMATTER)
_LOGGER.addHandler(CH)
if ENABLE_FILE_LOG:
    LOG_PATH = os.path.join(os.getcwd(), 'logs')
    LOG_NAME = os.path.join(LOG_PATH, 'sec_bot.log')
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)
    FH = logging.handlers.TimedRotatingFileHandler(LOG_NAME, when="midnight", interval=1)
    FH.setLevel(level="DEBUG")
    FH.setFormatter(FORMATTER)
    _LOGGER.addHandler(FH)

@app.route("/ad")
def ad():
    my_resolver = dns.resolver.Resolver()
    _LOGGER.info("nameserver used: " + my_resolver.nameservers)
    try:
        a = my_resolver.query('ent.labgartner.com', "A")
        _LOGGER.info(a)
        return a
    except Exception  as e:
        _LOGGER.info('didnt resolved.')
        _LOGGER.info(str(e))
        return str(e)

@app.route("/")
def hello():
    _LOGGER.debug("printing debug log")
    _LOGGER.info("printing info log")
    return "Hello World!"

if __name__ == "__main__":
    app.run()
