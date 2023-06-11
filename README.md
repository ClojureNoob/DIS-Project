# NASDAQ DIS PROJECT    
This project is a limited simulation of historical data from the NASDAQ. It consists of a simple flask app and a postgres backend

## Setup
To run the project, clone the repository and run 'db_setup.py'. The setup script is dependent on a config-file 'config.config'. An example is given in 'config.config.example', but this should be customized. Be aware that the config file assumes the existence of the database named in 'config'.  After setup, the web app can then be run by running app.py

## How to use
To use the app, you can customize your portfolio by choosing your stocks on the left part of the screen. You can navigate the map in the middle to see e.g. where your favourite companies are located. By specifying buy and sell date and pressing 'buy', you can now see the performance of your picks. It is to be remarked upon that the app is not fuly functional at the handin-time

# A remark on the ER diagram
The ER diagram is made to accurately depict the system as implemented. 
The primary contributor to the structure of the ER diagram is the fact that 
we had to allow selection of companies through multiple avenues, all through the interface.
One will notice that companies have a state and a country attribute. Using
this as a selector could be viable, however, this did not fit our vision
for the interface. These attributes could be utilized for other features however.
The 'Handler' is a simplification of the use of temporary tables which are used for queries. 
This use of temporary features allows for modularity in our python part of the program, 
making new features easier to implement, as well as important existing features from
other programs. Examples of which would be using longitude and latitude to specify 
geographical shapes, doing pattern matching, adding aditional interface options such as 
prices, and so on. In hindsight we notice that some features could have been put into the 
SQL database, however we failed to account for this early enough during development.

Our ER diagram displays Interface, and by extension, Countries, States and Companies,
even though they are not part of the SQL database. We choose to integrate them into
the diagram as they serve as great tools to illustrate the functionality of our 
application, and because we believe that our program could ( and argueably should) 
have been made with these pieces being of the SQL database, instead of being stored 
in Python. 