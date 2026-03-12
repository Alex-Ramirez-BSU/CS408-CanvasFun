import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
DARK_GREEN = "\033[38;5;28m"

#Load Dot Env File
load_dotenv()

#Getting Keys
CANVAS_API_TOKEN = os.getenv("CANVAS_API_TOKEN")
if not CANVAS_API_TOKEN:
    raise ValueError("CANVAS_API_TOKEN must be set")

CANVAS_BASE_URL = os.getenv("CANVAS_BASE_URL")
if not CANVAS_BASE_URL:
    raise ValueError("CANVAS_BASE_URL must be set")

headers = {"Authorization": f"Bearer {CANVAS_API_TOKEN}"}

#Get/Display Raw Data
def get_raw_data():
    courses = get_all_active_courses()

    for course in courses:
        print(course)


#Get All Current Courses
def get_all_active_courses():
    data = canvas_endpoint("/api/v1/users/self/courses?enrollment_state=active")
    courses = []

    for course in data:
        course_term = course.get("enrollment_term_id")
        # Only return courses for term 223 (Spring 2026)
        if course_term == 223:
            courses.append(course)

    return courses


#Print All Current Courses
def print_all_active_courses(courses):
    print(f"{BOLD}---------- Displaying all current courses ----------{RESET}")
    for course in courses:
        print(course['name'])
    print(f"{BOLD}-{RESET}" * 52)


def get_single_course(course_id):
    course = canvas_endpoint(f"/api/v1/courses/{course_id}")
    return course


def print_course(course):
    print(f"{BOLD}---------- Displaying information about a specific class ----------{RESET}")
    if not course:
        print(f"Failed to retrieve data: {course}")
        return

    print(f"{BOLD}Course Name:{RESET} {course.get('name')}")
    print(f"{BOLD}Course Code:{RESET} {course.get('course_code')}")
    print(f"{BOLD}Course ID:{RESET} {course.get('id')}")
    print(f"{BOLD}Term ID:{RESET} {course.get('enrollment_term_id')}")
    print(f"{BOLD}Start Date:{RESET} {course.get('start_at')}")
    print(f"{BOLD}End Date:{RESET} {course.get('end_at')}")
    print(f"{BOLD}-{RESET}" * 67)


#Get All Submission
def course_submissions(course_id):
    col_width = 40

    submissions = canvas_endpoint(f"/api/v1/courses/{course_id}/students/submissions?student_ids[]=self&include[]=assignment")

    total_score = 0
    total_points = 0

    print(f"\nGrades for Course ID {course_id}")
    print(f"{BOLD}{'Assignment':<40} {'Score':>8} {'Possible':>10} {'Grade':>10}{RESET}")
    print("-" * 70)

    for sub in submissions:
        assignment = sub.get("assignment", {})

        name = assignment.get("name", "Unknown")
        if len(name) > col_width:
            name = name[:col_width - 3] + "..."

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
    print(f"{BOLD}Total Score: {total_score}/{total_points} | Percentage: {percentage:.2f}%{RESET}")


def todo():
    today = datetime.today()
    overdue = []
    upcoming = []

    assignments = canvas_endpoint("/api/v1/users/self/todo")

    for item in assignments:
        assignment = item['assignment']
        course_name = item.get('context_name', 'Unknown Course')
        if " - " in course_name:
            course_name = course_name.split(" - ", 1)[1]  # keeps everything after the first " - "
        name = assignment['name']
        points = assignment['points_possible']
        due_date = datetime.strptime(assignment['due_at'][:10], "%Y-%m-%d")
        due_in_days = (due_date - today).days

        entry = {
            "course": course_name,
            "assignment": name,
            "points": points,
            "due_in_days": due_in_days,
        }

        if due_in_days > 0:
            upcoming.append(entry)
        else:
            overdue.append(entry)

    # --- Print Upcoming Assignments ---
    if overdue:
        print(f"\n{BOLD}{RED}Overdue Assignments{RESET}")
        print_todo(overdue, overdue=True)
    else:
        print(f"{BOLD}\nNo overdue assignments!{RESET}")

    # --- Print Upcoming Assignments ---
    if upcoming:
        print(f"\n{BOLD}{CYAN}Upcoming Assignments{RESET}")
        print_todo(upcoming, overdue=False)
    else:
        print(f"\n{BOLD}No upcoming assignments!{RESET}")


def print_todo(todo_items, overdue=False):
    col_width_course = 35
    col_width_assignment = 40

    line_width = col_width_course + col_width_assignment + 20
    print("-" * line_width)

    # Header
    if overdue:
        header = f"{BOLD}{'Days Late':<10} {'Course':<{col_width_course}} {'Assignment':<{col_width_assignment}} {'Points':>6}{RESET}"
    else:
        header = f"{BOLD}{'Due In':<10} {'Course':<{col_width_course}} {'Assignment':<{col_width_assignment}} {'Points':>6}{RESET}"
    print(header)
    print("-" * line_width)

    for a in todo_items:
        # Truncate long names
        course = (a['course'][:col_width_course - 3] + "...") if len(a['course']) > col_width_course else a['course']
        assignment = (a['assignment'][:col_width_assignment - 3] + "...") if len(a['assignment']) > col_width_assignment else a['assignment']

        if overdue:
            days_late = abs(a['due_in_days'])
            due_text = f"{RED}{days_late} day{'s' if days_late != 1 else ''}{RESET}"
        else:
            if a['due_in_days'] == 0:
                due_text = f"{YELLOW}Today{RESET}"
            elif a['due_in_days'] == 1:
                due_text = f"{GREEN}1 day{RESET}"
            else:
                due_text = f"{DARK_GREEN}{a['due_in_days']} days{RESET}"

        print(f"{due_text:<19} {course:<{col_width_course}} {assignment:<{col_width_assignment}} {a['points']:>6}")

    print("-" * line_width)


def canvas_endpoint(endpoint):
    url = f"{CANVAS_BASE_URL}{endpoint}"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Canvas API error {response.status_code}: {response.text[:100]}")

    return response.json()