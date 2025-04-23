import hashlib
import getpass # For securely getting password input

class User:
    """Represents a user in the system."""
    def __init__(self, username, hashed_password, email=None):
        self.username = username
        self.hashed_password = hashed_password
        self.email = email

    def __str__(self):
        return f"User(username='{self.username}', email='{self.email}')"

class UserManager:
    """Manages user operations like adding, authenticating, and deleting."""
    def __init__(self):
        # Using a dictionary for in-memory storage
        # Key: username, Value: User object
        self._users = {}

    def _hash_password(self, password):
        """Hashes a password using SHA-256."""
        # In a real app, use a stronger hashing library like bcrypt or Argon2
        # Also, use a unique salt per user for better security
        salt = "some_basic_salt" # WARNING: Use a unique, random salt per user in production!
        password_bytes = (password + salt).encode('utf-8')
        return hashlib.sha256(password_bytes).hexdigest()

    def add_user(self, username, password, email=None):
        """Adds a new user to the system."""
        if not username or not password:
            print("Error: Username and password cannot be empty.")
            return False
        if username in self._users:
            print(f"Error: Username '{username}' already exists.")
            return False

        hashed_password = self._hash_password(password)
        new_user = User(username, hashed_password, email)
        self._users[username] = new_user
        print(f"User '{username}' added successfully.")
        return True

    def get_user(self, username):
        """Retrieves a user by username."""
        return self._users.get(username) # Returns None if user not found

    def authenticate_user(self, username, password):
        """Checks if the provided username and password are valid."""
        user = self.get_user(username)
        if user:
            hashed_input_password = self._hash_password(password)
            if user.hashed_password == hashed_input_password:
                print(f"Authentication successful for user '{username}'.")
                return user # Return the user object on success
            else:
                print("Authentication failed: Incorrect password.")
                return None
        else:
            print(f"Authentication failed: User '{username}' not found.")
            return None

    def delete_user(self, username):
        """Deletes a user from the system."""
        if username in self._users:
            del self._users[username]
            print(f"User '{username}' deleted successfully.")
            return True
        else:
            print(f"Error: User '{username}' not found.")
            return False

    def list_users(self):
        """Lists all usernames currently in the system."""
        if not self._users:
            print("No users in the system.")
            return
        print("Current users:")
        for username in self._users:
            print(f"- {username}")

# --- Simple Command-Line Interface (CLI) ---
def main():
    user_manager = UserManager()

    while True:
        print("\n--- User Management System ---")
        print("1. Add User")
        print("2. Authenticate User")
        print("3. View User Details")
        print("4. Delete User")
        print("5. List All Users")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter username: ")
            # Use getpass for password to hide input
            password = getpass.getpass("Enter password: ")
            email = input("Enter email (optional): ")
            user_manager.add_user(username, password, email or None)
        elif choice == '2':
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            user_manager.authenticate_user(username, password)
        elif choice == '3':
            username = input("Enter username to view details: ")
            user = user_manager.get_user(username)
            if user:
                print(user)
            else:
                print(f"User '{username}' not found.")
        elif choice == '4':
            username = input("Enter username to delete: ")
            # Maybe add a confirmation step here in a real app
            user_manager.delete_user(username)
        elif choice == '5':
            user_manager.list_users()
        elif choice == '6':
            print("Exiting User Management System.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
