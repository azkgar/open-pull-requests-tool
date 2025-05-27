# ---------- Define the class Reviews to handle information related to the Pull Requests reviews --------------- #
# Import requests library to send HTTP requests to the GitHub API

# Import class Github
from github import Github
# Import class Users
from users import Users

# Create object users from Users
users = Users()
# Create object github from Github
github = Github()

# Store the users dictionary
users_dict = users.read_file()


def check_item(item: str) -> str:
    """Function check_item receives an item and checks if the item exists in either of the users or repos dictionary
    If the item exists it will return its value. If the item doesn't exist it will return the item"""
    if item in users_dict.keys():
        # Return the value of the item if it exists in the user dictionary
        return users_dict[item]
    else:
        # Return the item as it's not part of the user or repos dictionaries
        return item

class Reviews:
    def __init__(self):
        self.p1 = ""
        self.p2 = ""
        self.m1 = ""
        self.m2 = ""
        self.status = ""

    def get_reviewers(self, url: str, owner: str):
        reviewers = github.get_reviewers(url=url)
        for reviewer in reviewers:
            if reviewer:
                owner = owner
                reviewer_name = check_item(reviewer["user"]["login"])
                state = reviewer["state"]
                self.order_reviewers(
                    reviewer_name=reviewer_name,
                    state=state
                )
        self.set_review_status(owner=owner)

    def get_mergeable(self, url: str, draft: bool):
        merge_state = github.get_merge_status(url=url)
        mergeable = merge_state["mergeable"]
        rebaseable = merge_state["rebaseable"]
        mergeable_state = merge_state["mergeable_state"]
        self.define_merge(
            mergeable=mergeable,
            rebaseable=rebaseable,
            mergeable_state=mergeable_state,
            draft=draft
        )

    def order_reviewers(self, reviewer_name: str, state: str):
        if state == "COMMENTED":
            self.m1 = reviewer_name
        elif state == "APPROVED" and len(self.p1) > 0:
            self.p2 = reviewer_name
        elif state == "APPROVED":
            self.p1 = reviewer_name
        elif state == "CHANGES_REQUESTED":
            self.m2 = reviewer_name

    def define_merge(self, mergeable: bool, rebaseable: bool, mergeable_state: str, draft: bool):
        if draft:
            self.status = "✍️ Work in progress. Don't review"
        elif not mergeable:
            self.status = "💥 Merge conflict"
        elif mergeable_state == "dirty":
            self.status = "💥 Merge conflict"
        # elif rebaseable:
        # self.status = "🗘 Rebase required"
        elif mergeable_state == "behind":
            self.status = "🔄 Rebase required"
        # elif mergeable_state == "blocked":
            # self.status = "😵 Build failed..."

    def reset_reviewers(self):
        self.p1 = ""
        self.p2 = ""
        self.m1 = ""
        self.m2 = ""

    def set_review_status(self, owner: str):
        if self.m2:
            self.status = f"❌ {owner} to update task"
        elif self.p2:
            self.status = "✅ Ready to Merge"
        elif self.m1:
            self.status = f"💭 {owner} to check comments"
        elif self.p1:
            self.status = "👀 Needs 1 review"
        else:
            self.status = "👀 Needs reviewers"
