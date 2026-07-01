import streamlit as st
import sqlite3
import pandas as pd
import time

st.set_page_config(page_title="Trolley Tracker", layout="wide")

# ─── Session state for login ───────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user_data = None

# ─── DB connection ──────────────────────────────
def get_conn():
    return sqlite3.connect("trolley.db")

# ─── LOGIN PAGE ─────────────────────────────────
def login_page():
    st.title("Airport Trolley Tracker — Login")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Staff Login")
        admin_user = st.text_input("Username", key="admin_user")
        admin_pass = st.text_input("Password", type="password", key="admin_pass")
        if st.button("Login as Staff"):
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT role FROM users 
                WHERE username=? AND password=?
            """, (admin_user, admin_pass))
            result = cursor.fetchone()
            conn.close()

            if result:
                st.session_state.logged_in = True
                st.session_state.role = result[0]
                st.session_state.user_data = {"username": admin_user}
                st.rerun()
            else:
                st.error("Invalid username or password")

    with col2:
        st.subheader("Passenger Login")
        pass_user = st.text_input("Username", key="pass_user")
        pass_pnr  = st.text_input("PNR", key="pass_pnr")
        if st.button("Login as Passenger"):
            conn = get_conn()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, flight_number, scheduled_time, gate 
                FROM passengers 
                WHERE username=? AND pnr=?
            """, (pass_user, pass_pnr))
            result = cursor.fetchone()
            conn.close()

            if result:
                st.session_state.logged_in = True
                st.session_state.role = "passenger"
                st.session_state.user_data = {
                    "name": result[0],
                    "flight_number": result[1],
                    "scheduled_time": result[2],
                    "gate": result[3]
                }
                st.rerun()
            else:
                st.error("Invalid username or PNR")

# ─── ADMIN DASHBOARD ────────────────────────────
def admin_dashboard():
    st.title("Staff Dashboard")
    st.write(f"Logged in as: **{st.session_state.user_data['username']}** ({st.session_state.role})")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if st.button("Refresh Now"):
        st.rerun()

    conn = get_conn()
    df = pd.read_sql("SELECT * FROM trolley_tracking", conn)
    conn.close()

    # Zone filter dropdown
    zones = ["All Zones"] + sorted(df["zone"].unique().tolist())
    selected_zone = st.selectbox("Filter by Zone", zones)

    if selected_zone != "All Zones":
        filtered_df = df[df["zone"] == selected_zone]
    else:
        filtered_df = df

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Trolleys", len(filtered_df))
    col2.metric("Active", len(filtered_df[filtered_df["status"] == "ACTIVE"]))
    col3.metric("Weak Signal", len(filtered_df[filtered_df["status"] == "WEAK_SIGNAL"]))
    col4.metric("Offline", len(filtered_df[filtered_df["status"] == "OFFLINE"]))

    st.subheader(f"Trolleys in {selected_zone}")
    sorted_df = filtered_df.sort_values(by=["zone", "trolley_id"])
    st.dataframe(sorted_df, use_container_width=True)

    # Offline trolleys section
    offline_df = df[df["status"] == "OFFLINE"]
    if len(offline_df) > 0:
        st.subheader("⚠️ Offline Trolleys")
        st.dataframe(offline_df, use_container_width=True)

    # Auto refresh every 60 seconds
    time.sleep(60)
    st.rerun()

# ─── PASSENGER DASHBOARD ────────────────────────
def passenger_dashboard():
    st.title("Passenger Portal")

    data = st.session_state.user_data
    st.write(f"Welcome, **{data['name']}**")

    col1, col2, col3 = st.columns(3)
    col1.metric("Flight", data["flight_number"])
    col2.metric("Scheduled Time", data["scheduled_time"])
    col3.metric("Gate", data["gate"])

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if st.button("Refresh Now"):
        st.rerun()

    conn = get_conn()
    df = pd.read_sql("SELECT * FROM trolley_tracking ORDER BY zone, trolley_id", conn)
    conn.close()

    zones = sorted(df["zone"].unique().tolist())
    selected_zone = st.selectbox("Select your Zone", zones)

    available_df = df[(df["zone"] == selected_zone) & (df["status"] == "ACTIVE")]

    st.subheader(f"Available Trolleys in {selected_zone}")
    if len(available_df) > 0:
        st.dataframe(available_df[["trolley_id", "zone", "status"]], use_container_width=True)
    else:
        st.warning("No trolleys currently available in this zone.")

    # Auto refresh every 60 seconds
    time.sleep(60)
    st.rerun()

# ─── MAIN ROUTER ────────────────────────────────
if not st.session_state.logged_in:
    login_page()
elif st.session_state.role == "passenger":
    passenger_dashboard()
else:
    admin_dashboard()