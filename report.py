# ---------- Define the class Report to format pull requests and export as a report in Excel --------------- #
# Import pandas library to export the report to Excel
import pandas as pd
# Import RegEx library to extract the Jira ticket number from the branch name
import re
# Import Users class
from users import Users
# Import Repositories class
from repositories import Repositories
# Import Github class
from github import Github
# Import Jira class
from jira import Jira
# Import Reviews class
from reviews import Reviews
# Import Time class
from timedifference import Timedifference

# Create object users for all user related actions
users = Users()
# Create object repos for all repos related actions
repos = Repositories()
# Create object github for all API requests actions
github = Github()
# Create object jira for all API requests actions
jira = Jira()
# Create object reviews for all reviews related actions
reviews = Reviews()
# Create object time for all time calculations
time = Timedifference()

# Name of the Excel file where the report will be exported
EXCEL_FILE = "PullRequestReport.xlsx"

# TODO. Add your corporate Jira Cloud URL for adding the link to the tickets
#  (https://your-company.atlassian.net/browse/)
JIRA_URL = ""

# Read the users dictionary
users_dict = users.read_file()
# Read the repositories dictionary
repos_dict = repos.read_file()


def format_as_url(url: str, text: str) -> str:
    """Function format_as_url receives the url and the text that will be displayed in the report as parameters.
    It returns a hyperlink that can be populated in an Excel file cell"""
    # Populate the Excel formula =HYPERLINK(url, description)
    return f'=HYPERLINK("{url}", "{text}")'


def format_ticket(branch_name: str) -> str:
    """Function format ticket receives the GitHub branch name and extracts the Jira ticket number using
    the REgEx library. It returns the Jira ticket number if available"""

    # Store the branch_name only if it contains numbers
    has_numbers = re.match(r'^[A-Z]+-\d+', branch_name)

    if has_numbers:
        # Extract the Jira ticket number from the branch name
        jira_ticket = re.sub(r'(\d+).*$', r'\1', has_numbers.group(0))
    else:
        # Branch doesn't include a JIRA ticket, so it won't be able to create a link
        jira_ticket = ""
    # Return the formatted Jira ticket
    return jira_ticket


def check_item(item: str) -> str:
    """Function check_item receives an item and checks if the item exists in either of the users or repos dictionary
    If the item exists it will return its value. If the item doesn't exist it will return the item"""
    if item in users_dict.keys():
        # Return the value of the item if it exists in the user dictionary
        return users_dict[item]
    elif item in repos_dict.keys():
        # Return the value of the item if it exists in the repos dictionary
        return repos_dict[item]
    else:
        # Return the item as it's not part of the user or repos dictionaries
        return item


class Report:
    def __init__(self):
        # List that contains all the formated open pull requests
        self.pull_requests_list = []

    def parse_items(self, repo):
        """Function parse_items receives the repository as a parameter and will send a GET request to the
        GitHub API. If the repo has any open Pull Request it will parse the relevant items and use them as parameters
        for building the list. If the repo doesn't have any open Pull Request it won't be part of the report"""
        # Send the request to retrieve the repo's open Pull Requests and stores the response
        response = github.get_request(repo=repo)
        # Loop through the items in the response
        for item in response:
            # Check if the response includes any open pull requests
            if item:
                # Open Pull Request found extract the items for our response
                item_branch = item["head"]["ref"]
                item_user = item["user"]["login"]
                item_repo = item["head"]["repo"]["name"]
                item_repo_url = item["head"]["repo"]["html_url"]
                item_pr = item["title"]
                item_pr_url = item["html_url"]
                item_reviews_url = item["url"]
                item_draft = item["draft"]
                item_created_at = item["created_at"]

                # Send the items to the build list function
                self.build_list(
                    branch=item_branch.upper(),
                    user=item_user,
                    repo=item_repo,
                    repo_url=item_repo_url,
                    pull_request=item_pr,
                    pull_request_url=item_pr_url,
                    reviews_url=item_reviews_url,
                    draft=item_draft,
                    created_at=item_created_at
                )

    def build_list(
            self,
            branch: str,
            user: str,
            repo: str,
            repo_url: str,
            pull_request: str,
            pull_request_url: str,
            reviews_url: str,
            draft: bool,
            created_at: str
    ):
        """Function build_list receives the branch name, user, repo, repo url, pull request title and pull request
        url as parameters. It calls format_ticket function to extract the Jira ticket from the branch name and
        check_item to ensure that the owner and repo are part of existing dictionaries. Once these checks are completed
         it will format the items in a pull request dictionary that will be appended to the pull requests list"""
        # Extract Jira ticket number from branch name
        ticket = format_ticket(branch_name=branch)
        # Check if the owner is part of the dictionary
        owner = check_item(item=user)
        # Check if the repository is part of the dictionary
        repository = check_item(repo)
        # Get the reviewers information
        reviews.get_reviewers(url=reviews_url, owner=owner)
        # Get the merge status of the pull request
        reviews.get_mergeable(url=reviews_url, draft=draft)
        # Get ticket information from Jira Cloud
        jira_cloud = jira.get_request(ticket=ticket)

        # Check if the reviewers lists are empty
        if reviews.m2 == "":
            reviews.m2 = "-"
        if reviews.m1 == "":
            reviews.m1 = "-"
        if reviews.p1 == "":
            reviews.p1 = "-"
        if reviews.p2 == "":
            reviews.p2 = "-"

        # Check if information was retrieved from Jira Cloud
        if jira_cloud is None:
            sprint = ""
        else:
            sprint = jira_cloud["fields"]["customfield_10020"][-1]["name"]

        # Build the pull request dictionary
        pull_request_dict = {
            "Jira Ticket": format_as_url(url=f"{JIRA_URL}{ticket}", text=ticket),
            "Pull Request": format_as_url(url=pull_request_url, text=pull_request),
            "Owner": owner,
            "Repo": format_as_url(url=repo_url, text=repository),
            "-2": reviews.m2,
            "-1": reviews.m1,
            "+1": reviews.p1,
            "+2": reviews.p2,
            "Status": reviews.status,
            "Aging": time.calculate_difference(created_at=created_at),
            "Sprint": sprint
        }

        # Add the pull request to the pull request list
        self.pull_requests_list.append(pull_request_dict)

        # Reset the reviewers for next pull request
        reviews.reset_reviewers()

    def export_report(self):
        """Function export_report calls function parse_items to populate the pull request list. It converts the
        pull request list to a Pandas DataFrame then it will export the DataFrame as an Excel file"""
        # Get the open pull request for all repositories in the dictionary
        for repo in repos_dict:
            self.parse_items(repo)

        # Create DataFrame from the open pull requests list
        df = pd.DataFrame(self.pull_requests_list)

        # Send the DataFrame to the Excel file
        with pd.ExcelWriter(EXCEL_FILE) as report:
            df.to_excel(report, index=False)

        # Confirm completion to user
        print("\nReport created successfully!\n")
