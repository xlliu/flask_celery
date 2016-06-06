# -*- coding: utf-8 -*-

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from mongo2mysql import app
#import logging
#import logging.config
# abs_path = os.path.split(os.path.realpath(__file__))[0]
#logging.config.fileConfig("logger.conf")
#logger = logging.getLogger("log_output_1")


if __name__ == '__main__':
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(4000)
#    logger.info("http://127.0.0.1:4000/")
    IOLoop.instance().start()
