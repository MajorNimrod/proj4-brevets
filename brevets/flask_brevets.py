"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY
VALID_BREVETS = (200, 300, 400, 600, 1000)

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    # app.logger.debug("km={}".format(km))
    # app.logger.debug("request.args: {}".format(request.args))
    brevet_dist = request.args.get('brevit_dist_km', 200, type=int)
    begin_time = request.args.get('begin_time', type=str)
    
    if km is None or km < 0:
        return flask.jsonify(result={"ERR": "Please enter a non-negative distance"})
    if brevet_dist not in VALID_BREVETS:
        return flask.jsonify(result={"ERR": "Invalid brevet distance"})
    try:
        arrow.get(begin_time)
    except Exception:
        return flask.jsonify(result={"ERR": "Invalid start date & time"})
    if km > brevet_dist * 1.2:
        return flask.jsonify(
            result={"ERR": "Control is more than 20% beyond the {}km brevet".format(brevet_dist)})

    open_time = acp_times.open_time(km, brevet_dist, begin_time)
    close_time = acp_times.close_time(km, brevet_dist, begin_time)
    return flask.jsonify(result={"open": open_time, "close": close_time})


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
