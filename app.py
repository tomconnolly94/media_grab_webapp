#!/venv/bin/python

# external dependencies
from flask import Flask, request, redirect, Response
from dotenv import load_dotenv
from os.path import join, dirname

# internal dependencies
from server.page_server import serveIndex, serveNodeModule, serveCustomJsModule, serveCustomCssModule
from server.data_server import serveMediaInfo, submitMediaInfoRecord, deleteMediaInfoRecord

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
    return serveMediaInfo()


@app.route('/MediaInfoRecord', methods=["POST", "DELETE"])
def MediaIndexRecord():
    if request.method == "POST":
        submitMediaInfoRecord(request.form)
        return redirect("/")
    elif request.method == "DELETE":
        deleteMediaInfoRecord(request.args["recordName"])
        return Response(response="Ok",
                    status=200)
    else:
        print("ERROR: http request method unrecognised for this route")

    # request.method = "GET"
    # return redirect("/")


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
    app.run(host="0.0.0.0")
