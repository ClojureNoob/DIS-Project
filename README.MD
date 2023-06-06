# NASDAQ DIS PROJECT    
This project is a limited simulation of historical data from the NASDAQ. It consists of a simple flask app and a postgres backend

## Setup
To run the project clone the repository and run db_setup.py. The setup script is dependent on a config-file config.config. An example is given in config.config.example, but this should be customized. Be aware that the config file assumes the existence of an already existing database.  After setup, the web app can then be run by running app.py.