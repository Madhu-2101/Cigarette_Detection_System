import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv()) 
# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': os.getenv('password'),
    'database': 'cigarette_tracking_database'
}

def create_connection():
    """Create a database connection."""
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def insert_brand_count(brand_name, current_count):
    """Insert or update the brand count in the Brands table."""
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO Brands (brand_name, current_count) VALUES (%s, %s) "
            "ON DUPLICATE KEY UPDATE current_count = %s",
            (brand_name, current_count, current_count)
        )
        connection.commit()
    except Error as e:
        connection.rollback()
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        connection.close()

def log_removal(brand_name, count_before_removal,  removed_count, count_after_removal):
    """Log the removal event in the RemovalLogs table."""
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id FROM Brands WHERE brand_name = %s", (brand_name,))
        brand_id = cursor.fetchone()

        if brand_id:
            brand_id = brand_id[0]

            cursor.execute(
                "INSERT INTO RemovalLogs (brand_id, count_before_removal, removed_count, count_after_removal) VALUES (%s, %s, %s, %s)",
                (brand_id, count_before_removal, removed_count, count_after_removal)
            )
            connection.commit()
        else:
            print(f"No brand found for {brand_name}")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        connection.close()

def fetch_removal_logs():
    """Fetch removal logs from the RemovalLogs table."""
    connection = create_connection()
    cursor = connection.cursor()
    removal_logs = []
    try:
        cursor.execute("""
            SELECT b.brand_name as brand, r.count_before_removal, r.removed_count, r.removal_time, r.count_after_removal 
            FROM RemovalLogs r 
            JOIN Brands b ON r.brand_id = b.id
            ORDER BY r.removal_time DESC
        """)
        rows = cursor.fetchall()
        for row in rows:
            log_entry = {
                "brand": row[0],
                "count_before_removal": row[1],
                "removed_count": row[2],
                "removal_time": row[3],
                "count_after_removal": row[4]
            }
            removal_logs.append(log_entry)
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        connection.close()
    return removal_logs

def fetch_current_counts():
    """Fetch the current counts for each brand."""
    connection = create_connection()
    cursor = connection.cursor()
    current_counts = []
    try:
        cursor.execute("SELECT * FROM Brands")
        rows = cursor.fetchall()
        for row in rows:
            log_entry = {
                "brand_id": row[0],
                "brand": row[1],
                "current_count": row[2],
                "last_updated_time": row[3]
            }
            current_counts.append(log_entry)
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        connection.close()
    return current_counts





