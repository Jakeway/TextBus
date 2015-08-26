__author__ = 'jakeway'

"""This file contains all rutger's related API methods"""

import requests


def get_eta(bus_stop, bus_name):
    url = "http://runextbus.heroku.com/stop/" + bus_stop
    r = requests.get(url)
    bus_info = r.json()
    for bus in bus_info:
        if bus['title'] == bus_name:
            return bus['predictions'][0]['minutes']


class Soc:

    def __init__(self, campus='NB', semester='92014', level='U,G'):
        self.base_url = 'http://sis.rutgers.edu/soc'
        self.params = {
            'campus': campus,
            'semester': semester,
            'level': level
        }

    """ Get title of a specific course """
    def get_title(self, subject, course_number):
        subject_courses = self.get_courses(subject)
        for course in subject_courses:
            course_num = course['courseNumber']
            if course_num.isdigit():
                course_num = str(int(course_num))
            if course_num == course_number:
                return course['title']

    """ Filters out everything but section info for a particular rutgers course """
    """ All inputs have to be strings, not numbers """
    """ Example: self.get_section('016', '222', '1') """
    def get_section(self, subject, course_number, section_number):
        subject_courses = self.get_courses(subject)
        for course in subject_courses:
            course_num = course['courseNumber']
            if course_num.isdigit():
                course_num = str(int(course_num))
            if course_num == course_number:
                target_course = course
                for section in target_course['sections']:
                    section_num = section['number']
                    if section_num.isdigit():
                        section_num = str(int(section_num))
                    if section_num == section_number:
                        return section

    """After getting a section, we need a couple things."""
    """We need to get some info from meetingTimes key, i.e. section['meetingTimes']"""
    """ Need: startTime, meetingDay, campusAbbrev """
    """ Notes: meetingModeDesc might be useful, if it isn't LEC it might not even meet up (online class), so don't care about it"""

    def get_meeting_info(self, section):
        meeting_info = []
        for meeting in section['meetingTimes']:
            class_meeting = {}
            class_meeting['startTime'] = meeting['startTime']
            class_meeting['meetingDay'] = meeting['meetingDay']
            class_meeting['campus'] = meeting['campusAbbrev']
            class_meeting['pmCode'] = meeting['pmCode']
            meeting_info.append(class_meeting)
        return meeting_info

    def query(self, resource, params):
        params.update(self.params)
        r = requests.get(self.base_url + resource, params=params, headers=self.headers)
        if r.status_code == requests.codes.ok:
            return r.json()
        raise Exception('You made an invalid request %s: %s' % (r.status_code, r.text))

    def get_subjects(self, **kwargs):
        return self.query('/subjects.json', params=kwargs)

    def get_courses(self, subject):
        return self.query('/courses.json', params={'subject': subject})

    def to_military_time(self, time, pmCode):
        if pmCode == 'P':
            hour = time[:2]
            if hour == '12':
                return time
            minute = time[2:]
            hour_num = int(hour) + 12
            return str(hour_num) + minute
        else:
            return time


if __name__ == '__main__':
    s = Soc()
    sec = s.get_section('198', '344', '1')
    meeting_info = s.get_meeting_info(sec)
    for meeting in meeting_info:
        print s.to_military_time(meeting['startTime'], meeting['pmCode'])
