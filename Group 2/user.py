import json

class User:
    # Define the accepted roles
    ALLOWED_ROLES = {"operator", "qc_inspector", "admin"}

    def __init__(self, name, database_path=r"data_set\user_profile.json"):
        self.name = name
        # Get the user's role from the database
        self.role = self.get_role_from_database(name, database_path)

    def __str__(self):
        return f"Name: {self.name}\nRole: {self.role}"
    
    @classmethod
    def is_user_in_database(cls, name, database_path=r"data_set\user_profile.json"):
        """
        Check if the user exists in the JSON database.
        """
        try:
            with open(database_path, mode="r") as file:
                user_data = json.load(file)  # Load JSON data
                for user in user_data:
                    if user["name"].strip() == name:
                        return True
        except FileNotFoundError:
            raise FileNotFoundError(f"The database file {database_path} does not exist.")
        except json.JSONDecodeError:
            raise ValueError(f"The database file {database_path} contains invalid JSON.")
        return False
    
    @classmethod
    def get_role_from_database(cls, name, database_path=r"data_set\user_profile.json"):
        """
        Retrieve the role of a user from the JSON database.
        """
        try:
            with open(database_path, mode="r") as file:
                user_data = json.load(file)
                for user in user_data:
                    if user["name"].strip().lower() == name.lower():
                        return user["role"]  # Return the role if the user is found
        except FileNotFoundError:
            raise FileNotFoundError(f"The database file {database_path} does not exist.")
        except json.JSONDecodeError:
            raise ValueError(f"The database file {database_path} contains invalid JSON.")
        raise ValueError(f"User {name} is not an authorized user.")  # Raise error if user is not found

