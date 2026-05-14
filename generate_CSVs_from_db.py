import sqlite3
import pandas as pd
from pathlib import Path


def export_sqlite_to_csv(db_path, output_dir):
    """
    Export all tables from a SQLite database into separate CSV files.

    Args:
        db_path (str): Path to the SQLite database file.
        output_dir (str): Directory where CSV files will be stored.
    """

    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Get all table names
        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name NOT LIKE 'sqlite_%';
        """)

        tables = cursor.fetchall()

        if not tables:
            print("No tables found in the database.")
            return

        # Export each table
        for table in tables:
            table_name = table[0]

            # Read table into pandas DataFrame
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)

            # CSV file path
            csv_file = output_path / f"{table_name}.csv"

            # Export to CSV
            df.to_csv(csv_file, index=False)

            print(f"Exported: {table_name} -> {csv_file}")

        print("\nAll tables exported successfully.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        conn.close()


if __name__ == "__main__":
    # Example usage

    DATABASE_PATH = "database\\phonepe_data.db"
    OUTPUT_FOLDER = "CSVs"

    export_sqlite_to_csv(DATABASE_PATH, OUTPUT_FOLDER)
