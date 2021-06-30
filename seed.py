from ss3dbc import *

with open("./db/database.sql", "w") as file:
    file.write("")

db = Database("./db/database.sql")
db.create_table("server",
                "server_name TEXT, command_prefix TEXT, im_variations TEXT, rekts TEXT, message TEXT, enabled BOOLEAN")
db.create_table("rekt", "server_id INT, name TEXT, on_message TEXT, response TEXT")
db.close()
