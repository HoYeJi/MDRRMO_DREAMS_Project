import mysql.connector
from mysql.connector import Error

# Configuration for local XAMPP/MariaDB server
# NOTE: The default XAMPP user is 'root' with no password.
#       If you set a password for 'root', update it here.
DB_CONFIG = {
    'host': '127.0.0.1',
    'database': 'MDRRMO_DREAMS_DB',
    'user': 'root', # Default XAMPP user
    'password': ''   # Default XAMPP password (usually empty)
}

def create_connection():
    """Attempts to create and return a connection to the database."""
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print(f"Successfully connected to MySQL Database: {DB_CONFIG['database']}")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def close_connection(connection):
    """Closes the active database connection if it exists."""
    if connection and connection.is_connected():
        connection.close()
        print("MySQL connection closed.")

# --- Test Connection ---
if __name__ == "__main__":
    conn = create_connection()
    if conn:
        close_connection(conn)