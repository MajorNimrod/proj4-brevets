"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

SPEEDS = [
    (200, 15, 34),
    (400, 15, 32),
    (600, 15, 30),
    (1000, 11.428, 28),
    (1300, 13.333, 26),
]

# # Official final-control closing times, in hours
FINAL_CLOSE_HOURS = {200: 13.5, 300: 20, 400: 27, 600: 40, 1000: 75}

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#

def calculate_hours(control_dist_km, brevet_dist_km, which):
   """The number of hours it takes to ride control_dist_km using max open speeds."""
   # I just came back from a crew race so this is super convienent that I'm working on this haha
   dist = min(control_dist_km, brevet_dist_km)
   hours = 0
   previous_end = 0
   for end, min_speed, max_speed in SPEEDS:
      if dist <= previous_end:
         break
      speed = max_speed if which == "open" else min_speed
      hours += (min(dist, end) - previous_end) / speed # in km
      previous_end = end
   return hours

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    minutes = round(calculate_hours(control_dist_km, brevet_dist_km, "open") * 60)
    return arrow.get(brevet_start_time).shift(minutes=minutes).isoformat()


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    if control_dist_km >= brevet_dist_km:
       hours = FINAL_CLOSE_HOURS[brevet_dist_km]
    elif control_dist_km == 0:
       hours = 1
    elif control_dist_km <= 60:
       hours = control_dist_km / 20 + 1
    else:
       hours = calculate_hours(control_dist_km, brevet_dist_km, "close")
    minutes = round(hours * 60)
    return arrow.get(brevet_start_time).shift(minutes=minutes).isoformat()
