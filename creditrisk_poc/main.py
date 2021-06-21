from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hydrus.app_factory import app_factory
from hydrus.utils import set_session, set_doc, set_hydrus_server_url, set_api_name
from hydra_python_core import doc_maker
from hydrus.data import doc_parse
from hydrus.data.db_models import Base, create_database_tables
from hydrus.extensions.socketio_factory import create_socket
import configparser
import json

# Fetching database_url & api_doc path from config file
config = configparser.ConfigParser()
config.read('config.ini')
DB_URL = config['Database']['database_url']
API_DOC_PATH = config['API_Doc']['API_Doc_path']

# loading serialized api_doc object
doc_file = open(API_DOC_PATH, "r")
doc = json.load(doc_file)

HYDRUS_SERVER_URL = "http://localhost:8080/"
API_NAME = "creditrisk_api"

apidoc = doc_maker.create_doc(doc, HYDRUS_SERVER_URL, API_NAME)

engine = create_engine(DB_URL)
classes = doc_parse.get_classes(apidoc)
# Drop all existing models and add the new ones.
Base.metadata.drop_all(engine)
# creating the DB tables
create_database_tables(classes)
Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)()


if __name__ == "__main__":
    app = app_factory(API_NAME)
    socketio = create_socket(app, session)
    # Set the name of the API
    with set_api_name(app, API_NAME):
       # Set the API Documentation
       with set_doc(app, apidoc):
           # Set HYDRUS_SERVER_URL
           with set_hydrus_server_url(app, HYDRUS_SERVER_URL):
               # Set the Database session
               with set_session(app, session):
                   socketio.run(app=app,debug=True,port=8080)
