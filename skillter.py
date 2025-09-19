import streamlit as st
import uuid
from datetime import datetime

# In-memory "database"
USERS = {}
SESSIONS = {}
LEDGER = {}

st.set_page_config(page_title="Skill Exchange", page_icon="🎓")

st.title("🎓 Skill Exchange Prototype")

# Sidebar navigation
menu = st.sidebar.radio("Menu", ["Signup", "Create Session", "Browse Sessions", "My Wallet"])

# --- Signup ---
if menu == "Signup":
    st.subheader("Student Signup")
    name = st.text_input("Name")
    email = st.text_input("College Email")
    college = st.text_input("College Name")
    if st.button("Sign up"):
        uid = str(uuid.uuid4())[:8]
        USERS[uid] = {"id": uid, "name": name, "email": email, "college": college}
        LEDGER[uid] = {"balance": 50}  # give free credits
        st.success(f"Welcome {name}! Your User ID: {uid}")
        st.info("Note this User ID for booking sessions.")

elif menu == "Create Session":
    st.subheader("Host a Skill Session")
    host_id = st.text_input("Your User ID")
    skill = st.text_input("Skill you want to teach")

    # Fixed datetime input
    date = st.date_input("Start date")
    time = st.time_input("Start time")
    start_time = datetime.combine(date, time)

    duration = st.number_input("Duration (minutes)", 30, 180, 60)
    credits = st.number_input("Credits (price)", 5, 50, 10)
    if st.button("Create Session"):
        if host_id not in USERS:
            st.error("Invalid User ID")
        else:
            sid = str(uuid.uuid4())[:6]
            SESSIONS[sid] = {
                "id": sid,
                "host": USERS[host_id]["name"],
                "host_id": host_id,
                "skill": skill,
                "start_time": start_time,
                "duration": duration,
                "credits": credits,
            }
            st.success(f"Session created with ID: {sid}")

# --- Browse Sessions ---
elif menu == "Browse Sessions":
    st.subheader("Available Sessions")
    user_id = st.text_input("Enter Your User ID to Book")
    if not SESSIONS:
        st.info("No sessions yet. Create one!")
    for sid, s in SESSIONS.items():
        with st.expander(f"{s['skill']} by {s['host']} ({s['credits']} credits)"):
            st.write(f"🕒 {s['start_time']} | {s['duration']} mins")
            if st.button(f"Book {sid}", key=sid):
                if user_id not in USERS:
                    st.error("Invalid User ID")
                elif LEDGER[user_id]["balance"] < s["credits"]:
                    st.error("Not enough credits!")
                else:
                    LEDGER[user_id]["balance"] -= s["credits"]
                    LEDGER[s["host_id"]]["balance"] += s["credits"]
                    st.success(f"Booked {s['skill']}! {s['credits']} credits deducted.")

# --- Wallet ---
elif menu == "My Wallet":
    st.subheader("Check Your Credits")
    user_id = st.text_input("Enter Your User ID")
    if st.button("Check Balance"):
        if user_id in LEDGER:
            st.info(f"Balance: {LEDGER[user_id]['balance']} credits")
        else:
            st.error("User not found.")
