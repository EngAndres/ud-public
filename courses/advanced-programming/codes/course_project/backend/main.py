from db_connection import DBConnection, test_function
from products.videogames import list_videogames

connection = DBConnection()
connection.connect()

test_function()
list_videogames()
