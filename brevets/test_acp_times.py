"""Nose tests for acp_times.py

uses nosetests
"""

import arrow
import acp_times

# I went with default start time in calc.html
START = "2017-01-01T00:00:00+00:00"

def at(hours, minutes=0, start=START):
    """ISO string for `start` + hours:minutes (hours may exceed 24)."""
    return arrow.get(start).shift(hours=hours, minutes=minutes).isoformat()

def opens(control, brevet, start=START):
    return arrow.get(acp_times.open_time(control, brevet, start)).isoformat()

def closes(control, brevet, start=START):
    return arrow.get(acp_times.close_time(control, brevet, start)).isoformat()

# 200 km brevet. Controls are at 60/120/175.
def test_open_within_first_segment():
    assert opens(60, 200) == at(1, 46)
    assert opens(120, 200) == at(3, 32)
    assert opens(175, 200) == at(5, 9)

# same as first one with closing times
def test_close_within_first_segment():
    assert closes(60, 200) == at(4, 0)
    assert closes(120, 200) == at(8, 0)
    assert closes(175, 200) == at(11, 40)

# start closes 1 hr after open
def test_start_control_times():
    assert opens(0, 200) == at(0, 0)
    assert closes(0, 200) == at(1, 0)

# testing controle (the first 60)
def test_french_rule_first_60km():
    assert closes(20, 200) == at(2, 0)
    assert closes(30, 200) == at(2, 30)
    assert opens(30, 200) == at(0, 53)

# 200/15 would be 13:20. Official lim is 13:30, so 10 sec buffer.
# Similar to how crew does it
def test_final_control_200_official_lim():
    assert opens(200, 200) == at(5, 53)
    assert closes(200, 200) == at(13, 30)
    
def test_final_control_at_brevet_length():
    assert opens(300, 300) == at(9, 0)
    assert closes(300, 300) == at(20, 0)
    assert opens(400, 400) == at(12, 8)
    assert closes(400, 400) == at(27, 0)
    assert opens(600, 600) == at(18, 48)
    assert closes(600, 600) == at(40, 0)
    assert opens(1000, 1000) == at(33, 5)
    assert closes(1000, 1000) == at(75, 0)
    
# Accounting for extra
def test_control_with_extra_past_final_control():
    assert opens(205, 200) == opens(200, 200)
    assert closes(205, 200) == closes(200, 200)
    assert closes(240, 200) == at(13, 30)
    
def test_multi_segment_at_600():
    # 550 km = 550/15 close
    assert opens(550, 600) == at(17, 8)
    assert closes(550, 600) == at(36, 40)
    
def test_multi_segment_at_1000():
    assert opens(700, 1000) == at(22, 22)
    assert closes(700, 1000) == at(48, 45)
    
def test_segment_boundary_not_double_counted():
    assert opens(400, 400) != at(11, 46)
    assert opens(200, 300) == at(5, 53)
    assert closes(200, 300) == at(13, 20)

def test_timezone_preserved_and_start_offset_applied():
    start = "2017-01-01T06:00:00-08:00"
    assert opens(60, 200, start) == "2017-01-01T07:46:00-08:00"
    assert closes(60, 200, start) == "2017-01-01T10:00:00-08:00"
    
def test_rolls_over_midnight_and_month():
    start = "2017-01-31T20:00:00+00:00"
    assert closes(200, 200, start) == "2017-02-01T09:30:00+00:00"
    