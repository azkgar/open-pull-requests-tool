# Import class Users
from users import Users
# Import class Repositories
from repositories import Repositories
# Import class Report
from report import Report

# Create object users for all users related actions
users = Users()
# Create object repos for all repos related actions
repos = Repositories()
# Create object report for exporting the report
report = Report()

# Set flag to keep the program running to True
is_on = True

# While the program is running
while is_on:
    # Show actions list and capture user's choice
    choice = input("\nPick one option from the list:\n"
                   "\n1) Add new user\n"
                   "2) Remove existing user\n"
                   "3) Add new repo\n"
                   "4) Remove existing repo\n"
                   "5) Create open pull requests report\n"
                   "6) Exit\n"
                   "\nType the number of the action you selected: ").lower()
    # Add user
    if choice == "1":
        # Call function to add user. User will be added if the ID is not part of the users dictionary
        users.add_user()

    # Remove user
    elif choice == "2":
        # Call function to remove user. User will be removed if the ID is part of the users dictionary
        users.remove_user()

    # Add repo
    elif choice == "3":
        # Call function to add repo. Repo will be added if it's not part of the repos dictionary
        repos.add_repo()

    # Remove repo
    elif choice == "4":
        # Call function to remove repo. Repo will be removed if it's part of the repos dictionary
        repos.remove_repo()

    # Create report
    elif choice == "5":
        # Call function to create the open Pull Requests report
        report.export_report()

    # Exit program
    elif choice == "6":
        # Confirm exit to user
        print("\nHave a great day!\n")
        # Turn off the program
        is_on = False

    else:
        # User picked an invalid option. Asking for a valid option
        print("\nOption not valid. Choose one option from the list\n")
