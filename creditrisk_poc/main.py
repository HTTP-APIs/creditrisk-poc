import os
import json
import logging
from pathlib import Path
from os.path import abspath, dirname
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hydrus.app_factory import app_factory
from hydrus.utils import (
    set_session,
    set_doc,
    set_hydrus_server_url,
    set_token,
    set_api_name,
    set_authentication,
)
from hydra_python_core import doc_maker
from hydrus.data import doc_parse
from gevent.pywsgi import WSGIServer
from hydrus.data.db_models import Base, create_database_tables
from hydrus.extensions.socketio_factory import create_socket


logger = logging.getLogger(__file__)

# Fetching database_url & api_doc path from env variables
PORT = int(os.environ["PORT"]) if "PORT" in dict(os.environ).keys() else 8080
API_NAME = os.environ["API_NAME"] if "API_NAME" in dict(os.environ).keys() else "creditrisk_api"
DB_URL = (
    os.environ["DB_URL"]
    if "DB_URL" in dict(os.environ).keys()
    else "sqlite:///database.db"
)

HYDRUS_SERVER_URL = f"http://localhost:{PORT}/"

cwd_path = Path(dirname(dirname(abspath(__file__))))
API_DOC_PATH = cwd_path / "creditrisk_poc" / "api_doc" / "ApiDoc.jsonld"

# loading serialized api_doc object
doc_file = open(API_DOC_PATH, "r")
doc = json.load(doc_file)

apidoc = doc_maker.create_doc(doc, HYDRUS_SERVER_URL, API_NAME)

engine = create_engine(DB_URL)
classes = doc_parse.get_classes(apidoc)
# Drop all existing models and add the new ones.
Base.metadata.drop_all(engine)
# creating the DB tables
create_database_tables(classes)
Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)()

AUTH = False
TOKEN = False

# Create a Hydrus app
app = app_factory(API_NAME)
socketio = create_socket(app, session)
#
# Nested context managers
#
# Use authentication for all requests
# Set the API Documentation
# Set HYDRUS_SERVER_URL
# Set the Database session
with set_authentication(app, AUTH), set_token(app, TOKEN), set_api_name(
    app, API_NAME
), set_doc(app, apidoc), set_hydrus_server_url(app, HYDRUS_SERVER_URL), set_session(
    app, session
):
    if __name__ == "__main__":
        # this is run only if development server is run
        # Set the name of the API
        socketio.run(app=app, debug=True, port=PORT)
    else:
        # Start the Hydrus app
        http_server = WSGIServer(("", PORT), app)
        logger.info(f"Running server at port {PORT}")
        try:
            http_server.serve_forever()
        except KeyboardInterrupt:
            pass
