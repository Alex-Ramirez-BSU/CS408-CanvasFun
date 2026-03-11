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
    """Fetch all submissions for a student in a course and display grades with total and GPA estimate."""

    headers = {"Authorization": f"Bearer {CANVAS_API_TOKEN}"}

    # Step 1: Get all assignments
    assignments_url = f"https://boisestatecanvas.instructure.com/api/v1/courses/{course_id}/assignments"
    assignments_resp = requests.get(assignments_url, headers=headers)
    if assignments_resp.status_code != 200:
        print(f"Failed to retrieve assignments: {assignments_resp.status_code}")
        return

    assignments = assignments_resp.json()

    total_score = 0
    total_points = 0

    print(f"\nGrades for Course ID {course_id}:\n{'Assignment':<50} {'Score':<10} {'Grade':<10}")
    print("-" * 75)

    for assignment in assignments:
        assignment_id = assignment['id']
        assignment_name = assignment['name']
        points_possible = assignment.get('points_possible', 0)

        # Step 2: Get this student's submission
        submissions_url = f"https://boisestatecanvas.instructure.com/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions?student_ids[]=self"
        submission_resp = requests.get(submissions_url, headers=headers)

        if submission_resp.status_code != 200:
            print(f"Failed to retrieve submission for {assignment_name}")
            continue

        submission = submission_resp.json()[0]
        score = submission.get('score', 0)
        grade = submission.get('grade', 'N/A')

        print(f"{assignment_name:<50} {score:<10} {grade:<10}")

        # Accumulate for course total
        if score is not None:
            total_score += score
            total_points += points_possible

    # Step 3: Calculate course percentage
    course_percentage = (total_score / total_points) * 100 if total_points > 0 else 0

    # Step 4: Convert to estimated GPA (using common 4.0 scale)
    if course_percentage >= 93:
        gpa = 4.0
    elif course_percentage >= 90:
        gpa = 3.7
    elif course_percentage >= 87:
        gpa = 3.3
    elif course_percentage >= 83:
        gpa = 3.0
    elif course_percentage >= 80:
        gpa = 2.7
    elif course_percentage >= 77:
        gpa = 2.3
    elif course_percentage >= 73:
        gpa = 2.0
    elif course_percentage >= 70:
        gpa = 1.7
    elif course_percentage >= 67:
        gpa = 1.3
    elif course_percentage >= 63:
        gpa = 1.0
    elif course_percentage >= 60:
        gpa = 0.7
    else:
        gpa = 0.0

    print("\n" + "-" * 75)
    print(f"Total Score: {total_score}/{total_points}  |  Percentage: {course_percentage:.2f}%  |  Estimated GPA: {gpa:.2f}")