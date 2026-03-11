import os
import requests
from dotenv import load_dotenv

#Load Dot Env File
load_dotenv()

#Getting Keys
CANVAS_API_TOKEN = os.getenv("CANVAS_API_TOKEN")
USER_ID = "232391"

#API URL
# URL = "https://boisestatecanvas.instructure.com/api/v1/..."

#Get All Upcoming Assignments
def assignment_tracker():
    pass

#Get All Current Courses
def get_all_active_courses():
    url = "https://boisestatecanvas.instructure.com/api/v1/users/self/courses?enrollment_state=active"
    courses = []

    response = requests.get(url, headers={"Authorization": f"Bearer {CANVAS_API_TOKEN}"})
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}, {response.text[:50]}")
        return courses

    data = response.json()

    for course in data:
        course_name = course.get("name")
        course_term = course.get("enrollment_term_id")

        # Only return courses for term 223 (Spring 2026)
        if course_term == 223:
            courses.append(course)

    return courses

#Print All Current Courses
def print_all_active_courses(courses):
    for course in courses:
        print(course['name'])

def get_single_course(course_id):
    course_url = f"https://boisestatecanvas.instructure.com/api/v1/courses/{course_id}"

    response = requests.get(course_url, headers={"Authorization": f"Bearer {CANVAS_API_TOKEN}"})

    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}, {response.text[:50]}")

    course = response.json()
    print(course)