"""SQLite database: connect, create tables and add sample data."""

import os
import sqlite3
from app.exceptions import DatabaseError

DB_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "foodbridge.db")


def run(sql, values=()):
    """Run INSERT / UPDATE / DELETE and save the change."""
    connection = sqlite3.connect(DB_FILE)
    try:
        connection.execute(sql, values)
        connection.commit()
    except sqlite3.Error as error:
        raise DatabaseError("Database error: " + str(error))
    finally:
        connection.close()


def get_rows(sql, values=()):
    """Run SELECT and return a list of tuples."""
    connection = sqlite3.connect(DB_FILE)
    try:
        return connection.execute(sql, values).fetchall()
    except sqlite3.Error as error:
        raise DatabaseError("Database error: " + str(error))
    finally:
        connection.close()


def setup_database():
    """Create the tables if missing. Add sample records the first time."""
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    run("""CREATE TABLE IF NOT EXISTS donations (
        donation_id TEXT PRIMARY KEY, donor_name TEXT, food_name TEXT,
        category TEXT, quantity REAL, unit TEXT, expiry_date TEXT)""")
    run("""CREATE TABLE IF NOT EXISTS recipients (
        recipient_id TEXT PRIMARY KEY, name TEXT, contact TEXT, address TEXT, recipient_type TEXT)""")
    run("""CREATE TABLE IF NOT EXISTS distributions (
        distribution_id TEXT PRIMARY KEY, donation_id TEXT, recipient_id TEXT,
        quantity REAL, distribution_date TEXT)""")

    if get_rows("SELECT COUNT(*) FROM donations")[0][0] > 0:
        return

    donations = [
        ("DON-001", "Sunrise Restaurant", "Chicken Biryani", "Cooked Meal", 40, "kg", "2026-11-20"),
        ("DON-002", "Golden Crust Bakery", "Whole Wheat Bread", "Bakery", 60, "piece", "2026-11-18"),
        ("DON-003", "Fresh Mart Grocery", "Tomatoes", "Fruits & Vegetables", 25, "kg", "2026-11-22"),
        ("DON-004", "Fresh Mart Grocery", "Rice", "Grains & Staples", 100, "kg", "2027-03-01"),
        ("DON-005", "Green Valley Dairy", "Fresh Milk", "Dairy", 50, "liter", "2026-11-16"),
        ("DON-006", "Rahim Uddin", "Bottled Water", "Beverages", 120, "piece", "2027-06-30"),
        ("DON-007", "City Kitchen", "Vegetable Khichuri", "Cooked Meal", 30, "kg", "2026-11-14"),
        ("DON-008", "Happy Family Store", "Biscuit Packets", "Packaged Food", 80, "packet", "2027-01-15"),
        ("DON-009", "Golden Crust Bakery", "Sweet Buns", "Bakery", 45, "piece", "2026-11-05"),
        ("DON-010", "Sunrise Restaurant", "Lentil Soup", "Cooked Meal", 20, "liter", "2026-11-03"),
        ("DON-011", "Nasrin Akter", "Bananas", "Fruits & Vegetables", 15, "kg", "2026-11-17"),
        ("DON-012", "Fresh Mart Grocery", "Cooking Oil", "Packaged Food", 35, "liter", "2027-04-10"),
    ]
    recipients = [
        ("REC-001", "Hope Shelter", "01711000001", "Mirpur, Dhaka", "Shelter"),
        ("REC-002", "Care Charity", "01711000002", "Uttara, Dhaka", "Charity"),
        ("REC-003", "Karim Family", "01711000003", "Mohammadpur, Dhaka", "Family"),
        ("REC-004", "Green Community", "01711000004", "Dhanmondi, Dhaka", "Community Group"),
        ("REC-005", "Light of Life Shelter", "01711000005", "Gulshan, Dhaka", "Shelter"),
    ]
    distributions = [
        ("DIS-001", "DON-001", "REC-001", 15, "2026-11-10"),
        ("DIS-002", "DON-002", "REC-002", 20, "2026-11-11"),
        ("DIS-003", "DON-004", "REC-003", 10, "2026-11-12"),
        ("DIS-004", "DON-006", "REC-004", 40, "2026-11-12"),
        ("DIS-005", "DON-008", "REC-005", 30, "2026-11-13"),
    ]
    for row in donations:
        run("INSERT INTO donations VALUES (?, ?, ?, ?, ?, ?, ?)", row)
    for row in recipients:
        run("INSERT INTO recipients VALUES (?, ?, ?, ?, ?)", row)
    for row in distributions:
        run("INSERT INTO distributions VALUES (?, ?, ?, ?, ?)", row)
