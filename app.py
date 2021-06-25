#!/venv/bin/python

# external dependencies
from flask import Flask, render_template, Response
from dotenv import load_dotenv
from os.path import join, dirname
import os

# internal dependencies


#create app
app = Flask(__name__, template_folder="client")

# load env file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


@app.route("/", methods=["GET"])
def serverIndex():
    resp = Response(response=render_template('./index.html'),
                    status=200,
                    mimetype="text/html")

                    
    f = open(f"client/index.html", "r")
    return f.read()

@app.route("/MediaIndex", methods=["GET"])
def serveMediaIndex():
    f = open(os.getenv("MEDIA_INDEX_FILE_LOCATION"), "r")
    mediaIndexFileContent = f.read()
    return mediaIndexFileContent

@app.route("/node_modules/<module>", methods=["GET"])
def serveNodeModule(module):
    moduleName = module.replace(".js", "")
    f = open(f"client/node_modules/{moduleName}/dist/{moduleName}.js", "r")
    
    return Response(response=f.read(),
                    status=200,
                    mimetype="text/javascript")

@app.route("/js/<module>", methods=["GET"])
def serveModule(module):
    moduleName = module.replace(".js", "")
    f = open(f"client/{moduleName}.js", "r")

    return Response(response=f.read(),
                    status=200,
                    mimetype="text/javascript")


if __name__ == "__main__":
    app.run()