import sqlite3, re, pandas as pd
pd.set_option("display.width", 200)

con = sqlite3.connect(":memory:")              # fresh database every run
raw = open("02_queries.sql").read()

# 1) remove comments and the two MySQL-only lines (SQLite has no CREATE DATABASE / USE)
sql = re.sub(r"--[^\n]*", "", raw)             # removes whole-line and end-of-line comments
sql = re.sub(r"(?im)^\s*(CREATE DATABASE|USE)\b[^;]*;", "", sql)

# 2) split into statements
statements = [s.strip() for s in sql.split(";") if s.strip()]

loaded = False
for st in statements:
    if st.upper().startswith("CREATE TABLE"):
        con.execute(st)
        continue
    if not loaded:                              # tables exist -> run load_data.sql once
        con.executescript(open("load_data.sql").read())
        con.commit()
        loaded = True
    print("\n" + "=" * 70 + "\n" + st[:90].replace("\n", " ") + " ...")
    try:
        if st.upper().startswith(("SELECT", "WITH")):
            print(pd.read_sql_query(st, con).to_string(index=False))
        else:
            con.execute(st)
    except sqlite3.IntegrityError as e:         # the duplicate A0001 insert lands here
        print("ERROR (copy this into the comment in 02_queries.sql):", e)
