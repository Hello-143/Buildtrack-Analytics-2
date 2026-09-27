import sqlite3
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../database/buildtrack.db"))

def get_connection():
    """
    Returns a connection to the SQLite database.
    Creates the directory for the database if it doesn't exist.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    # Enable foreign keys
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """
    Initializes the SQLite database schema, resetting it if it already exists.
    """
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
            print("Resetting database: existing file removed.")
        except Exception as e:
            print(f"Warning: could not remove existing database file: {e}")
            
    conn = get_connection()
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 1. Projects Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        project_id INTEGER PRIMARY KEY,
        project_name TEXT NOT NULL,
        project_type TEXT NOT NULL,
        start_date TEXT NOT NULL,
        planned_end_date TEXT NOT NULL,
        actual_end_date TEXT,
        budgeted_cost REAL NOT NULL,
        actual_cost REAL,
        status TEXT NOT NULL
    );
    """)
    
    # 2. Material & Vendor Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS material_vendor (
        record_id INTEGER PRIMARY KEY,
        project_id INTEGER NOT NULL,
        material_type TEXT NOT NULL,
        vendor_name TEXT NOT NULL,
        ordered_qty REAL NOT NULL,
        delivered_qty REAL NOT NULL,
        wastage_pct REAL NOT NULL,
        promised_delivery_date TEXT NOT NULL,
        actual_delivery_date TEXT NOT NULL,
        on_time INTEGER NOT NULL, -- 0 or 1
        FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
    );
    """)
    
    # 3. Labour Attendance Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS labour_attendance (
        record_id INTEGER PRIMARY KEY,
        project_id INTEGER NOT NULL,
        site_name TEXT NOT NULL,
        date TEXT NOT NULL,
        workers_expected INTEGER NOT NULL,
        workers_present INTEGER NOT NULL,
        attendance_pct REAL NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
    );
    """)
    
    conn.commit()
    conn.close()
    print(f"SQLite database initialized at: {DB_PATH}")

if __name__ == "__main__":
    init_db()
