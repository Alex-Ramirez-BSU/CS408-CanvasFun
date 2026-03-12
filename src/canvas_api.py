import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

#Load Dot Env File
load_dotenv()

#Getting Keys
CANVAS_API_TOKEN = os.getenv("CANVAS_API_TOKEN")
if not CANVAS_API_TOKEN:
    raise ValueError("CANVAS_API_TOKEN must be set")
headers = {"Authorization": f"Bearer {CANVAS_API_TOKEN}"}

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

    response = requests.get(url, headers=headers)
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

    response = requests.get(course_url, headers=headers)

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

#Get All Submission
def course_submissions(course_id):
    COL_WIDTH = 40

    url = f"https://boisestatecanvas.instructure.com/api/v1/courses/{course_id}/students/submissions?student_ids[]=self&include[]=assignment"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve submissions: {response.status_code}")
        return

    submissions = response.json()

    total_score = 0
    total_points = 0

    print(f"\nGrades for Course ID {course_id}")
    print(f"{'Assignment':<40} {'Score':>8} {'Possible':>10} {'Grade':>10}")
    print("-" * 70)

    for sub in submissions:
        assignment = sub.get("assignment", {})

        name = assignment.get("name", "Unknown")
        if len(name) > COL_WIDTH:
            name = name[:COL_WIDTH - 3] + "..."

        points_possible = assignment.get("points_possible", 0)

        score = sub.get("score")
        grade = sub.get("grade") or "N/A"

        if score is None:
            score = 0

        print(f"{name:<40} {score:>8} {points_possible:>10} {grade:>10}")

        if sub.get("workflow_state") == "graded":
            total_score += score
            total_points += points_possible

    percentage = (total_score / total_points * 100) if total_points > 0 else 0

    print("-" * 75)
    print(f"Total Score: {total_score}/{total_points} | Percentage: {percentage:.2f}%")

#Get All Upcoming Assignments
# def assignment_tracker(courses):
#     headers = {"Authorization": f"Bearer {CANVAS_API_TOKEN}"}
#
#     now = datetime.now(timezone.utc)
#     today = now.date()
#     week_ahead = (now + timedelta(days=7)).date()
#
#     assignments_list = []
#
#     for course in courses:
#         course_id = course['id']
#         url = f"https://boisestatecanvas.instructure.com/api/v1/courses/{course_id}/assignments"
#
#         resp = requests.get(url, headers=headers)
#         if resp.status_code != 200:
#             continue
#
#         assignments = resp.json()
#
#         for assignment in assignments:
#             print(assignment["name"], assignment["due_at"])
#
#         for assignment in assignments:
#             due = assignment.get("due_at")
#             if not due:
#                 continue
#
#             due_dt = datetime.fromisoformat(due.replace("Z", "+00:00"))
#
#             if today <= due_dt.date() <= week_ahead:
#                 days_left = (due_dt.date() - today).days
#
#                 if days_left == 0:
#                     due_in = "Today"
#                 elif days_left == 1:
#                     due_in = "Tomorrow"
#                 else:
#                     due_in = f"{days_left} days"
#
#                 assignments_list.append({
#                     "due": due_dt,
#                     "due_in": due_in,
#                     "course": course["name"],
#                     "name": assignment["name"],
#                     "points": assignment.get("points_possible", 0)
#                 })
#
#     assignments_list.sort(key=lambda x: x["due"])
#
#     print("\nUpcoming Assignments (next 7 days):")
#     print(f"{'Due In':<10} {'Course':<40} {'Assignment':<40} {'Points':>6}")
#     print("-" * 100)
#
#     for a in assignments_list:
#         course = a["course"][:37] + "..." if len(a["course"]) > 40 else a["course"]
#         name = a["name"][:37] + "..." if len(a["name"]) > 40 else a["name"]
#
#         print(f"{a['due_in']:<10} {course:<40} {name:<40} {a['points']:>6}")

def todo():
    url = f"https://boisestatecanvas.instructure.com/api/v1/users/self/todo"

    today = datetime.today()

    print(today)

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve submissions: {response.status_code}")
        return

    assignments = response.json()

    for item in assignments:
        assignment = item['assignment']
        name = assignment['name']
        due_date = datetime.strptime(assignment['due_at'][:10], "%Y-%m-%d")
        due_in_days = (due_date - today).days

        if due_in_days == 0:
            status = "DUE TODAY"
        elif due_in_days > 0:
            status = "UPCOMING"
        else:
            status = "OVERDUE"

        points = assignment['points_possible']
        print(due_in_days, name, points, status)
