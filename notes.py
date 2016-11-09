from flask import Flask
# initalize the model, view and controller. 
from model import Model
from view import View
from controller import Con
app = Flask(__name__)
## initalize each module and start the view with the others as a parameter 
modelobj = Model()
controllerobj = Con(modelobj)
viewobj  = View(app,controllerobj)
if __name__ == "__main__":
    app.run(host='0.0.0.0')
