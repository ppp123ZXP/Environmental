from flask import Flask
from gevent import pywsgi
from algotirhm.controller.watercontroller import groundwater_cal_api
from algotirhm.controller.watercontroller import facewater_cal_api
from algotirhm.controller.watercontroller import drinkwater_cal_api
from algotirhm.controller.watercontroller import ocean_cal_api
from algotirhm.controller.aircontroller import air_cal_api
from algotirhm.controller.noisecontroller import noise_cal_api
from algotirhm.controller.aircontroller import acidrain_cal_api

app = Flask(__name__)
app.register_blueprint(noise_cal_api)
app.register_blueprint(groundwater_cal_api)
app.register_blueprint(drinkwater_cal_api)
app.register_blueprint(ocean_cal_api)
app.register_blueprint(air_cal_api)
app.register_blueprint(facewater_cal_api)
app.register_blueprint(acidrain_cal_api)
app.config['JSON_AS_ASCII'] = False

if __name__ == "__main__":
    server = pywsgi.WSGIServer(('0.0.0.0', 5002), app)
    server.serve_forever()
