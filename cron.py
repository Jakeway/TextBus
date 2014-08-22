__author__ = 'jakeway'

""" This file contains the daily cron job that will poll to see if alerts need to be sent"""

##### Weekday Codes #######
  #   Monday    = 'M'  #
  #   Tuesday   = 'T'  #
  #   Wednesday = 'W'  #
  #   Thursday  = 'TH' #
  #   Friday    = 'F'  #
  #   Saturday  = 'SA' #
  #   Sunday    = 'SU' #

import time
from models import CourseAlert, User
from message import send_alert
from rutgers import get_eta


days_of_week = {
    'Monday': 'M',
    'Tuesday': 'T',
    'Wednesday': 'W',
    'Thursday': 'TH',
    'Friday': 'F',
    'Saturday': 'SA',
    'Sunday': 'SU'
}

"""Takes in the meetingDay Rutgers abbreviation and translates to unshortened day name"""


def rutgers_abbrev_to_normal_day(day_abbrev):
    for day in days_of_week:
        if day_abbrev == days_of_week[day]:
            return day

""" Return the time difference in minutes between current time and class start time."""
""" Will be positive if current time is not after the class start time (i.e. class has not yet started)"""


def get_time_difference(current_time, class_start_time):
    current_hour = current_time[:2]
    current_minute = int(current_time[2:])
    class_hour = class_start_time[:2]
    class_minute = int(class_start_time[2:])
    current_hour_num = int(current_hour)
    class_hour_num = int(class_hour)
    if current_hour_num > class_hour_num:
        # it is past class time. don't care about actual time difference.
        return -1
    minute_difference = class_minute - current_minute
    if minute_difference < 0:
        minute_difference += 60
        current_hour_num += 1
    hour_difference = class_hour_num - current_hour_num
    minute_difference += (60 * hour_difference)
    return minute_difference


def poll():
    current_day = time.strftime('%A')
    courses = CourseAlert.query.filter_by(meetingDay=current_day)
    current_time = time.strftime('%H%M')
    for course in courses:
        time_difference = get_time_difference(current_time, course.start_time)
        if course.alert_interval > time_difference > 0:
            user = User.query_filter_by(id=course.user_id).first()
            eta = get_eta(course.bus_stop, course.bus_name)
            send_alert(course.bus_name, course.bus_name, eta, user.phone_number, course.course_title)



