from ss3dbc import *

db = Database("../db/database.sql")
db.create_table("Server", "server_name TEXT, command_prefix TEXT, im_variations TEXT, message TEXT, disabled BOOLEAN")
db.close()
