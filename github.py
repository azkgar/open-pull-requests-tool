# ---------- Define the class Github to handle all HTTP requests --------------- #
# Import requests library to send HTTP requests to the GitHub API
import requests

# TODO. Populate your personal Authentication GitHub Token below ("github_pat_xxxxx...")
TOKEN = ""

# GitHub API Endpoint
GITHUB_ENDPOINT = "https://api.github.com/repos"

# GitHub API Version
GITHUB_API_VERSION = "2022-11-28"

# TODO. Populate the Owner of the repositories
REPOS_OWNER = ""


def token_available() -> bool:
    """ Function token_available makes sure that the user populated their GitHub authentication token.
    It returns True if a token was populated and False if the token is missing"""
    if TOKEN == "":
        # Token was not populated
        return False
    else:
        # Token was populated
        return True


class Github:
    def __init__(self):
        # HTTP Authentication Header
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {TOKEN}",
            "X-GitHub-Api-Version": GITHUB_API_VERSION,
        }

    def get_request(self, repo: str):
        """Function get_requests calls a function to check if the authentication token was populated.
        If the token is available, uses the library requests to build a GET request and returns the response
        in JSON format. If the token is not available reminds the user to populate a valid GitHub token"""
        # Checks if there's a token populated
        token = token_available()

        if token:
            # Send the GET request to the GitHub API when a valid token is populated
            response = requests.get(
                url=f"{GITHUB_ENDPOINT}/{REPOS_OWNER}/{repo}/pulls",
                headers=self.headers
            )
            # Catch any error response
            response.raise_for_status()
            # Returns the response in JSON format
            return response.json()
        else:
            # GitHub token was not populated
            print("\nToken not found. Add your token in file github.py\n")

    def get_reviewers(self, url: str):
        """Function get_reviewers calls a function to check if the authentication token was populated.
        If the token is available, uses the library requests to build a GET request and returns the response
        in JSON format. If the token is not available reminds the user to populate a valid GitHub token"""
        # Checks if there's a token populated
        token = token_available()

        if token:
            # Send the GET request to the GitHub API when a valid token is populated
            response = requests.get(
                url=f"{url}/reviews",
                headers=self.headers
            )
            # Catch any error response
            response.raise_for_status()
            # Returns the response in JSON format
            return response.json()
        else:
            # GitHub token was not populated
            print("\nToken not found. Add your token in file github.py\n")

    def get_merge_status(self, url: str):
        """Function get_merge_status calls a function to check if the authentication token was populated.
        If the token is available, uses the library requests to build a GET request and returns the response
        in JSON format. If the token is not available reminds the user to populate a valid GitHub token"""
        # Checks if there's a token populated
        token = token_available()

        if token:
            # Send the GET request to the GitHub API when a valid token is populated
            response = requests.get(
                url=url,
                headers=self.headers
            )
            # Catch any error response
            response.raise_for_status()
            # Returns the response in JSON format
            return response.json()
        else:
            # GitHub token was not populated
            print("\nToken not found. Add your token in file github.py\n")
