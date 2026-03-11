import os
import requests
from dotenv import load_dotenv

#Load Dot Env File
load_dotenv()

#Getting Keys
CANVAS_API_TOKEN = os.getenv("CANVAS_API_TOKEN")
if not CANVAS_API_TOKEN:
    raise ValueError("CANVAS_API_TOKEN must be set")

# USER_ID = "232391"

#API URL
# URL = "https://boisestatecanvas.instructure.com/api/v1/..."

#Get/Display Raw Data
def get_raw_data():
    courses = get_all_active_courses()

    for course in courses:
        print(course)

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
    return course

def print_course(course):

    if not course:
        print(f"Failed to retrieve data: {course}")
        return

    print(f"Course Name: {course.get('name')}")
    print(f"Course Code: {course.get('course_code')}")
    print(f"Course ID: {course.get('id')}")
    print(f"Term ID: {course.get('enrollment_term_id')}")
    print(f"Start Date: {course.get('start_at')}")
    print(f"End Date: {course.get('end_at')}")

#Get All Upcoming Assignments
def assignment_tracker():
    pass

#Get All Submission
def course_submissions(course_id):
    headers = {"Authorization": f"Bearer {CANVAS_API_TOKEN}"}

    url = f"https://boisestatecanvas.instructure.com/api/v1/courses/{course_id}/students/submissions?student_ids[]=self&include[]=assignment"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve submissions: {response.status_code}")
        return

    submissions = response.json()

    total_score = 0
    total_points = 0

    print(f"\nGrades for Course ID {course_id}")
    print(f"{'Assignment':<50} {'Score':<10} {'Grade':<10}")
    print("-" * 75)

    for sub in submissions:
        assignment = sub.get("assignment", {})
        name = assignment.get("name", "Unknown")
        points_possible = assignment.get("points_possible", 0)

        score = sub.get("score") or 0
        grade = sub.get("grade") or "N/A"

        # if score is None:
        #     score = 0

        print(f"{name:<50} {score:<10} {grade:<10}")

        total_score += score
        total_points += points_possible

    percentage = (total_score / total_points * 100) if total_points > 0 else 0

    print("-" * 75)
    print(f"Total Score: {total_score}/{total_points} | Percentage: {percentage:.2f}%")