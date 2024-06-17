"""
This file contains the classes and methods to manage the news of the application.

Author: Carlo A. Sierra <cavirguezs@udistrital.edu.co>
"""

from pydantic import BaseModel

class News(BaseModel):
    """This class represents the behavior of a news."""

    name: str
    publish_date: str
    description: str
    deadline: int
    status: str

    def is_activate(self, current_date: str) -> bool:
        """
        This method is used to know if a news is active or not.

        Args:
            current_date (str): the current date.

        Returns:
            bool: True if the news is active, False otherwise.
        """
        return current_date < self.deadline

    def __str__(self):
        return f"{self.name} ({self.publish_date}):\n {self.description}"
