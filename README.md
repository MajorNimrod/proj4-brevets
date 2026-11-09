# Project 4: Brevet time calculator with Ajax

Reimplement the RUSA ACP controle time calculator with flask and ajax.

Credits to Michal Young for the initial version of this code.

This is a Flask & AJAX version of the RUSA ACP controle time calculator. (https://rusa.org/octime_acp.html)

Enter control distances in km or miles and then it will update open and close times.

**Author** Jake House - Jhouse@uoregon.edu
**Repo** https://github.com/MajorNimrod/proj4-brevets

### To run it:

Make sure you are in /brevets

**Running it**
docker build -t brevets .
docker run -p 5000:5000 brevets

then open up http://localhost:5000

Check out the tests in brevets/test_acp_times.py. 

### The rules
Since RUSA rules are ambigious, I provided both open and close time calculations.

Generally speaking:
- **Open Time** = the sum over each segement at each control reach divided by the max cycling speed.
- **Close Time** = the sum using the minimum speed at each control.

*Note that results are rounded to the nearest minute and added to the start time. Time-zones are accounted for. (note to grader, this was a sneaky evil bug that I had to do integration testing for. yay)*

### Files

- `brevets/acp_times.py`: `open_time` and `close_time`
- `brevets/flask_brevets.py`: the Flask app; `/_calc_times` is the AJAX endpoint
- `brevets/templates/calc.html`: the page and its JavaScript
- `brevets/test_acp_times.py`: the test suite