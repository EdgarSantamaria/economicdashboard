import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import datetime



#from sklearn.linear_model import LinearRegression, LogisticRegression
#from sklearn.ensemble import RandomForestRegressor

#from sklearn.model_selection import train_test_split

#from sklearn import metrics

#abbrevation
def us_state_to_abbrev(string):
    us_state_to_abbrev = {
        "Alabama": "AL",
        "Alaska": "AK",
        "Arizona": "AZ",
        "Arkansas": "AR",
        "California": "CA",
        "Colorado": "CO",
        "Connecticut": "CT",
        "Delaware": "DE",
        "Florida": "FL",
        "Georgia": "GA",
        "Hawaii": "HI",
        "Idaho": "ID",
        "Illinois": "IL",
        "Indiana": "IN",
        "Iowa": "IA",
        "Kansas": "KS",
        "Kentucky": "KY",
        "Louisiana": "LA",
        "Maine": "ME",
        "Maryland": "MD",
        "Massachusetts": "MA",
        "Michigan": "MI",
        "Minnesota": "MN",
        "Mississippi": "MS",
        "Missouri": "MO",
        "Montana": "MT",
        "Nebraska": "NE",
        "Nevada": "NV",
        "New Hampshire": "NH",
        "New Jersey": "NJ",
        "New Mexico": "NM",
        "New York": "NY",
        "North Carolina": "NC",
        "North Dakota": "ND",
        "Ohio": "OH",
        "Oklahoma": "OK",
        "Oregon": "OR",
        "Pennsylvania": "PA",
        "Rhode Island": "RI",
        "South Carolina": "SC",
        "South Dakota": "SD",
        "Tennessee": "TN",
        "Texas": "TX",
        "Utah": "UT",
        "Vermont": "VT",
        "Virginia": "VA",
        "Washington": "WA",
        "West Virginia": "WV",
        "Wisconsin": "WI",
        "Wyoming": "WY",
        "District of Columbia": "DC",
        "American Samoa": "AS",
        "Guam": "GU",
        "Northern Mariana Islands": "MP",
        "Puerto Rico": "PR",
        "United States Minor Outlying Islands": "UM",
        "U.S. Virgin Islands": "VI",
        }
    return us_state_to_abbrev[string]

df1 = pd.read_csv("Master_DF.csv")


df1_nat = df1[df1['GeoName'] == 'United States']
df1_nat["Abrev"] = "US"

df1_states = df1[df1['GeoName'].isin(['Alabama', 'Alaska', 'Arizona', 'Arkansas',
       'California', 'Colorado', 'Connecticut', 'Delaware',
       'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
       'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
       'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
       'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
       'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
       'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
       'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
       'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
       'West Virginia', 'Wisconsin', 'Wyoming'])]

df1_states["Abbrev"] = df1_states['GeoName'].apply(us_state_to_abbrev)

df1_regions = df1[df1['GeoName'].isin(['Wyoming', 'New England', 'Mideast',
       'Great Lakes', 'Plains', 'Southeast', 'Southwest',
       'Rocky Mountain', 'Far West'])]



#site config
st.set_page_config(
    page_title="State Economic Comp",
    page_icon="📈",
    layout = "wide"
)

# CHoro pleth map alternatint with input date 
user_input = st.text_input( "Input text")
st.write(user_input)
start_time = st.slider('Years', 2010, 2021, 2010)
df1_states_recent = df1_states[df1_states["Year"] == start_time]
if(user_input != "" ):
    fig = px.choropleth(df1_states_recent,
                    locations="Abbrev",
                    color= "Personal Income",
                    locationmode="USA-states",
                    range_color=(0,df1_states_recent["Personal Income"].max()),
                    scope="usa")
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)

st.dataframe(df1)
#header column
col0 = st.columns([1])[0]



# column 0 header
with col0:
    st.header('Welcome to my economic dashboard!')

# column 1 pick a state for regression plot and real gdp data
    st.write('Choose states to view.')
    
    #create a sorted list for user to choose from
    state_list = sorted(df1_states['Abbrev'].unique())
    
    #selection tool
    selected_states = st.multiselect(
        "Select which states to compare.",
        state_list
        )
        
    #create dataframe of the seleted states
    state_df = df1_states[df1_states['Abbrev'].isin(selected_states)].copy()
    chart = st.radio(
    "Which plot do you want to see?",
    ('Regression', 'Line'))
    #create scatter plot for selected states
    fig = px.scatter(
        state_df, x= "Real GDP", y= "Personal Income", opacity=0.65,
        trendline='ols', trendline_color_override='darkblue'
    )
    
    # change the background color of plot
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })

    # adds grid axes for better vizualization
    fig.update_xaxes(showgrid=False, gridwidth=1, gridcolor='Gray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='Gray')
    
    # create stats from user selected states dataframe
    # we can probably have the user pick what stats they want to see
    summary_stats = state_df.groupby('Abbrev')['Real GDP'].agg(['mean', 'median', 'min', 'max', 'std'])
    
    #print out the stats in index
    summary_stats.index = summary_stats.index.rename('Real GDP Info')
    st.write('Real GDP Info', summary_stats)
    
    #fixes plot sizing
    st.plotly_chart(fig, use_container_width=True)
