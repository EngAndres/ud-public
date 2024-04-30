from datetime import datetime


class Observability:

    @staticmethod
    def write_user_log(user: str, action: str):
        message = f"{datetime.now()} - User: {user} - Action: {action}\n"
        with open("log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(message)

    @staticmethod
    def write_performance_log(feature: str, performance: str):
        message = (
            f"{datetime.now()} - Feature: {feature} - Performance: {performance}\n"
        )
        with open("performance_log.txt", "a", encoding="utf-8") as performance_log_file:
            performance_log_file.write(message)
