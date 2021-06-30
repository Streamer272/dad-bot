from json import dumps as dump_json
from ss3dbc import Database


class DatabaseController:
    # server management
    @staticmethod
    def create_server(
            server_name,
            im_variations=None,
            rekts=None,
            message="Hi <name>, Im Dad!",
            enabled=True,
            command_prefix="$"
    ):
        if not rekts:
            rekts = []
        if not im_variations:
            im_variations = []

        db = Database("./db/database.sql")

        db.get_table("server").add_record(
            f"'{server_name}', '{command_prefix}', '{dump_json(im_variations)}', '{dump_json(rekts)}', '{message}',{enabled}"
        )

        db.close()

    @staticmethod
    def set_server_value(server_name, key, value):
        db = Database("./db/database.sql")

        db.get_table("server").update_record(f"server_name='{server_name}'", f"{key}='{value}'")

        db.close()

    @staticmethod
    def set_server_status(server_name, enabled):
        db = Database("./db/database.sql")

        db.get_table("server").update_record(f"server_name='{server_name}'", f"enabled={enabled}")

        db.close()

    @staticmethod
    def get_server_value(server_name, key):
        db = Database("./db/database.sql")

        return db.get_table("server").controller.query(
            f"SELECT {key} FROM server WHERE server_name='{server_name}'").fetchone()[0]

    @staticmethod
    def get_server_status(server_name):
        db = Database("./db/database.sql")

        return bool(db.get_table("server").controller.query(
            f"SELECT enabled FROM server WHERE server_name='{server_name}'").fetchone()[0])

    # rekt management
    @staticmethod
    def get_server_id_by_server_name(server_name):
        db = Database("./db/database.sql")

        id = None
        for line in db.get_table("server").data:
            if line.data["server_name"] == server_name:
                id = line.id

        if id is None:
            raise TypeError(f"Couldn't find server with name {server_name}")

        return id

    @staticmethod
    def create_rekt(
            server_name,
            name,
            on_message,
            response
    ):
        db = Database("./db/database.sql")

        id = DatabaseController.get_server_id_by_server_name(server_name)

        db.get_table("rekt").add_record(
            f"{id}, '{name}', '{on_message}', '{response}'"
        )

        db.close()

    @staticmethod
    def set_rekt_value(server_name, rekt_name, key, value):
        db = Database("./db/database.sql")

        id = DatabaseController.get_server_id_by_server_name(server_name)

        db.get_table("rekt").update_record(f"server_id='{id}' AND name='{rekt_name}'", f"{key}='{value}'")

        db.close()

    @staticmethod
    def get_rekt_value(server_name, rekt_name, key):
        db = Database("./db/database.sql")

        id = DatabaseController.get_server_id_by_server_name(server_name)

        return db.get_table("rekt").controller.query(
            f"SELECT {key} FROM rekt WHERE server_id='{id}' AND name='{rekt_name}'").fetchone()[0]

    @staticmethod
    def get_all_rekts(server_name):
        db = Database("./db/database.sql")

        id = DatabaseController.get_server_id_by_server_name(server_name)

        rekts = []
        for line in db.get_table("rekt").data:
            if line.data["server_id"] == id:
                rekts.append(line.data)

        return rekts
