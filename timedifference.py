# Import date time library
from datetime import datetime, date
# Import RegEx library
import re


class Timedifference:
    def __init__(self):
        self.today = datetime.now()

    def calculate_difference(self, created_at: str) -> str:
        parsed_date = re.search(r'\d{4}-\d{2}-\d{2}', created_at)
        created_date = datetime.strptime(parsed_date.group(), "%Y-%m-%d").date()

        d0 = date(self.today.year, self.today.month, self.today.day)
        d1 = date(created_date.year, created_date.month, created_date.day)

        delta = d0 - d1

        if delta.days == 1:
            return f"{delta.days} day"
        else:
            return f"{delta.days} days"
