import streamlit as st
import time

# Page configuration
st.set_page_config(
    page_title="Travel Research Agent",
    page_icon="✈️",
    layout="wide"
)

# Initialize session state
if 'agent_running' not in st.session_state:
    st.session_state.agent_running = False
if 'agent_finished' not in st.session_state:
    st.session_state.agent_finished = False
if 'current_status' not in st.session_state:
    st.session_state.current_status = ""

# Title
st.title("✈️ Travel Research Agent")
st.markdown("---")

# Function to simulate agent running with status updates
def run_agent():
    """Simulate the agent running with various status updates"""
    st.session_state.agent_running = True
    st.session_state.agent_finished = False
    
    statuses = [
        "Checking calendar availability...",
        "Researching activities in San Francisco...",
        "Finding the best hotels in the area...",
        "Comparing flight prices...",
        "Analyzing restaurant options...",
        "Gathering weather information...",
        "Compiling recommendations..."
    ]
    
    status_placeholder = st.empty()
    
    for status in statuses:
        st.session_state.current_status = status
        status_placeholder.info(f"🔄 {status}")
        time.sleep(1.5)  # Simulate processing time
    
    st.session_state.agent_running = False
    st.session_state.agent_finished = True
    status_placeholder.success("✅ Research completed!")

# Sample results to display after agent finishes
def get_sample_results():
    """Return sample travel options"""
    return [
        {
            "title": "Weekend Getaway Package",
            "destination": "San Francisco, CA",
            "duration": "3 days / 2 nights",
            "price": "$1,299",
            "highlights": "Golden Gate Bridge Tour, Alcatraz Visit, Fisherman's Wharf"
        },
        {
            "title": "Wine Country Retreat",
            "destination": "Napa Valley, CA",
            "duration": "4 days / 3 nights",
            "price": "$1,899",
            "highlights": "Wine Tasting Tours, Spa Experience, Gourmet Dining"
        },
        {
            "title": "Coastal Adventure",
            "destination": "Big Sur & Monterey",
            "duration": "5 days / 4 nights",
            "price": "$2,199",
            "highlights": "Scenic Highway Drive, Whale Watching, Aquarium Visit"
        },
        {
            "title": "City Explorer",
            "destination": "San Francisco Downtown",
            "duration": "2 days / 1 night",
            "price": "$899",
            "highlights": "Cable Car Rides, Museum Tours, Chinatown Experience"
        },
        {
            "title": "Nature & Parks",
            "destination": "Yosemite National Park",
            "duration": "4 days / 3 nights",
            "price": "$1,599",
            "highlights": "Hiking Trails, Waterfalls, Scenic Overlooks"
        },
        {
            "title": "Cultural Immersion",
            "destination": "San Francisco & Oakland",
            "duration": "3 days / 2 nights",
            "price": "$1,099",
            "highlights": "Art Galleries, Theater Shows, Local Cuisine"
        }
    ]

# Main interface
if not st.session_state.agent_finished:
    st.write("Click the button below to start researching travel options:")
    
    if st.button("🚀 Run Agent", type="primary", disabled=st.session_state.agent_running):
        run_agent()
    
    # Display current status if agent is running
    if st.session_state.agent_running and st.session_state.current_status:
        st.info(f"🔄 {st.session_state.current_status}")

# Display results after agent finishes
if st.session_state.agent_finished:
    st.markdown("---")
    st.header("🎯 Available Travel Options")
    st.write("Here are the top recommendations based on your preferences:")
    
    # Display results in a grid format (3 columns)
    results = get_sample_results()
    cols_per_row = 3
    
    for i in range(0, len(results), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(results):
                result = results[i + j]
                with col:
                    with st.container(border=True):
                        st.subheader(result["title"])
                        st.write(f"📍 **Destination:** {result['destination']}")
                        st.write(f"⏱️ **Duration:** {result['duration']}")
                        st.write(f"💰 **Price:** {result['price']}")
                        st.write(f"✨ **Highlights:**")
                        st.write(result['highlights'])
                        if st.button("Select", key=f"select_{i+j}"):
                            st.success(f"Selected: {result['title']}")
    
    # Reset button
    st.markdown("---")
    if st.button("🔄 Start New Search"):
        st.session_state.agent_running = False
        st.session_state.agent_finished = False
        st.session_state.current_status = ""
        st.rerun()
