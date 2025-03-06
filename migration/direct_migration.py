import sqlite3
import os

def migrate_database():
    # Look for the database file in common locations
    possible_paths = [
        'users.db',
        'instance/users.db',
        '../users.db',
        './users.db'
    ]
    
    db_path = None
    for path in possible_paths:
        if os.path.exists(path):
            db_path = path
            print(f"Found database at: {path}")
            break
    
    if not db_path:
        print("Database file not found! Please run your app first to create it.")
        return

    print("Starting direct database migration...")

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get existing columns
    cursor.execute("PRAGMA table_info(user)")
    existing_columns = [col[1] for col in cursor.fetchall()]
    print(f"Existing columns: {existing_columns}")
    
    # Define columns to add - make sure names match your model exactly
    columns_to_add = [
        ("bio", "TEXT"),
        ("song_picture", "VARCHAR(128)"),
        ("sotd_title", "VARCHAR(128)"),
        ("sotd_artist", "VARCHAR(128)"),
        ("_favorite_songs", "TEXT")
    ]
    
    # Add missing columns
    for col_name, col_type in columns_to_add:
        if col_name not in existing_columns:
            try:
                sql = f"ALTER TABLE user ADD COLUMN {col_name} {col_type}"
                print(f"Executing: {sql}")
                cursor.execute(sql)
                print(f"Added column: {col_name}")
            except sqlite3.Error as e:
                print(f"Error adding column {col_name}: {e}")
        else:
            print(f"Column {col_name} already exists")
    
    # Commit changes
    conn.commit()
    
    # Verify columns were added
    cursor.execute("PRAGMA table_info(user)")
    final_columns = [col[1] for col in cursor.fetchall()]
    print(f"Final columns: {final_columns}")
    
    # Close connection
    conn.close()
    print("Migration completed")

if __name__ == "__main__":
    migrate_database()