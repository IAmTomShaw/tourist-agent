import streamlit as st
from streamlit import session_state as ss
import asyncio
import datetime
from src.gcal import get_events
from src.agent import run_agent
from src.cal import show_calendar

# Page configuration
st.set_page_config(
    page_title="Travel Research Agent",
    page_icon="✈️",
    layout="wide"
)

# Initialize session state
if 'agent_running' not in ss:
    ss.agent_running = False
if 'agent_finished' not in ss:
    ss.agent_finished = False
if 'current_status' not in ss:
    ss.current_status = ""
# step/state machine for staged reruns to surface statuses
if 'agent_step' not in ss:
    ss.agent_step = None
if 'agent_run_started' not in ss:
    ss.agent_run_started = False
# Ensure trip date keys exist so ss.trip_start / trip_end are always available
if 'trip_start' not in ss:
    ss.trip_start = datetime.date.today()
if 'trip_end' not in ss:
    ss.trip_end = ss.trip_start + datetime.timedelta(days=3)

# Title
st.title("✈️ Travel Research Agent")
st.subheader("Discover the best activities for your trip based on your calendar availability.")
st.markdown("---")

# Status message box placeholder to keep user informed while agent runs

# Main interface
if not ss.agent_finished:
    st.write("Click the button below to start researching travel options:")

    # Location input field
    location = st.text_input("Destination Location", value="San Francisco, CA", key="trip_location")

    # Get user inputs for trip dates
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Trip Start Date", key="trip_start")
    with col2:
        end_date = st.date_input("Trip End Date", key="trip_end")

    # When clicked: set initial state and force a rerun so UI updates (button disabled)
    if st.button("🚀 Run Agent", type="primary", disabled=ss.agent_running):
        if not ss.agent_running:
            ss.agent_running = True
            ss.agent_finished = False
            ss.agent_step = 0
            ss.agent_run_started = False
            ss.current_status = "Starting agent..."
            st.rerun()()
    
    status_box = st.empty()

    # Step-driven work so intermediate statuses render between long tasks
    if ss.agent_running:
        # STEP 0: fetch calendar events
        if ss.agent_step == 0:
            ss.current_status = "Fetching calendar events..."
            # perform fetch (synchronous)
            events = get_events(ss.trip_start, ss.trip_end)
            ss.fetched_events = events or []
            ss.agent_step = 1
            # rerun so the "Running research agent..." status can be shown before the heavy work
            st.rerun()()

        # STEP 1: prepare to run long async agent; show status first, then run on next rerun
        elif ss.agent_step == 1 and not ss.agent_run_started:
            ss.current_status = f"Found {len(ss.fetched_events)} calendar events. Running research agent..."
            ss.agent_run_started = True
            st.rerun()()

        elif ss.agent_step == 1 and ss.agent_run_started:
            # run the async agent (blocking call) now that status is visible
            agent_result = asyncio.run(run_agent(
                start_date=ss.trip_start,
                end_date=ss.trip_end,
                location=ss.get("trip_location", "San Francisco, CA"),
                busy_periods=ss.fetched_events
            ))
            ss.agent_result = agent_result
            ss.agent_step = 2
            st.rerun()()

        # STEP 2: finalize
        elif ss.agent_step == 2:
            ss.agent_running = False
            ss.agent_finished = True
            ss.current_status = ""
            # leave agent_step as 2 so finished UI renders

    # Display current status if agent is running
    # Render the persistent status message box so users see updates between reruns
    print('current status: ', ss.current_status)
    if ss.current_status:
        status_box.info(f"🔄 {ss.current_status}")
    elif ss.agent_finished:
        status_box.success("✅ Research complete.")
    else:
        print('empty box')
        status_box.empty()

# Display results after agent finishes
if ss.agent_finished:
    st.markdown("---")
    st.header("🎯 Available Travel Options")
    st.write("Here are the top recommendations based on your preferences:")
    
    # Display results in a grid format (3 columns)
    results = ss.agent_result if ss.agent_result else []
    cols_per_row = 3

    for i in range(0, len(results), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(results):
                result = results[i + j]
                with col:
                    with st.container(border=True):
                        st.subheader(result.name)
                        st.write(f"📍 **Location:** {result.location}")
                        st.write(f"💰 **Price:** {result.price}")
                        st.write(f"📝 **Description:**")
                        st.write(result.description)
                        st.write(f"🗓️ **Date:** {result.date.split('T')[0]}")
                        st.write(f"🕒 **Suggested Time:** {result.start_time} to {result.end_time}")

    # Hide the inputs
    st.markdown("<style>div.row-widget.stTextInput {display: none;} div.row-widget.stDateInput {display: none;}</style>", unsafe_allow_html=True)
    
    # Reset button
    st.markdown("---")
    if st.button("🔄 Start New Search"):
        ss.agent_running = False
        ss.agent_finished = False
        ss.current_status = ""
        ss.agent_step = None
        ss.agent_run_started = False
        st.rerun()
