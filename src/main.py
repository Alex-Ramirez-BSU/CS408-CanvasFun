# Other functions, classes, and code for the module
import canvas_api

def canvas_menu():
    print("----------Welcome to Canvas Menu----------")
    print("1. Display all current classes")
    print("2. Display information about a specific class")
    print("3. Display all current grades")
    print("4. Display upcoming assignments")
    print("------------------------------------------")

    choice = int(input("Enter your choice: "))
    while choice < 1 or choice > 4:
        choice = input("Invalid choice, please try again: ")

    return choice

def main():
    """Main entry point of the script."""
    print("Starting Canvas CLI...")

    # Retrieving MetaData
    courses = canvas_api.get_all_active_courses()

    #Get User Input
    user_choice = canvas_menu()

    match user_choice:
        case 1:
            print("-----Displaying all current classes-----")
            canvas_api.print_all_active_courses(courses)
        # case 2:



    # canvas_api.get_all_active_courses()
    # # canvas_api.get_single_course(46080) # enrollment_term_id = 223
    # canvas_api.print_all_active_courses()

if __name__ == "__main__":
    main() # Call the main function



