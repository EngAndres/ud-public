"""
This module contains the Observability class.

Author: Carlos Andrés Sierra <cavirguezs@udistrital.edu.co>
"""

from datetime import datetime


class Observability:
    """
    This class provides methods to log events in the system.

    Methods:
        write_user_log: This method write a log message for an user action.
        write_performance_log: This method write a log message for a performance event.
    """

    @staticmethod
    def write_user_log(user: str, message: str):
        """
        This method write a log message for an user action.

        Args:
            user_id (str): The user identifier
            message (str): The message to be logged
        """
        with open("user_log.txt", "a", encoding="utf-8") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp} - User {user}: {message}\n")

    @staticmethod
    def write_performance_log(message: str):
        """
        This method write a log message for a performance event.

        Args:
            message (str): The message to be logged
        """
        with open("performance_log.txt", "a", encoding="utf-8") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp} - {message}\n")
