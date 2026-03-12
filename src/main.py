# Other functions, classes, and code for the module
import canvas_api as canvas

def canvas_menu():
    print("----------Welcome to Canvas Menu----------")
    print("1. Display all current classes")
    print("2. Display information about a specific class")
    print("3. Display all grades for a specific class")
    print("4. Display upcoming assignments")
    print("------------------------------------------")

    choice = int(input("Enter your choice: "))
    while choice < 1 or choice > 4:
        choice = int(input("Invalid choice, please try again: "))

    return choice

def course_menu(courses):
    counter = 1
    print("----------Pick A Course----------")
    for course in courses:
        print(f"{counter}: {course['name']}")
        counter += 1

    choice = int(input("Enter your choice: "))
    while choice < 1 or choice > counter - 1:
        choice = int(input("Invalid choice, please try again: "))

    course_id = courses[choice-1]["id"]

    return course_id


def main():
    """Main entry point of the script."""
    print("Starting Canvas CLI...")

    #Debug
    # canvas.get_raw_data()
    #End

    # Retrieving MetaData
    courses = canvas.get_all_active_courses()

    while 1:
        #Get User Input
        user_choice = canvas_menu()
        print()

        match user_choice:
            case 1:
                canvas.print_all_active_courses(courses)
            case 2:
                class_choice = course_menu(courses)
                info = canvas.get_single_course(class_choice)
                canvas.print_course(info)
            case 3:
                print(f"---------- Available Courses ----------")
                for i, course in enumerate(courses, start=1):
                    print(f"{i}. {course['name']}")
                print(f"---------------------------------------")
                course_num = int(input("Select a course number to view grades: "))
                while course_num < 1 or course_num > len(courses):
                    course_num = int(input("Invalid choice, please try again: "))
                print()
                course_id = courses[course_num-1]['id']
                canvas.course_submissions(course_id)
            case 4:
                canvas.todo()
            case _:
                print("Option Not Available")

        choice = input("Continue? [y/n]: " )
        while choice.lower() != "y" and choice.lower() != "n":
            choice = input("Invalid choice, please try again [y/n]: ")
        if choice.lower() == "n":
            break
        print()
        continue

if __name__ == "__main__":
    main() # Call the main function



