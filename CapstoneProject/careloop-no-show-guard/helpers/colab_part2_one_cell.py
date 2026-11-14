import sqlite3, re, os, pandas as pd
pd.set_option("display.width", 200)

SQL_TEXT = r"""-- 02_queries.sql  (MySQL 8; in SQLiteOnline skip the first two lines)
CREATE DATABASE noshowguard;
USE noshowguard;

-- ===== Task 2.1 =====
CREATE TABLE clinics (
  clinic_id VARCHAR(5) PRIMARY KEY, clinic_name VARCHAR(40) NOT NULL, city VARCHAR(20) NOT NULL,
  tier VARCHAR(10), latitude DECIMAL(8,4), longitude DECIMAL(8,4), temp_c DECIMAL(5,1));
CREATE TABLE appointments (
  appointment_id VARCHAR(8) PRIMARY KEY, patient_id VARCHAR(8) NOT NULL, clinic_id VARCHAR(5) NOT NULL,
  booked_on DATE, appt_date DATE, age INT, gender VARCHAR(1), distance_km DECIMAL(5,1), fee_inr INT,
  booking_channel VARCHAR(10), visit_type VARCHAR(12), reminder_sent VARCHAR(3), prior_no_shows INT,
  status VARCHAR(10), lead_days INT, no_show INT,
  FOREIGN KEY (clinic_id) REFERENCES clinics(clinic_id));

-- now run load_data.sql, then:
SELECT COUNT(*) AS clinics_rows FROM clinics;                       -- expect 8
SELECT COUNT(*) AS appointments_rows, SUM(no_show) AS no_shows FROM appointments;   -- expect 990 and 218

-- duplicate key test: run this, then paste the real error text from YOUR output below
INSERT INTO appointments VALUES ('A0001','P999','C01','2025-01-01','2025-01-05',30,'F',5.0,500,'App','Consultation','Yes',0,'Attended',4,0);
-- ERROR (paste yours here), e.g.: Error Code: 1062. Duplicate entry 'A0001' for key 'appointments.PRIMARY'

-- ===== Task 2.2 =====
SELECT c.clinic_name, c.city, COUNT(*) AS appointments, SUM(a.no_show) AS no_shows,
       ROUND(100.0 * SUM(a.no_show) / COUNT(*), 1) AS no_show_pct
FROM appointments a JOIN clinics c ON a.clinic_id = c.clinic_id
GROUP BY c.clinic_id, c.clinic_name, c.city
HAVING COUNT(*) >= 95
ORDER BY no_show_pct DESC;

-- same query without HAVING (all 8 clinics)
-- NOTE (write from your output): highest rate = <clinic>, <pct>%, with <n> appointments
SELECT c.clinic_name, c.city, COUNT(*) AS appointments, SUM(a.no_show) AS no_shows,
       ROUND(100.0 * SUM(a.no_show) / COUNT(*), 1) AS no_show_pct
FROM appointments a JOIN clinics c ON a.clinic_id = c.clinic_id
GROUP BY c.clinic_id, c.clinic_name, c.city
ORDER BY no_show_pct DESC;

-- ===== Task 2.3 =====
SELECT CASE WHEN lead_days <= 7  THEN '1-7'
            WHEN lead_days <= 14 THEN '8-14'
            WHEN lead_days <= 30 THEN '15-30'
            ELSE '31+' END AS lead_band,
       COUNT(*) AS appointments, SUM(no_show) AS no_shows,
       ROUND(100.0 * SUM(no_show) / COUNT(*), 1) AS no_show_pct
FROM appointments
GROUP BY lead_band
ORDER BY MIN(lead_days);

-- ===== Task 2.4 =====
WITH monthly AS (
  SELECT SUBSTR(appt_date, 1, 7) AS month, COUNT(*) AS appointments,
         ROUND(100.0 * SUM(no_show) / COUNT(*), 1) AS no_show_pct
  FROM appointments
  GROUP BY SUBSTR(appt_date, 1, 7))
SELECT month, appointments, no_show_pct,
       ROUND(no_show_pct - LAG(no_show_pct) OVER (ORDER BY month), 1) AS change_pp
FROM monthly
ORDER BY month;

-- ===== Task 2.5 =====
WITH clinic_rates AS (
  SELECT c.clinic_name AS clinic, c.city,
         ROUND(100.0 * SUM(a.no_show) / COUNT(*), 1) AS no_show_pct
  FROM appointments a JOIN clinics c ON a.clinic_id = c.clinic_id
  GROUP BY c.clinic_id, c.clinic_name, c.city)
SELECT clinic, city, no_show_pct,
       RANK() OVER (PARTITION BY city ORDER BY no_show_pct DESC) AS rank_in_city,
       CASE WHEN no_show_pct > (SELECT 100.0 * SUM(no_show) / COUNT(*) FROM appointments) THEN 'above'
            WHEN no_show_pct < (SELECT 100.0 * SUM(no_show) / COUNT(*) FROM appointments) THEN 'below'
            ELSE 'equal' END AS vs_overall
FROM clinic_rates
ORDER BY city, rank_in_city;
"""

# save the SQL as a real file (download it from the Files panel for your GitHub repo)
with open("02_queries.sql", "w") as f:
    f.write(SQL_TEXT)

assert os.path.exists("load_data.sql"), "load_data.sql not found - run notebook 01 (Task 1.6) first in this same Colab session"

con = sqlite3.connect(":memory:")
sql = re.sub(r"--[^\n]*", "", SQL_TEXT)                                   # remove comments
sql = re.sub(r"(?im)^\s*(CREATE DATABASE|USE)\b[^;]*;", "", sql)          # SQLite has no CREATE DATABASE / USE
statements = [s.strip() for s in sql.split(";") if s.strip()]

loaded = False
for st in statements:
    if st.upper().startswith("CREATE TABLE"):
        con.execute(st)
        continue
    if not loaded:
        con.executescript(open("load_data.sql").read())
        con.commit()
        loaded = True
    print("\n" + "=" * 70 + "\n" + st[:90].replace("\n", " ") + " ...")
    try:
        if st.upper().startswith(("SELECT", "WITH")):
            print(pd.read_sql_query(st, con).to_string(index=False))
        else:
            con.execute(st)
    except sqlite3.IntegrityError as e:
        print("ERROR (copy this into the comment in 02_queries.sql):", e)
