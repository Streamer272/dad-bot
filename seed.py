from ss3dbc import *


file = open("./db/database.sql", "wb")
file.write(b"")
file.close()

db = Database("./db/database.sql")
db.create_table("Server", "server_name TEXT, command_prefix TEXT, im_variations TEXT, message TEXT, enabled BOOLEAN")
db.close()
