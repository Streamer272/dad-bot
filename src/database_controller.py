from json import dumps
from ss3dbc import Database


class DatabaseController:
    @staticmethod
    def create_record(server_name, im_variations, message="Hi <name>, Im Dad!", enabled=True, command_prefix="$"):
        db = Database("./db/database.sql")

        db.get_table("Server").add_record(
            f"'{server_name}', '{command_prefix}', '{dumps(im_variations)}', '{message}', {enabled}")

        db.close()

    @staticmethod
    def set_value(server_name, key, value):
        db = Database("./db/database.sql")

        db.get_table("Server").update_record(f"server_name='{server_name}'", f"{key}='{value}'")

        db.close()

    @staticmethod
    def set_status(server_name, enabled):
        db = Database("./db/database.sql")

        db.get_table("Server").update_record(f"server_name='{server_name}'", f"enabled={enabled}")

        db.close()

    @staticmethod
    def get_value(server_name, key):
        db = Database("./db/database.sql")

        return db.get_table("Server").controller.query(
            f"SELECT {key} FROM Server WHERE server_name='{server_name}'").fetchone()[0]

    @staticmethod
    def get_status(server_name):
        db = Database("./db/database.sql")

        return bool(db.get_table("Server").controller.query(
            f"SELECT enabled FROM Server WHERE server_name='{server_name}'").fetchone()[0])
