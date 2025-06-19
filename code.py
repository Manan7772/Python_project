import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="🚴‍♂️ Weekly Travel Tracker",
    page_icon="🚴‍♂️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    body {
        background-image: url('https://example.com/path_to_background_image.jpg');
        background-size: cover;
        color: #333;
    }
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #4caf50 0%, #2196f3 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    .day-header {
        background-color: #e1f5fe;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🚴‍♂️ Weekly Travel Tracker</h1>
    <p>Track your daily travel, costs, and carbon emissions</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'travel_data' not in st.session_state:
    st.session_state.travel_data = []
if 'setup_complete' not in st.session_state:
    st.session_state.setup_complete = False

# User Information Setup
if not st.session_state.setup_complete:
    st.header("📝 User Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Enter your name:", placeholder="John Doe")
        age = st.number_input("Enter your age:", min_value=16, max_value=100, value=25)
    
    with col2:
        vehicle = st.text_input("Enter your bike model:", placeholder="Shine125")
        city = st.text_input("Enter your city name:", placeholder="Mumbai")
    
    if st.button("Continue to Travel Tracking", type="primary"):
        if name and vehicle and city:
            st.session_state.user_data = {
                'name': name,
                'age': age,
                'vehicle': vehicle,
                'city': city
            }
            st.session_state.setup_complete = True
            st.rerun()
        else:
            st.error("Please fill in all required fields!")

else:
    # Display user info
    user = st.session_state.user_data
    st.sidebar.markdown(f"""
    ### 👤 User Profile
    **Name:** {user['name']}  
    **Age:** {user['age']}  
    **Vehicle:** {user['vehicle']}  
    **City:** {user['city']}
    """)
    
    if st.sidebar.button("Reset User Info"):
        st.session_state.setup_complete = False
        st.session_state.travel_data = []
        st.rerun()
    
    # Days of the week
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Travel Data Collection
    st.header("📅 Weekly Travel Data")
    
    # Create tabs for each day
    tabs = st.tabs(days_of_week)
    
    # Initialize travel data if empty
    if len(st.session_state.travel_data) == 0:
        st.session_state.travel_data = [
            {'day': day, 'traveled': False, 'destination': '', 'km': 0, 'cost': 0, 'emission': 0}
            for day in days_of_week
        ]
    
    # Process each day
    for i, (tab, day) in enumerate(zip(tabs, days_of_week)):
        with tab:
            st.markdown(f"<div class='day-header'><h3>📍 {day}</h3></div>", unsafe_allow_html=True)
            
            # Check if user traveled
            traveled = st.radio(
                f"Did you travel on {day}?",
                options=[False, True],
                format_func=lambda x: "Yes" if x else "No",
                key=f"travel_{i}",
                index=0 if not st.session_state.travel_data[i]['traveled'] else 1
            )
            
            if traveled:
                destination = st.text_input(
                    "Where did you travel?",
                    key=f"dest_{i}",
                    value=st.session_state.travel_data[i]['destination']
                )
                
                km = st.number_input(
                    "How many kilometers did you travel?",
                    min_value=0,
                    max_value=1000,
                    value=st.session_state.travel_data[i]['km'],
                    key=f"km_{i}"
                )
                
                if km > 0:
                    cost = km * 75  # Cost calculation
                    emission = km * 125  # Emission calculation
                    
                    # Display calculations
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("💰 Estimated Cost", f"₹{cost}")
                    with col2:
                        st.metric("📏 Distance", f"{km} km")
                    with col3:
                        st.metric("🌿 CO₂ Emission", f"{emission}g")
                    
                    # Update session state
                    st.session_state.travel_data[i] = {
                        'day': day,
                        'traveled': True,
                        'destination': destination,
                        'km': km,
                        'cost': cost,
                        'emission': emission
                    }
                    
                    st.success(f"✅ On {day}, {user['name']}, you traveled {km} km to {destination}. Estimated cost: ₹{cost}, CO₂ emitted: {emission}g")
                else:
                    st.session_state.travel_data[i]['traveled'] = True
                    st.session_state.travel_data[i]['destination'] = destination
            else:
                st.session_state.travel_data[i] = {
                    'day': day,
                    'traveled': False,
                    'destination': '',
                    'km': 0,
                    'cost': 0,
                    'emission': 0
                }
                st.success(f"🌱 Great! You preserved money and reduced carbon emissions on {day}!")
    
    # Summary Section
    st.header("📊 Weekly Summary")
    
    # Calculate totals
    total_km = sum([data['km'] for data in st.session_state.travel_data])
    total_cost = sum([data['cost'] for data in st.session_state.travel_data])
    total_emission = sum([data['emission'] for data in st.session_state.travel_data])
    days_traveled = sum([1 for data in st.session_state.travel_data if data['traveled']])
    
    # Display summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🗓️ Days Traveled", f"{days_traveled}/7")
    with col2:
        st.metric("📏 Total Distance", f"{total_km} km")
    with col3:
        st.metric("💰 Total Cost", f"₹{total_cost}")
    with col4:
        st.metric("🌿 Total CO₂", f"{total_emission}g")
    
    # Create visualizations
    if total_km > 0:
        st.subheader("📈 Visual Analytics")
        
        # Prepare data for charts
        chart_data = []
        for data in st.session_state.travel_data:
            if data['traveled']:
                chart_data.append(data)
        
        if chart_data:
            df = pd.DataFrame(chart_data)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Distance chart
                fig_distance = px.bar(
                    df, 
                    x='day', 
                    y='km',
                    title='Daily Distance Traveled',
                    color='km',
                    color_continuous_scale='Blues'
                )
                fig_distance.update_layout(showlegend=False)
                st.plotly_chart(fig_distance, use_container_width=True)
            
            with col2:
                # Cost and Emission chart
                fig_multi = go.Figure()
                fig_multi.add_trace(go.Bar(
                    x=df['day'],
                    y=df['cost'],
                    name='Cost (₹)',
                    marker_color='green',
                    yaxis='y'
                ))
                fig_multi.add_trace(go.Bar(
                    x=df['day'],
                    y=df['emission'],
                    name='CO₂ Emission (g)',
                    marker_color='red',
                    yaxis='y2'
                ))
                
                fig_multi.update_layout(
                    title='Daily Cost vs CO₂ Emissions',
                    yaxis=dict(title='Cost (₹)', side='left'),
                    yaxis2=dict(title='CO₂ Emission (g)', side='right', overlaying='y'),
                    barmode='group'
                )
                st.plotly_chart(fig_multi, use_container_width=True)
    
    # Data Table
    st.subheader("📋 Detailed Travel Log")
    
    # Create display dataframe
    display_data = []
    for data in st.session_state.travel_data:
        display_data.append({
            'Day': data['day'],
            'Traveled': '✅ Yes' if data['traveled'] else '❌ No',
            'Destination': data['destination'] if data['destination'] else '-',
            'Distance (km)': data['km'],
            'Cost (₹)': data['cost'],
            'CO₂ Emission (g)': data['emission']
        })
    
    df_display = pd.DataFrame(display_data)
    st.dataframe(df_display, use_container_width=True)
    
    # Environmental Impact Section
    if total_emission > 0:
        st.subheader("🌍 Environmental Impact")
        
        # Calculate some environmental comparisons
        trees_needed = round(total_emission / 22000, 2)  # Approximate CO2 absorbed by one tree per year
        car_equivalent = round(total_emission / 404, 2)  # Average car CO2 per km
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"🌳 Trees needed to offset your weekly CO₂: **{trees_needed}** trees")
        with col2:
            st.info(f"🚗 Equivalent to driving a car for: **{car_equivalent}** km")
    
    # Export functionality
    st.subheader("💾 Export Data")
    if st.button("📥 Download Weekly Report", type="secondary"):
        # Create a summary report
        report_data = {
            'User ': [user['name']],
            'Vehicle': [user['vehicle']],
            'City': [user['city']],
            'Week Summary': [f"{days_traveled} days traveled"],
            'Total Distance': [f"{total_km} km"],
            'Total Cost': [f"₹{total_cost}"],
            'Total CO₂': [f"{total_emission}g"]
        }
        
        report_df = pd.DataFrame(report_data)
        csv = report_df.to_csv(index=False)
        
        st.download_button(
            label="📄 Download CSV Report",
            data=csv,
            file_name=f"travel_report_{user['name']}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    🚴‍♂️ Weekly Travel Tracker | Track • Analyze • Optimize your daily travel
</div>
""", unsafe_allow_html=True)
