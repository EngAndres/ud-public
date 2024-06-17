"""
This is a simple example of a web service for Python into PacketTracer.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

from http import *
from time import *

def on_route_networks(url: str, response):
    """
    This function is called when the URL is /healthcheck.

    Args:
        url (str): The URL of the request.
        response (HTTPResponse): The response object to send data to the client.
    """
    print("Test Services")
    response.send("This is a verification about python services.")

def main():
    """This is the main function of the program."""
    HTTPServer.route("/healthcheck", on_route_networks)
    # start server on port 80
    print(HTTPServer.start(80))
    # don't let it finish
    while True:
        sleep(3600)

if __name__ == "__main__":
    main()
