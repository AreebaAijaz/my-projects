import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

TIME_ZONES = {
    "UTC",
    "Asia/Karachi",
    "Asia/Kolkata",
    "Asia/Tokyo",
    "Asia/Dubai",
    "America/New_York",
    "America/Los_Angeles",
    "Europe/London",
    "Europe/Berlin",
    "Australia/Sydney",
}

st.title("Time Zone App")
selected_timezone = st.multiselect("Select Time Zones", TIME_ZONES, default=["UTC", "Asia/Karachi"])

st.subheader("Selected Timezones")

for tz in selected_timezone:
    current_time = datetime.now(ZoneInfo(tz))
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    st.write(f"{tz}: {formatted_time}")


st.subheader("Convert Time Between Timezones")
current_time = st.time_input("Enter Current Time", value=datetime.now().time())
from_tz = st.selectbox("From Timezone", TIME_ZONES , index=0)
to_tz = st.selectbox("To Timezone", TIME_ZONES, index=8)

if st.button("Convert"):
    dt = datetime.combine(datetime.today(), current_time, tzinfo=ZoneInfo(from_tz))
    converted_time = dt.astimezone(ZoneInfo(to_tz)).strftime("%Y-%m-%d %H:%M:%S")
    st.success(f"Converted time in {to_tz}: {converted_time}")