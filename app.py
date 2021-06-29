#!/venv/bin/python

# external dependencies
from flask import Flask, request, redirect, Response, send_from_directory
from dotenv import load_dotenv
from os.path import join, dirname
import os

# internal dependencies
from server.page_server import serveIndex, serveNodeModule, serveCustomJsModule, serveCustomCssModule
from server.data_server import serveMediaInfo, submitMediaInfoRecord, deleteMediaInfoRecord, updateMediaInfoRecord

#create app
app = Flask(__name__, template_folder="client")

# load env file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def getErrorReponse(errorCode, errorMessage):
    Response(errorMessage, status=errorCode, mimetype="text/html") 


@app.route("/", methods=["GET"])
def index():
    return serveIndex()


@app.route("/favicon.ico", methods=["GET"])
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'client/images'),
                          'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/MediaInfoRecords", methods=["GET"])
def MediaInfoRecords():
        return serveMediaInfo()



# @app.route("/MediaIndex/<recordIndex>", methods=["GET", "PUT"])
# def MediaIndex(recordIndex):
#     elif request.method == "PUT":
#         if updateMediaInfoRecord(request.data):
#             return getErrorReponse(200, "got put request, all good") 
#         else:
#             return getErrorReponse(500, "put request failed") 
#     else:
#         return Response("ERROR, method incorrect",
#                     status=404,
#                     mimetype="text") 



@app.route('/MediaInfoRecord/<recordIndex>', methods=["POST", "PUT", "DELETE"])
def MediaIndexRecord(recordIndex):
    if request.method == "POST":
        submitMediaInfoRecord(request.form)
        return redirect("/")
    elif request.method == "DELETE":
        deleteMediaInfoRecord(request.args["recordName"])
        return Response(response="Ok",
                    status=200)
    elif request.method == "PUT":
        if updateMediaInfoRecord(request.data, int(recordIndex)):
            return getErrorReponse(200, "got put request, all good") 
        else:
            return getErrorReponse(500, "put request failed") 
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
