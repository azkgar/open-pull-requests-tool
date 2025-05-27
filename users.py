# ---------- Define the class Users to handle all users information processing --------------- #
# Import ast library to format text file data as dictionary
import ast

# Path where the users text file will be created/read
FILE_PATH = "TextFiles/users.txt"


class Users:
    def __init__(self):
        # Variable to hold the users dictionary retrieved from the text file
        self.users_dict = {}
        # Variable to hold the users text file path
        self.file_path = FILE_PATH

    def read_file(self) -> dict:
        """Function read_file reads the users text file. If the file exists and contains data,
        converts it from text and returns it as dictionary. If the file doesn't exist, or it
        doesn't contain any data it returns an empty dictionary."""
        try:
            # Open the file when it exists
            with open(self.file_path, "r") as file:
                # Stores the file content
                file_content = file.read()
                # Returns the converted text content to dictionary or an empty dictionary
                return ast.literal_eval(file_content) if file_content else {}
        except FileNotFoundError:
            # The file doesn't exist. Returns and empty dictionary
            return {}

    def write_file(self) -> None:
        """Function write_file writes the users dictionary to the users text file as text"""
        with open(self.file_path, "w") as file:
            # Converts the dictionary to text and writes it to the users text file
            file.write(str(self.users_dict))

    def user_exists(self, github_id: str) -> bool:
        """Function user_exists receives the user ID as a parameter and returns True if the
        ID exists in the users dictionary or False if the ID is not part of the users dictionary"""
        if github_id in self.users_dict.keys():
            # The ID is part of the users dictionary
            return True
        else:
            # The ID is not part of the users dictionary
            return False

    def add_user(self) -> None:
        """Function add_user receives the user ID and the username as inputs. Calls function read_file
        to retrieve the users dictionary and then calls function user_exists to verify if the user being added
        already exists. If the user already exists it won't add the user again, if the user doesn't exist
        it will add the new user to the users dictionary"""
        # Call function to read file and retrieve the users dictionary
        self.users_dict = self.read_file()
        # Get ID from the user
        github_id = input("\nWhat's the GitHub ID? ")
        # Call function to determine if the ID already exists in the users dictionary
        if self.user_exists(github_id):
            # User already exists
            print("\nThe ID you tried to add already exists.\n")
        else:
            # Get name from the user
            user_name = input("\nWhat's the name? ")
            # Add the new user to the dictionary
            self.users_dict[github_id] = user_name
            # Call function to write the updated dictionary in the text file
            self.write_file()
            print("\nUser successfully added.\n")

    def remove_user(self) -> None:
        """Function remove_user receives the user ID as an input. Calls function read_file to
        retrieve the users dictionary and then calls function user_exists to verify if the user being
        removed is part of the dictionary. If the user exists then proceeds to remove it from the dictionary
        and writes the updated dictionary to the users text file. If the user doesn't exist it won't update
        the dictionary"""
        # Call function to read file and retrieve users dictionary
        self.users_dict = self.read_file()
        # Get ID from the user
        github_id = input("\nWhat's the GitHub ID? ")
        # Call function to determine if the ID exists in the users dictionary
        if self.user_exists(github_id):
            # Remove user from the users dictionary
            del self.users_dict[github_id]
            # Call function to write the updated dictionary in the text file
            self.write_file()
            print("\nUser successfully removed.\n")
        else:
            # User is not part of the users dictionary
            print("\nThe ID you tried to remove doesn't exist.\n")
