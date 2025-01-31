import logging
import sqlite3
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename="user_management.log",
    level=logging.DEBUG,
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def setup_database():
    """
    Set up the SQLite database with a Users table.
    """
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        logging.info("Database connected successfully.")
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL UNIQUE,
                Email TEXT NOT NULL UNIQUE,
                CreatedAt TEXT NOT NULL
            )
        ''')
        conn.commit()
        logging.info("Users table created or verified successfully.")
    except sqlite3.Error as e:
        logging.error("Database setup failed: %s", e)
    finally:
        conn.close()

def add_user(username, email):
    """
    Add a new user to the Users table.
    """
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO Users (Username, Email, CreatedAt) VALUES (?, ?, ?)", (username, email, timestamp))
        conn.commit()
        logging.info("Added user: %s (%s)", username, email)
    except sqlite3.IntegrityError as e:
        logging.warning("Integrity error when adding user %s: %s", username, e)
    except Exception as e:
        logging.error("Failed to add user %s: %s", username, e)
    finally:
        conn.close()

def get_users():
    """
    Retrieve all users from the Users table.
    """
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM Users")
        users = cursor.fetchall()
        logging.debug("Retrieved %d users from the database.", len(users))
        return users
    except sqlite3.Error as e:
        logging.error("Failed to retrieve users: %s", e)
        return []
    finally:
        conn.close()

def delete_user(username):
    """
    Delete a user from the Users table by username.
    """
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM Users WHERE Username = ?", (username,))
        if cursor.rowcount > 0:
            conn.commit()
            logging.info("Deleted user: %s", username)
        else:
            logging.warning("No user found with username: %s", username)
    except sqlite3.Error as e:
        logging.error("Failed to delete user %s: %s", username, e)
    finally:
        conn.close()

def main():
    """
    Main function to demonstrate logging capabilities.
    """
    # Set up the database
    logging.info("Application started.")
    setup_database()
    
    # Add users
    logging.debug("Adding users to the database.")
    add_user("john_doe", "john@example.com")
    add_user("jane_smith", "jane@example.com")
    add_user("john_doe", "duplicate@example.com")  # This should trigger a warning
    
    # Retrieve users
    logging.debug("Retrieving users from the database.")
    users = get_users()
    if users:
        logging.info("Users in the system:")
        for user in users:
            logging.info("UserID: %d, Username: %s, Email: %s, CreatedAt: %s", *user)
    else:
        logging.warning("No users found in the database.")
    
    # Delete a user
    logging.debug("Deleting a user.")
    delete_user("john_doe")
    delete_user("non_existent_user")  # This should trigger a warning
    
    # Retrieve users again
    users = get_users()
    logging.info("Remaining users:")
    for user in users:
        logging.info("UserID: %d, Username: %s, Email: %s, CreatedAt: %s", *user)
    
    logging.info("Application ended.")

if __name__ == "__main__":
    main()
