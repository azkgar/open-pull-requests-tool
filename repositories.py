# ---------- Define the class Repositories to handle all repositories information processing --------------- #
# Import ast library to format text file data as dictionary
import ast

# Path where the repositories text file will be created/read
FILE_PATH = "TextFiles/repositories.txt"


class Repositories:
    def __init__(self):
        # Variable to hold the users dictionary retrieved from the text file
        self.repos_dict = {}
        # Variable to hold the repos list
        self.repos_list = list(self.repos_dict.keys())
        # Variable to hold the repos text file path
        self.file_path = FILE_PATH

    def read_file(self) -> dict:
        """Function read_file reads the repositories text file. If the file exists and contains data,
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
        """Function write_file writes the repos dictionary to the repositories text file as text"""
        with open(self.file_path, "w") as file:
            # Converts the dictionary to text and writes it to the repositories text file
            file.write(str(self.repos_dict))

    def repo_exists(self, repo: str) -> bool:
        """Function repo_exists receives the repo as a parameter and returns True if the
        repo exists in the repos dictionary or False if the repo is not part of the repos dictionary"""
        if repo in self.repos_dict.keys():
            # The repo is part of the repositories dictionary
            return True
        else:
            # The repo is not part of the repositories dictionary
            return False

    def add_repo(self) -> None:
        """Function add_repo receives the repo and the short name as inputs. Calls function read_file
        to retrieve the repositories dictionary and then calls function repo_exists to verify if the repo
        being added already exists. If the repo already exists it won't add the repo to the dictionary,
        if the repo doesn't exist it will add the new repo to the repos dictionary"""
        # Call function to read file and retrieve the repos dictionary
        self.repos_dict = self.read_file()
        # Get repo as input
        repo = input("\nWrite the name of the repo you want to add: ")
        # Call function to determine if the repo already exists in the repos dictionary
        if self.repo_exists(repo):
            # Repo already exists
            print("\nThe repo you tried to add already exists.\n")
        else:
            # Get the name that will be displayed in the report
            short_name = input("\nWrite the short name for the repo: ")
            # Add the new repo to the dictionary
            self.repos_dict[repo] = short_name
            # Call function to write the updated dictionary in the text file
            self.write_file()
            print("\nRepo successfully added.\n")

    def remove_repo(self) -> None:
        """Function remove_repo receives the repo as input. Calls function read_file to
        retrieve the repos dictionary and then calls function repo_exists to verify if the repo being
        removed is part of the dictionary. If the repo exists then proceeds to remove it from the dictionary
        and writes the updated dictionary to the repositories text file. If the repo doesn't exist it won't update
        the dictionary"""
        # Call function to read file and retrieve repos dictionary
        self.repos_dict = self.read_file()
        # Get repo as input
        repo = input("\nWrite the name of the repo you want to remove: ")
        # Call function to determine if the repo exists in the repos dictionary
        if self.repo_exists(repo):
            # Remove repo from the repos dictionary
            del self.repos_dict[repo]
            # Call function to write the updated dictionary in the text file
            self.write_file()
            print("\nRepo successfully removed.\n")
        else:
            # Repo is not part of the repos dictionary
            print("\nThe repo you tried to remove doesn't exist.\n")
