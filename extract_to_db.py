"""
PhonePe Data Analysis - JSON to SQLite Extractor
=================================================
Reads all JSON files from the `data` folder and populates
9 SQLite tables inside `database/phonepe_data.db`.
"""

import os
import json
import sqlite3
import traceback

# ─────────────────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")

DATABASE_DIR = os.path.join(BASE_DIR, "database")

DB_PATH = os.path.join(
    DATABASE_DIR,
    "phonepe_data.db"
)

os.makedirs(DATABASE_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────

def load_json(path: str):

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception as exc:

        print(f"[WARN] Could not read {path}: {exc}")

        return None


def iter_year_quarter(root: str):

    if not os.path.isdir(root):
        return

    for year in sorted(os.listdir(root)):

        year_path = os.path.join(root, year)

        if not os.path.isdir(year_path):
            continue

        if not year.isdigit():
            continue

        for fname in sorted(os.listdir(year_path)):

            if not fname.endswith(".json"):
                continue

            quarter = int(
                os.path.splitext(fname)[0]
            )

            yield (
                int(year),
                quarter,
                os.path.join(year_path, fname)
            )


def iter_states(state_root: str):

    if not os.path.isdir(state_root):
        return

    for state in sorted(os.listdir(state_root)):

        state_path = os.path.join(state_root, state)

        if not os.path.isdir(state_path):
            continue

        for year, quarter, jpath in iter_year_quarter(state_path):

            yield (
                state,
                year,
                quarter,
                jpath
            )

# ─────────────────────────────────────────────────────────
# DATABASE SCHEMA
# ─────────────────────────────────────────────────────────

CREATE_STATEMENTS = """

CREATE TABLE IF NOT EXISTS Aggregated_insurance (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    State TEXT,
    Year INTEGER,
    Quarter INTEGER,

    Transaction_type TEXT,
    Transaction_count INTEGER,
    Transaction_amount REAL
);

CREATE TABLE IF NOT EXISTS Aggregated_transaction (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    State TEXT,
    Year INTEGER,
    Quarter INTEGER,

    Transaction_type TEXT,
    Transaction_count INTEGER,
    Transaction_amount REAL
);

CREATE TABLE IF NOT EXISTS Aggregated_user (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    State TEXT,
    Year INTEGER,
    Quarter INTEGER,

    Registered_users INTEGER,
    App_opens INTEGER,

    User_brand TEXT,
    User_count INTEGER,
    User_percentage REAL
);

CREATE TABLE IF NOT EXISTS Map_insurance (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    State TEXT,
    Year INTEGER,
    Quarter INTEGER,

    District TEXT,

    Transaction_count INTEGER,
    Transaction_amount REAL
);

CREATE TABLE IF NOT EXISTS Map_map (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    State TEXT,
    Year INTEGER,
    Quarter INTEGER,

    District TEXT,

    Transaction_count INTEGER,
    Transaction_amount REAL
);

CREATE TABLE IF NOT EXISTS Map_user (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    State TEXT,
    Year INTEGER,
    Quarter INTEGER,

    District TEXT,

    Registered_users INTEGER,
    App_opens INTEGER
);

CREATE TABLE IF NOT EXISTS Top_insurance (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    State TEXT,
    Year INTEGER,
    Quarter INTEGER,

    Entity_type TEXT,
    Entity_name TEXT,

    Transaction_count INTEGER,
    Transaction_amount REAL
);

CREATE TABLE IF NOT EXISTS Top_map (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    State TEXT,
    Year INTEGER,
    Quarter INTEGER,

    Entity_type TEXT,
    Entity_name TEXT,

    Transaction_count INTEGER,
    Transaction_amount REAL
);

CREATE TABLE IF NOT EXISTS Top_user (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    State TEXT,
    Year INTEGER,
    Quarter INTEGER,

    Entity_type TEXT,
    Entity_name TEXT,

    Registered_users INTEGER
);

"""

# ══════════════════════════════════════════════════════════
# AGGREGATED INSURANCE
# ══════════════════════════════════════════════════════════

def extract_aggregated_insurance(cur):

    print("\n[1/9] Aggregated_insurance")

    rows = []

    root = os.path.join(
        DATA_DIR,
        "aggregated",
        "insurance",
        "country",
        "india"
    )

    # INDIA LEVEL

    for year, quarter, jpath in iter_year_quarter(root):

        data = load_json(jpath)

        if not data:
            continue

        for tx in data.get("data", {}).get("transactionData", []):

            for pi in tx.get("paymentInstruments", []):

                rows.append((
                    "India",
                    year,
                    quarter,

                    tx.get("name"),

                    pi.get("count"),
                    pi.get("amount")
                ))

    # STATE LEVEL

    state_root = os.path.join(root, "state")

    for state, year, quarter, jpath in iter_states(state_root):

        data = load_json(jpath)

        if not data:
            continue

        for tx in data.get("data", {}).get("transactionData", []):

            for pi in tx.get("paymentInstruments", []):

                rows.append((
                    state.replace("-", " ").title(),
                    year,
                    quarter,

                    tx.get("name"),

                    pi.get("count"),
                    pi.get("amount")
                ))

    cur.executemany(
        """
        INSERT INTO Aggregated_insurance (
            State,
            Year,
            Quarter,
            Transaction_type,
            Transaction_count,
            Transaction_amount
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        rows
    )

    print(f"Inserted : {len(rows):,}")


# ══════════════════════════════════════════════════════════
# AGGREGATED TRANSACTION
# ══════════════════════════════════════════════════════════

def extract_aggregated_transaction(cur):

    print("\n[2/9] Aggregated_transaction")

    rows = []

    root = os.path.join(
        DATA_DIR,
        "aggregated",
        "transaction",
        "country",
        "india"
    )

    # INDIA

    for year, quarter, jpath in iter_year_quarter(root):

        data = load_json(jpath)

        if not data:
            continue

        for tx in data.get("data", {}).get("transactionData", []):

            for pi in tx.get("paymentInstruments", []):

                rows.append((
                    "India",
                    year,
                    quarter,

                    tx.get("name"),

                    pi.get("count"),
                    pi.get("amount")
                ))

    # STATES

    state_root = os.path.join(root, "state")

    for state, year, quarter, jpath in iter_states(state_root):

        data = load_json(jpath)

        if not data:
            continue

        for tx in data.get("data", {}).get("transactionData", []):

            for pi in tx.get("paymentInstruments", []):

                rows.append((
                    state.replace("-", " ").title(),
                    year,
                    quarter,

                    tx.get("name"),

                    pi.get("count"),
                    pi.get("amount")
                ))

    cur.executemany(
        """
        INSERT INTO Aggregated_transaction (
            State,
            Year,
            Quarter,
            Transaction_type,
            Transaction_count,
            Transaction_amount
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        rows
    )

    print(f"Inserted : {len(rows):,}")


# ══════════════════════════════════════════════════════════
# AGGREGATED USER
# ══════════════════════════════════════════════════════════

def extract_aggregated_user(cur):

    print("\n[3/9] Aggregated_user")

    rows = []

    root = os.path.join(
        DATA_DIR,
        "aggregated",
        "user",
        "country",
        "india"
    )

    def parse(state_label, year, quarter, data):

        inner = data.get("data", {})

        aggregated = inner.get("aggregated", {})

        registered_users = aggregated.get(
            "registeredUsers",
            0
        )

        app_opens = aggregated.get(
            "appOpens",
            0
        )

        for device in (inner.get("usersByDevice") or []):

            rows.append((
                state_label,
                year,
                quarter,

                registered_users,
                app_opens,

                device.get("brand"),
                device.get("count"),
                device.get("percentage")
            ))

    # INDIA

    for year, quarter, jpath in iter_year_quarter(root):

        data = load_json(jpath)

        if data:
            parse(
                "India",
                year,
                quarter,
                data
            )

    # STATES

    state_root = os.path.join(root, "state")

    for state, year, quarter, jpath in iter_states(state_root):

        data = load_json(jpath)

        if data:
            parse(
                state.replace("-", " ").title(),
                year,
                quarter,
                data
            )

    cur.executemany(
        """
        INSERT INTO Aggregated_user (
            State,
            Year,
            Quarter,

            Registered_users,
            App_opens,

            User_brand,
            User_count,
            User_percentage
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows
    )

    print(f"Inserted : {len(rows):,}")


# ══════════════════════════════════════════════════════════
# MAP INSURANCE
# ══════════════════════════════════════════════════════════

def extract_map_insurance(cur):

    print("\n[4/9] Map_insurance")

    rows = []

    root = os.path.join(
        DATA_DIR,
        "map",
        "insurance",
        "hover",
        "country",
        "india"
    )

    def parse(state_label, year, quarter, data):

        for item in data.get("data", {}).get(
            "hoverDataList",
            []
        ):

            district = item.get("name")

            for metric in item.get("metric", []):

                rows.append((
                    state_label,
                    year,
                    quarter,

                    district,

                    metric.get("count"),
                    metric.get("amount")
                ))

    # INDIA

    for year, quarter, jpath in iter_year_quarter(root):

        data = load_json(jpath)

        if data:
            parse("India", year, quarter, data)

    # STATES

    state_root = os.path.join(root, "state")

    for state, year, quarter, jpath in iter_states(state_root):

        data = load_json(jpath)

        if data:
            parse(
                state.replace("-", " ").title(),
                year,
                quarter,
                data
            )

    cur.executemany(
        """
        INSERT INTO Map_insurance (
            State,
            Year,
            Quarter,
            District,
            Transaction_count,
            Transaction_amount
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        rows
    )

    print(f"Inserted : {len(rows):,}")


# ══════════════════════════════════════════════════════════
# MAP MAP
# ══════════════════════════════════════════════════════════

def extract_map_map(cur):

    print("\n[5/9] Map_map")

    rows = []

    root = os.path.join(
        DATA_DIR,
        "map",
        "transaction",
        "hover",
        "country",
        "india"
    )

    def parse(state_label, year, quarter, data):

        for item in data.get("data", {}).get(
            "hoverDataList",
            []
        ):

            district = item.get("name")

            for metric in item.get("metric", []):

                rows.append((
                    state_label,
                    year,
                    quarter,

                    district,

                    metric.get("count"),
                    metric.get("amount")
                ))

    # INDIA

    for year, quarter, jpath in iter_year_quarter(root):

        data = load_json(jpath)

        if data:
            parse("India", year, quarter, data)

    # STATES

    state_root = os.path.join(root, "state")

    for state, year, quarter, jpath in iter_states(state_root):

        data = load_json(jpath)

        if data:
            parse(
                state.replace("-", " ").title(),
                year,
                quarter,
                data
            )

    cur.executemany(
        """
        INSERT INTO Map_map (
            State,
            Year,
            Quarter,
            District,
            Transaction_count,
            Transaction_amount
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        rows
    )

    print(f"Inserted : {len(rows):,}")


# ══════════════════════════════════════════════════════════
# MAP USER
# ══════════════════════════════════════════════════════════

def extract_map_user(cur):

    print("\n[6/9] Map_user")

    rows = []

    root = os.path.join(
        DATA_DIR,
        "map",
        "user",
        "hover",
        "country",
        "india"
    )

    def parse(state_label, year, quarter, data):

        hover = data.get("data", {}).get(
            "hoverData",
            {}
        )

        for district, values in hover.items():

            rows.append((
                state_label,
                year,
                quarter,

                district,

                values.get("registeredUsers"),
                values.get("appOpens")
            ))

    # INDIA

    for year, quarter, jpath in iter_year_quarter(root):

        data = load_json(jpath)

        if data:
            parse("India", year, quarter, data)

    # STATES

    state_root = os.path.join(root, "state")

    for state, year, quarter, jpath in iter_states(state_root):

        data = load_json(jpath)

        if data:
            parse(
                state.replace("-", " ").title(),
                year,
                quarter,
                data
            )

    cur.executemany(
        """
        INSERT INTO Map_user (
            State,
            Year,
            Quarter,
            District,
            Registered_users,
            App_opens
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        rows
    )

    print(f"Inserted : {len(rows):,}")


# ══════════════════════════════════════════════════════════
# TOP HELPERS
# ══════════════════════════════════════════════════════════

def parse_top_transaction(
    state_label,
    year,
    quarter,
    data,
    rows
):

    inner = data.get("data", {})

    mapping = [
        ("State", "states"),
        ("District", "districts"),
        ("Pincode", "pincodes")
    ]

    for entity_type, key in mapping:

        for item in (inner.get(key) or []):

            metric = item.get("metric", {})

            rows.append((
                state_label,
                year,
                quarter,

                entity_type,

                item.get(
                    "entityName",
                    item.get("name")
                ),

                metric.get("count"),
                metric.get("amount")
            ))


# ══════════════════════════════════════════════════════════
# TOP INSURANCE
# ══════════════════════════════════════════════════════════

def extract_top_insurance(cur):

    print("\n[7/9] Top_insurance")

    rows = []

    root = os.path.join(
        DATA_DIR,
        "top",
        "insurance",
        "country",
        "india"
    )

    # INDIA

    for year, quarter, jpath in iter_year_quarter(root):

        data = load_json(jpath)

        if data:
            parse_top_transaction(
                "India",
                year,
                quarter,
                data,
                rows
            )

    # STATES

    state_root = os.path.join(root, "state")

    for state, year, quarter, jpath in iter_states(state_root):

        data = load_json(jpath)

        if data:
            parse_top_transaction(
                state.replace("-", " ").title(),
                year,
                quarter,
                data,
                rows
            )

    cur.executemany(
        """
        INSERT INTO Top_insurance (
            State,
            Year,
            Quarter,

            Entity_type,
            Entity_name,

            Transaction_count,
            Transaction_amount
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        rows
    )

    print(f"Inserted : {len(rows):,}")


# ══════════════════════════════════════════════════════════
# TOP MAP
# ══════════════════════════════════════════════════════════

def extract_top_map(cur):

    print("\n[8/9] Top_map")

    rows = []

    root = os.path.join(
        DATA_DIR,
        "top",
        "transaction",
        "country",
        "india"
    )

    # INDIA

    for year, quarter, jpath in iter_year_quarter(root):

        data = load_json(jpath)

        if data:
            parse_top_transaction(
                "India",
                year,
                quarter,
                data,
                rows
            )

    # STATES

    state_root = os.path.join(root, "state")

    for state, year, quarter, jpath in iter_states(state_root):

        data = load_json(jpath)

        if data:
            parse_top_transaction(
                state.replace("-", " ").title(),
                year,
                quarter,
                data,
                rows
            )

    cur.executemany(
        """
        INSERT INTO Top_map (
            State,
            Year,
            Quarter,

            Entity_type,
            Entity_name,

            Transaction_count,
            Transaction_amount
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        rows
    )

    print(f"Inserted : {len(rows):,}")


# ══════════════════════════════════════════════════════════
# TOP USER
# ══════════════════════════════════════════════════════════

def extract_top_user(cur):

    print("\n[9/9] Top_user")

    rows = []

    root = os.path.join(
        DATA_DIR,
        "top",
        "user",
        "country",
        "india"
    )

    def parse(state_label, year, quarter, data):

        inner = data.get("data", {})

        mapping = [
            ("State", "states"),
            ("District", "districts"),
            ("Pincode", "pincodes")
        ]

        for entity_type, key in mapping:

            for item in (inner.get(key) or []):

                rows.append((
                    state_label,
                    year,
                    quarter,

                    entity_type,

                    item.get("name"),

                    item.get("registeredUsers")
                ))

    # INDIA

    for year, quarter, jpath in iter_year_quarter(root):

        data = load_json(jpath)

        if data:
            parse(
                "India",
                year,
                quarter,
                data
            )

    # STATES

    state_root = os.path.join(root, "state")

    for state, year, quarter, jpath in iter_states(state_root):

        data = load_json(jpath)

        if data:
            parse(
                state.replace("-", " ").title(),
                year,
                quarter,
                data
            )

    cur.executemany(
        """
        INSERT INTO Top_user (
            State,
            Year,
            Quarter,

            Entity_type,
            Entity_name,

            Registered_users
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        rows
    )

    print(f"Inserted : {len(rows):,}")


# ══════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════

def main():

    print("=" * 60)
    print("PhonePe Data → SQLite Extractor")
    print("=" * 60)

    print(f"Data Directory : {DATA_DIR}")
    print(f"Database Path  : {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)

    conn.execute("PRAGMA journal_mode=WAL;")

    try:

        # CREATE TABLES

        for stmt in CREATE_STATEMENTS.strip().split(";"):

            stmt = stmt.strip()

            if stmt:
                conn.execute(stmt)

        conn.commit()

        cur = conn.cursor()

        # RUN ALL EXTRACTORS

        extractors = [

            extract_aggregated_insurance,
            extract_aggregated_transaction,
            extract_aggregated_user,

            extract_map_insurance,
            extract_map_map,
            extract_map_user,

            extract_top_insurance,
            extract_top_map,
            extract_top_user
        ]

        for fn in extractors:

            try:

                fn(cur)

                conn.commit()

            except Exception:

                print(f"\n[ERROR] in {fn.__name__}")

                traceback.print_exc()

                conn.rollback()

        # SUMMARY

        print("\n" + "=" * 60)

        print("TABLE ROW COUNTS")

        tables = [

            "Aggregated_insurance",
            "Aggregated_transaction",
            "Aggregated_user",

            "Map_insurance",
            "Map_map",
            "Map_user",

            "Top_insurance",
            "Top_map",
            "Top_user"
        ]

        for table in tables:

            count = cur.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]

            print(f"{table:<30} {count:>10,}")

        print("=" * 60)

        print(f"\nDatabase saved to:\n{DB_PATH}")

    finally:

        conn.close()


if __name__ == "__main__":

    main()