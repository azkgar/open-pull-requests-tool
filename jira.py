# ---------- Define the class Jira to handle all HTTP requests --------------- #
# Import requests library to send HTTP requests to the Jira Cloud API
import requests
# Import HTTPBasicAuth from requests library to authenticate the API request
from requests.auth import HTTPBasicAuth

# TODO. Populate your personal Authentication Jira Cloud Token below ("ATAxxxxx...")
TOKEN = ""

# TODO. Populate your corporate email (user@company.com)
USER = ""

# TODO. Populate your Jira Cloud API Endpoint (https://your-company.atlassian.net/rest/api)
JIRA_ENDPOINT = ""

# TODO. Populate latest Jira Cloud API version
JIRA_API_VERSION = 3

# TODO. Populate your company proxies to avoid VPN request timeout error
PROXIES = {
    "http": "http://dcproxy.company.com:##",
    "https": "http://dcproxy.company.com:##",
}


def token_available() -> bool:
    """ Function token_available makes sure that the user populated their Jira Cloud authentication token.
    It returns True if a token was populated and False if the token is missing"""
    if TOKEN == "":
        # Token was not populated
        return False
    else:
        # Token was populated
        return True


class Jira:
    def __init__(self):
        # HTTP Authentication
        self.auth = HTTPBasicAuth(USER, TOKEN)
        # HTTP Header
        self.headers = {
            "Accept": "application/json",
        }

    def get_request(self, ticket: str):
        """Function get_requests calls a function to check if the authentication token was populated.
        If the token is available, uses the library requests to build a GET request and returns the response
        in JSON format. If the token is not available reminds the user to populate a valid Jira Cloud token"""
        # Checks if there's a token populated
        token = token_available()

        if token:
            try:
                # Send the GET request to the GitHub API when a valid token is populated
                response = requests.get(
                    url=f"{JIRA_ENDPOINT}/{JIRA_API_VERSION}/issue/{ticket}",
                    headers=self.headers,
                    auth=self.auth,
                )
                # Catch any error response
                response.raise_for_status()
                # Returns the response in JSON format
                return response.json()
            # Catch any error with the Jira Cloud API
            except requests.exceptions.RequestException as e:
                # print(f"Jira Cloud request error: {e}")
                return None
        else:
            # GitHub token was not populated
            print("\nToken not found. Add your token in file jira.py\n")
