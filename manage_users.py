import database_utility as dbu
import user as us


class ManageUsers:
    def __init__(self):
        self.db = dbu.SQLite("bookstore.db")
        self.user_table = "Users"
        self.db.open()

    def add_user(self, user_email: str) -> None:
        user = self.search_user(user_email)
        if user.get_id() != None:
            return
        self.db.insert(self.user_table, {"email": user_email})
        self.db.commit()

    def remove_user(self, user_id: int) -> None:
        self.db.delete(self.user_table, "user_id = ?", (user_id,))
        self.db.commit()

    def update_user(self, User: us.User) -> None:
        self.db.update(
            self.user_table,
            {"email": User.get_email()},
            "user_id = ?",
            (User.get_id(),),
        )
        self.db.commit()

    def get_user(self, user_id: int) -> us.User:
        user = us.User()
        user_data = self.db.select(self.user_table, "user_id = ?", (user_id,))
        user.set_id(user_data[0][0])
        user.set_email(user_data[0][1])
        return user

    def load_all_users(self) -> list[us.User]:
        users = []
        user_data = self.db.select(self.user_table)
        for user in user_data:
            user_obj = us.User()
            user_obj.set_id(user[0])
            user_obj.set_email(user[1])
            users.append(user_obj)
        return users

    def search_user(self, user_email: str) -> us.User:
        user = us.User()
        user_data = self.db.select(self.user_table, "email = ?", (user_email,))
        if not user_data:
            return user
        user.set_id(user_data[0][0])
        user.set_email(user_data[0][1])
        return user

    def search(self, search_text: str) -> list[us.User]:
        users = []
        user_data = self.db.select(
            self.user_table, "email LIKE ?", (f"%{search_text}%",)
        )
        for user in user_data:
            user_obj = us.User()
            user_obj.set_id(user[0])
            user_obj.set_email(user[1])
            users.append(user_obj)
        return users

    def convert_data_to_user(self, row: dict) -> us.User:
        user = us.User()
        user.set_id(row["user_id"])
        user.set_email(row["email"])
        return user

    def convert_rows(self, rows: list[dict]) -> list[us.User]:
        users = []
        for row in rows:
            user = self.convert_data_to_user(row)
            users.append(user)
        return users
    
    def __remove_all_users(self) -> None:
        self.db.free_execute("DELETE FROM Users")
        self.db.commit()

