#!/venv/bin/python

# external dependencies
from flask import Flask, request
from dotenv import load_dotenv
from os.path import join, dirname
import os

# internal dependencies
from server.page_server import serveIndex, serveNodeModule, serveCustomJsModule, serveCustomCssModule
from server.data_server import serveMediaIndex, submitMediaIndexRecord

#create app
app = Flask(__name__, template_folder="client")

# load env file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


@app.route("/", methods=["GET"])
def index():
    return serveIndex()


@app.route("/MediaIndex", methods=["GET"])
def MediaIndex():
    return serveMediaIndex()

    
@app.route('/MediaIndexRecord', methods=["POST"])
def MediaIndexRecord():
    return submitMediaIndexRecord(request)


@app.route("/node_modules/<module>", methods=["GET"])
def nodeModule(module):
    return serveNodeModule(module)


@app.route("/js/<module>", methods=["GET"])
def customJsModule(module):
    return serveCustomJsModule(module)


@app.route("/css/<module>", methods=["GET"])
def customCssModule(module):
    return serveCustomCssModule(module)


if __name__ == "__main__":
    app.run()