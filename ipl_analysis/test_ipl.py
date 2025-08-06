import pandas as pd
import sqlite3
import os

def test_csv_loading():
    df = pd.read_csv("ipl_2008_to_2025.csv")
    assert not df.empty
    assert 'Teams' in df.columns
    assert 'Date' in df.columns
    print("✅ CSV loaded successfully")

def test_date_parsing():
    df = pd.read_csv("ipl_2008_to_2025.csv")
    df['Date'] = pd.to_datetime(df['Date'], format='mixed', errors='coerce')
    assert df['Date'].dtype == 'datetime64[ns]'
    assert df['Date'].isna().sum() < len(df)
    print("✅ Mixed date parsing works")

def test_database_insertion():
    conn = sqlite3.connect("test.db")
    df = pd.read_csv("ipl_2008_to_2025.csv")
    df.to_sql("matches", conn, if_exists="replace", index=False)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM matches")
    count = cursor.fetchone()[0]
    assert count > 0
    print("✅ Data inserted into DB")

if __name__ == "__main__":
    test_csv_loading()
    test_date_parsing()
    test_database_insertion()
