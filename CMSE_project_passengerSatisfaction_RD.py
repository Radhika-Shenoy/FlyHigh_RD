
import io
import pickle
from distutils.command import upload
from hashlib import new
import itertools
import random
import time
import pandas as pd
import streamlit as st 
import plotly as plt
from pywaffle import Waffle
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import seaborn as sns
import plotly.express as px
import plotly.subplots as sp
import numpy as np
import hiplot as hip
import networkx as nx
from streamlit_option_menu import option_menu
from PIL import Image

#import utils.new_process
import joblib

#Load the dataset
flight_df = pd.read_csv('passenger_exp_train.csv')
flight_df_original=pd.read_csv('passenger_exp_train.csv')

#Imputation is performed on the Arrival Delay in Minutes column where N/A values is filled with zero
#The assumption that the people who have filled the survey didn't experience arrival delay
flight_df['Arrival Delay in Minutes'] = flight_df['Arrival Delay in Minutes'].fillna(0) 
def categorize_age(age):
        if 3 < age <= 14:
            return 'Children: 3yrs - 14yrs'
        elif 14 < age <= 60:
            return 'Adults: 14yrs - 60 yrs'
        else:
            return 'Seniors: greater than 60yrs'
flight_df['Age_Group'] = flight_df['Age'].apply(categorize_age)
st.set_page_config(layout="wide")

#Inclusions for background image
image_url = '''
    <style>
    [data-testid="stAppViewContainer"] {
    background-image: url('https://images.unsplash.com/photo-1498354136128-58f790194fa7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwxfDB8MXxyYW5kb218MHx8fHx8fHx8MTY4MTM0NDkzNA&ixlib=rb-4.0.3&q=80&utm_campaign=api-credit&utm_medium=referral&utm_source=unsplash_source&w=1080');
    background-size: cover;
    background-repeat: no-repeat;
    }
    </style>
    '''
st.markdown(image_url, unsafe_allow_html=True)


#Creating side panel with navigation options for admin
with st.sidebar:
    selected = option_menu( menu_title="FlyHigh R&D Admin navigation options",
    options=["Home",'Overall Airline Stats', "Analysis Page"],
    icons=['house', 'bar-chart', "list-task", 'gear','download','envelope'], 
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "black", "font-size": "20px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "blue"},
    },
    menu_icon="cast",
    default_index=0)

#Sidepanel functionalities
#Functionalities performed when user is on HOMEPAGE
if selected == 'Home':
    st.markdown('<h1 style="color:black;font-size:34px;">🛫FlyHigh Airlines: Rise beyond the clouds⛅</h1>', unsafe_allow_html=True)
    tab1,tab2 = st.tabs(['Home','Learn about satisfaction factors'])
    with tab1:
        
        st.markdown('<h3 style="color:black;font-size:20px;"><em>As a brand, we are dedicated to crafting unforgettable experiences for every passenger that takes to the skies with us, ensuring every moment is filled with delight and wonder.</em></h3>', unsafe_allow_html=True)
        
        image = Image.open('homepage_image.jpg')
        st.image(image, width=600)

        st.markdown('<p style="color:black; font-weight:bold;"><em>Welcome to FlyHigh Airlines Home page! At FlyHigh Airlines, we are dedicated to providing all our flyers with an exceptional and comfortable flying experience. Our brand strives to offer the best-in-class services, ensuring their satisfaction is our top priority. With a focus on efficient operations and unparalleled customer service, we aim to make your journey with us as smooth and enjoyable as possible.Our Dashboard provides a comprehensive overview of key performance indicators, customer feedback, and operational insights. From passenger satisfaction ratings to on-time performance statistics, this page offers a holistic view of our airline performance. With an emphasis on safety, comfort,entertainmen and convenience, we constantly strive to enhance our services and meet the evolving needs of our valued passengers.</em></p>', unsafe_allow_html=True)
    with tab2:
        st.markdown('<p style="color:black; font-weight:bold;">These are the factors which play a vital role in making the journey of a FlyHigh passenger from just a normal travel to a marvel!</p>', unsafe_allow_html=True)
        #st.markdown('<p style="color:black; font-weight:bold;">To view more info about each of the joy factor click on this icon </p>', unsafe_allow_html=True)
        
        st.markdown('<p style="color:black;"><em>To view more info about each of the joy factor click on the expander below the visual representation</em></p>', unsafe_allow_html=True)
        G = nx.DiGraph()

        # Add nodes for satisfaction index and other attributes
        attributes = [
            'Gender', 'Customer Type', 'Age', 'Type of Travel', 'Class', 'Flight Distance',
            'Inflight wifi service', 'Departure/Arrival time convenient', 'Ease of Online booking',
            'Gate location', 'Food and drink', 'Online boarding', 'Seat comfort',
            'Inflight entertainment', 'On-board service', 'Leg room service',
            'Baggage handling', 'Check-in service', 'Inflight service', 'Cleanliness',
            'Departure Delay in Minutes', 'Arrival Delay in Minutes'
        ]

        G.add_node('Satisfaction')  # Root node

        # Add edges between satisfaction and other attributes
        for attribute in attributes:
            G.add_edge('Satisfaction', attribute)

        # Draw the graph
        plt.figure(figsize=(13, 10),facecolor='none')
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=4000, node_color='skyblue', font_size=12, font_weight='bold',alpha=0.8)
        plt.title('Satisfaction Index and Attributes Network Graph')
        plt.tight_layout()
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', transparent=True)
        buffer.seek(0)

        # Display the graph image in Streamlit
        st.image(buffer)
        # Display the graph in Streamlit
        #st.pyplot(plt)
        exp = st.expander("**To view more info about each of the FlyHigh traveller's joy factor, expand**")
        with exp:
            st.write('<p style="color:black; font-weight:bold;">Below are the various factors related to airline passenger satisfaction along with their descriptions:</p>', unsafe_allow_html=True)

            st.markdown('<p style="color:black;"><strong>Gender : </strong>The demographic information pertaining to passengers, distinguishing between Female and Male travelers.', unsafe_allow_html=True)
            st.markdown('<p style="color:black;"><strong>Customer Type : </strong>Categorization based on passenger loyalty, differentiating between Loyal Customers and Disloyal Customers.', unsafe_allow_html=True)
            st.markdown('<p style="color:black;"><strong>Age : </strong>The precise numerical representation of the passenger\'s age, indicating their stage in life.', unsafe_allow_html=True)
            st.markdown('<p style="color:black;"><strong>Type of Travel : </strong>Defines the purpose of the passenger\'s flight, distinguishing between Personal Travel and Business Travel objectives.', unsafe_allow_html=True)
            st.markdown('<p style="color:black;"><strong>Class : </strong>Indicates the travel class within the airplane, offering choices between Business, Economy, and Economy Plus classes.', unsafe_allow_html=True)
            st.markdown('<p style="color:black;"><strong>Flight Distance : </strong>The measurement of the journey\'s distance traveled by the flight.', unsafe_allow_html=True)
            st.markdown('<p style="color:black;"><strong>Inflight Wifi Service : </strong>A measure of satisfaction regarding the availability and quality of the onboard wifi service, rated from \'Not Applicable\' to a scale of 1 to 5.', unsafe_allow_html=True)
            st.markdown('<p style="color:black;"><strong>Departure/Arrival Time Convenience : </strong>Satisfaction level concerning the convenience of departure and arrival times.', unsafe_allow_html=True)
            st.markdown('<p style="color:black;"><strong>Ease of Online Booking : </strong>The degree of satisfaction experienced during the online booking process.', unsafe_allow_html=True)
            st.markdown('<p style="color:black;"><strong>Gate Location : </strong>Satisfaction level regarding the location of gates within the airport.', unsafe_allow_html=True)
            st.markdown('<p style="color:black;"><strong>Food and Drink : </strong>Level of satisfaction with the quality and availability of food and drink options onboard.', unsafe_allow_html=True)
            st.markdown('<p style="color:black;"><strong>Online Boarding : </strong>Satisfaction level concerning the online boarding process.', unsafe_allow_html=True)
            st.markdown('<p style="color:black;"><strong>Seat Comfort : </strong>A measure of satisfaction with the comfort level of the seating arrangement.', unsafe_allow_html=True)
            st.markdown('<p style="color:black;"><strong>Inflight Entertainment : </strong>Satisfaction level regarding the availability and quality of entertainment during the flight.', unsafe_allow_html=True)
            st.markdown('<p style="color:black;"><strong>On-board Service : </strong>Level of satisfaction with the overall service provided onboard the flight.', unsafe_allow_html=True)
            st.markdown('<p style="color:black;"><strong>Leg Room Service : </strong>Satisfaction level with the service related to legroom space onboard.', unsafe_allow_html=True)
            st.markdown('<p style="color:black;"><strong>Baggage Handling : </strong>Satisfaction level concerning the handling of baggage during the journey.', unsafe_allow_html=True)
            st.markdown('<p style="color:black;"><strong>Check-in Service : </strong>Level of satisfaction with the service provided during the check-in process.', unsafe_allow_html=True)
            st.markdown('<p style="color:black;"><strong>Inflight Service : </strong>Satisfaction level concerning the service provided during the flight.', unsafe_allow_html=True)
            st.markdown('<p style="color:black;"><strong>Cleanliness : </strong>Level of satisfaction regarding the cleanliness maintained onboard the flight.', unsafe_allow_html=True)
            st.markdown('<p style="color:black;"><strong>Departure Delay in Minutes : </strong>The duration of delay during departure, measured in minutes.', unsafe_allow_html=True)
            st.markdown('<p style="color:black;"><strong>Arrival Delay in Minutes : </strong>The duration of delay during arrival, measured in minutes.', unsafe_allow_html=True)
            st.markdown('<p style="color:black;"><strong>Satisfaction : </strong>The overall satisfaction level of passengers, categorized as Satisfaction, Neutral, or Dissatisfaction with the airline experience.', unsafe_allow_html=True)
    
#Inclusions when navigated to the Overall Airline stats page
elif selected == "Overall Airline Stats":
    st.markdown('<h2 style="color:black;">FlyHigh Passenger Stats Gallery</h2>', unsafe_allow_html=True)

    st.markdown('<em>Explore the Comprehensive Insights of FlyHigh Airlines Brand Performance. Dive into the analysis of crucial factors like age and gender, evaluating the satisfaction levels of our esteemed past passengers. Engage with captivating visualizations and uncover the story behind our passengers experiences!</em>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(['Tabulated Stats', 'Graphical Stats'])
    with tab1:
        column1, space, column2 = st.columns([5,1,5])
        with column1:
            st.metric("Average Age of Passengers at FlyHigh", round(flight_df["Age"].mean()))
            st.metric("Average Flight Distance travelled by passengers at FlyHigh", round(flight_df["Flight Distance"].mean()))
            st.metric("Most frequently selected Customer Type", flight_df["Customer Type"].mode()[0])
            #st.dataframe(flight_df[["Flight Distance", "Age", "Departure Delay in Minutes", "Arrival Delay in Minutes"]].describe(), width=710, height=315)
        with column2:
            st.metric("Most frequently selected Travel Type of FlyHigh passengers", flight_df["Type of Travel"].mode()[0])
            st.metric("Most frequently selected Passenger Travel Class", flight_df["Class"].mode()[0])
            
        st.markdown('<hr>', unsafe_allow_html=True)
    
    with tab2:
        #st.markdown('<h3 style="color:black;">FlyHigh Graphical Stats Gallery</h3>', unsafe_allow_html=True)
        
        col1,col2 = st.columns([3,3])
        with col1:

            #extract counts of the 'satisfaction' feature and use these counts for creating a pie chart with labels and values
            customer_type_counts = flight_df['satisfaction'].value_counts()
            values = customer_type_counts.values
            labels = customer_type_counts.index
            colors = ['#BFEFFF', '#1E90FE']

            
            fig = go.Figure(data=go.Pie(values=values, labels=labels, pull=[0.01, 0.04, 0.01, 0.05], hole=0.45, marker_colors=colors))

            fig.update_traces(hoverinfo='label+percent', textinfo='percent', textfont_size=20)

            fig.add_annotation(x=0.5, y=0.5, text='Satisfaction',
                            font=dict(size=18, family='Verdana', color='black'), showarrow=False)
            st.markdown('<p style="color:black;font-weight:bold;">Overall passenger satisfaction at FlyHigh Airlines</p>', unsafe_allow_html=True)
            st.markdown("<p style='text-align:justify;'>Representation of the Overall passenger satisfaction at FlyHigh categorized into satisfied and neutral or dissatisfied' types.  According to the recent survey data, the passengers at FlyHigh are not very satisfied with their travel experiences as the satisfaction quotient is just marginally better.</p>", unsafe_allow_html=True)
            #st.markdown('<h3 style="color:black;">Overall passenger satisfaction at FlyHigh Airlines</h3>', unsafe_allow_html=True)

            #Gender wise passenger percentage is computed
            gender_counts = flight_df['Gender'].value_counts()
            gender_percentage = (gender_counts / len(flight_df)) * 100
            fig2 = plt.figure(
                FigureClass=Waffle,
                rows=5,
                figsize=(9, 6),
                values=gender_percentage,
                labels=[f"Female ({gender_percentage['Female']:.2f}%)", f"Male ({gender_percentage['Male']:.2f}%)"],  # legend labels with percentages
                colors=["#FF82AB", "#1E90FE"],
                icons=['female', 'male'],
                legend={'loc': 'lower center',
                        'bbox_to_anchor': (0.5, -0.5),
                        'ncol': len(gender_counts),
                        'framealpha': 0.5,
                        'fontsize': 12
                        },
                icon_size=15,
                icon_legend=True,
            )   
            
            #Plot 1 - Pie chart for satisfaction
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            #Plot 3 - Sunburst chart w=inidcating the satisfaction of each customer type
            st.markdown('<p style="color:black;font-weight:bold;">Proportion of Satisfaction based on Customer Type</h3>', unsafe_allow_html=True)
            st.markdown("<p style='text-align:justify;'>Recent survey study representation of FlyHigh passenger satisfaction based on their loyalty of being a loyal or disloyal Type of Customer for the airline brand which indicate that passengers who aren't FlyHigh valued customers have mostly reported unpleasant travel experiences which may lead to negative publicity on the brand.</p>", unsafe_allow_html=True)
            fig = px.sunburst(flight_df,path=["Customer Type","satisfaction"],template="plotly", width=520, height=450)
            st.plotly_chart(fig)
        
        #Function to categorize travellers based on age group
        # Applying categorize_age() to 'Age' column in flight_df to create a new column 'Age_Group' based on categorized age groups   
        age_counts = flight_df['Age_Group'].value_counts()
        colors = ['#1E90FF', '#98F5FF']

        col1,space,col2 = st.columns([5,1,5])
        #Plot 4 - Pie chart showing each Age category distribution
        with col1:
            
            st.markdown('<p style="color:black;font-weight:bold;">Traveller Age category distribution</p>', unsafe_allow_html=True)
            st.markdown("<p style='text-align:justify;'>FlyHigh caters to passengers ranging from infants to Seniors taking into consideration the age specific needs of a passenger based on his age. Currently, Adults seem to extensively use the airline services to travel across the globe which conveys the areas we can work on to attract more loyal customers.</p>", unsafe_allow_html=True)
            fig = px.pie(
                values=age_counts.values,
                names=age_counts.index,
                color_discrete_sequence=colors
            )

            fig.update_traces(textinfo='percent', pull=[0, 0], textfont=dict(size=18),insidetextorientation='auto') 

            fig.update_layout(
                showlegend=True,
                #title_font=dict(size=15),
                width=510,
                height=450
            )
            st.plotly_chart(fig)


        #Plot 5 - Bar plot for age group distribution
        with col2:
            
            st.markdown('<p style="color:black;font-weight:bold;">Age Group Analysis</p>', unsafe_allow_html=True)
            st.markdown("<p style='text-align:justify;'>FlyHigh passenger Age Group representation where each valid passenger age is displayed in intervals to observe target passenger age group who are most likely to fly with the airline. This visual representation allows the observation of each age relative to another.</p>", unsafe_allow_html=True)
            #Count the occurrences of each age in the 'Age' column and then resetting the index to obtain the count of each unique value in the 'Age' column
            age_count = flight_df['Age'].value_counts().reset_index()
            fig = px.bar(
                age_count,
                x='Age',
                y='count',
                #title='Age Group Analysis',
                labels={'Count': 'Number of Customers'},
                color='Age',
                color_discrete_sequence=px.colors.sequential.Blues[::-1], 
            )

            fig.update_traces(
                text=age_count['count'], 
                textposition='outside', 
                marker=dict(line=dict(color='#000000', width=1)), 
            )

            fig.update_layout(
                xaxis_title='Age Group',
                yaxis_title='Number of Customers',
                font=dict(size=12),
                #title_font=dict(size=16),
                showlegend=False,
                plot_bgcolor='#FFFFFF',
                margin=dict(l=25, r=20, t=100, b=30),
                width=500,
            )
            st.plotly_chart(fig)

        
        #Plot 2 - Waflle chart for gender distribution
        st.markdown('<p style="color:black;font-weight:bold;">Overall FlyHigh Airlines Gender Distribution pattern</p>', unsafe_allow_html=True)
        st.markdown("<p style='text-align:justify;'>FlyHigh aims to be familiar with their passengers and know how they can be considerate of the needs with regard to Gender so that the valued passenger feels taken care of even in terms of their gender specific requirements. FlyHigh observes a proportionate share of male and female passengers.</p>", unsafe_allow_html=True)
        st.pyplot(fig2)
        

# ANALYSIS PAGE
    
#ADVANCED ANALYSIS
elif selected == 'Analysis Page':

    c = 0
    st.markdown('<h2 style="color:black";font-size:20px;"> Immersive Data Exploration Hub<h2>', unsafe_allow_html=True)
    st.markdown('<em>The FlyHigh R&D team can leverage these intricate passenger experience insights to uncover the depths of customer satisfaction, fostering innovative ideas to elevate our services and strengthen our brand reputation for unparalleled joyous travel experiences. </em>', unsafe_allow_html=True)
    #with st.sidebar:
        
    #model = joblib.load("model.pkl")
    tab1, tab2, tab3, tab4,tab5 = st.tabs(['Data Obseravtion center','Data Insights Discovery Center','Hi-Dimensional plot', 'Satisfaction Prediction','Passenger Data Upload'])

    with tab1:
        st.markdown('<p style="text-align:justify;font-weight:bold;">FlyHigh passeneger survey data was collected from Kaggle website.It encompasses data obtained from more than 1,03,000 passengers who have travelled with the airline brand. The data involves around 25 passenger joy factors amongst which 2 are insignificant ones are eliminated and the 23 factors which are crucial for a passenger to rate the experience as a meorable one.</p>', unsafe_allow_html=True)
        flight_df = flight_df.drop(columns=['Unnamed: 0', 'id'])
        st.write(flight_df) 
        ch_b = st.checkbox("**Please select the checkbox to view the categorical passenger joy factors data**")
        if ch_b:
            st.dataframe(flight_df.describe(exclude="number"), width=710, height=200)
    with tab2:
        st.markdown('<h2 style="color:black";font-size:20px;"> Data Insights Discovery Center<h2>', unsafe_allow_html=True)
        st.markdown('<em>Uncover the perfect blend of journey elements that craft an unforgettable travel experience, leveraging advanced data visualization tools to discern evolving trends and pivotal moments in our passengers journeys. </em>', unsafe_allow_html=True)
        selected_features = []
        #Columns 'Unnamed: 0' and 'id' are dropped as they have insignificant data
        #flight_df = flight_df.drop(columns=['Unnamed: 0', 'id'])
        columns = list(flight_df.columns)
        categorical_data = list(set(flight_df.columns) - set(flight_df._get_numeric_data().columns))
        non_categorical_data = list(set(columns) - set(categorical_data))   



        options = [
        "Select for visualizing Relationships between numerical joy factors",
        "Select to Display Distribution and identifying peaks,detecting gaps and viewing observation frequency patterns amongst the passenger joy factors",
        "Select to display the contribution or proportion of each joy factor in passenger feedback data",]
        

        # Display a radio button to select an option
        plot_option = st.radio("Plot options", options)
        
        if 'visualizing' in plot_option:
            feature_options = st.multiselect('Select 2 Passenger joy factors', non_categorical_data, key="multiselect") 
            if len(feature_options)!=2:
                st.warning('Please select 2 Passenger joy factors for visualizing relationships')
            if len(feature_options) ==2:
                categorical_feature = st.selectbox('Select the factor against which you want to analyse the already selected feature', categorical_data)
                if categorical_feature:
                    # Plot 7 - Scatter plot based on selected features 
                    st.pyplot(sns.scatterplot(data=flight_df, x=feature_options[0], y=feature_options[1], hue=categorical_feature).figure)
                
        elif 'Display' in plot_option:
            feature_options = st.multiselect('Select a Feature', non_categorical_data, key="multiselect") 
            if len(feature_options) >1:
                st.warning('Please select one Passenger joy factor for viewing graphical bin wise distribution of numerical variables')
            if len(feature_options) == 1:
                # Selection of feature provided for user 
                categorical_feature = st.selectbox('Select the Passenger joy factor against which you want to analyse the already selected feature', categorical_data)
                if categorical_feature:
                    fig=px.histogram(flight_df,x=feature_options[0],color=flight_df[categorical_feature],title=f"{feature_options[0]} vs {categorical_feature}",
                            color_discrete_sequence=px.colors.qualitative.Vivid)
                    fig.update_layout(template="plotly")
                    fig.update_layout(title_font_size=30)
                    #Plot 8 - Histogram based on features selected
                    st.plotly_chart(fig)
        
        elif 'contribution' in plot_option:
            categorical_feature = st.selectbox('Select a categorical Passenger joy factor for visualization', categorical_data) 
            non_categorical_feature = st.selectbox('Please select a non-categorical Passenger joy factor for viewing the percentage composition of categories and comparing their relative sizes', non_categorical_data)    
            plt.figure(figsize=(20,10))
            fig=px.pie(values=flight_df[non_categorical_feature], names=flight_df[categorical_feature])
            #Plot 9 - Pie chart
            st.plotly_chart(fig, theme="streamlit")

    with tab3:
        #Hi-dimensional plot for the passenger satisfaction factors is plotted
        st.markdown('<p style="text-align:justify;font-weight:bold;">Representation of a Hi-dimensional display of the passenger joy factors for an in depth analysis of interrelation between multiple features.Explore the functionalities offered by the visualization plot by playing around with the feature rearrangemnet, export data and other options to discern the data better.</p>',unsafe_allow_html = True)
        df_f = flight_df.select_dtypes(include=[np.number])
        cols = flight_df[['Age', 'Gender', 'Customer Type', 'Type of Travel', 'Flight Distance','satisfaction']]
        hiplot_exp = hip.Experiment.from_dataframe(cols)
        hiplot_html = hiplot_exp.to_html()
        st.components.v1.html(hiplot_html, width=800, height=1350)
    
    with tab4:
        st.markdown('<p style="color:black";font-size:20px;"><b><em>Lets role play and see how a new passengers current review would predict his satisfaction quotient</em></b></p>',unsafe_allow_html = True)
        Customer_Type = st.selectbox("Select Customer Type", options=['Loyal Customer', 'disloyal Customer'])
        type_of_travel = st.selectbox("Select Type of Travel", options=['Personal Travel', 'Business travel'])
        Class = st.selectbox("Select Class", options=['Eco Plus', 'Business', 'Eco'])
        Gender = st.selectbox("Select Gender", options=['Male', 'Female'])

        ## nums.
        flight_Distance = st.number_input("input flight distance".title(), value=int(flight_df["Flight Distance"].mean()), step=100)
        arrival_delay = st.number_input("input Arrival Delay (Minutes)".title(), value=flight_df["Arrival Delay in Minutes"].median(), step=10.0)
        dep_delay = st.number_input("input Departure Delay (Minutes)".title(), value=flight_df["Arrival Delay in Minutes"].median(), step=10.0)
        age = st.slider("Age", min_value=1, max_value=100, step=1)
        

        CType_mapping = {'disloyal Customer': 0, 'Loyal Customer': 1}
        TravelType_mapping = {'Personal Travel': 0, 'Business travel': 1}
        Class_mapping = {'Eco Plus': 0, 'Eco': 1, 'Business': 2}
        Gender_mapping = {'Male': 0, 'Female': 1}
        flight_df['Customer Type'] = flight_df['Customer Type'].map(CType_mapping)
        flight_df['Type of Travel'] = flight_df['Type of Travel'].map(TravelType_mapping)
        flight_df['Class'] = flight_df['Class'].map(Class_mapping)
        flight_df['Gender'] = flight_df['Gender'].map(Gender_mapping)

        if Customer_Type=='disloyal Customer':
            cust_type=0
        elif Customer_Type=='Loyal Customer':
            cust_type=1
        if type_of_travel=='Personal Travel':
            t_type=0
        elif type_of_travel=='Business travel':
            t_type=1
        if Class=='Eco Plus':
            class_type=0
        elif Class=='Eco':
            class_type=1
        elif Class=='Business':
            class_type=2
        if Gender=='Male':
            gender=0
        elif Gender=='Female':
            gender=1

        ## ready.
        Leg_room = st.radio("Select Leg room service rate", options=[0, 1, 2, 3, 4, 5] , horizontal=True)
        food_drink = st.radio("Select Food and drink rate", options=[0, 1, 2, 3, 4, 5] , horizontal=True)
        gate_loc = st.radio("Select Gate location rate", options=[0, 1, 2, 3, 4, 5] , horizontal=True)
        online_boarding = st.radio("Select Online boarding rate", options=[0, 1, 2, 3, 4, 5] , horizontal=True)
        baggage_handling = st.radio("Select Baggage handling rate", options=[0, 1, 2, 3, 4, 5] , horizontal=True)
        onboard_service = st.radio("Select On-board service rate", options=[0, 1, 2, 3, 4, 5] , horizontal=True)
        inflight_wifi = st.radio("Select Inflight wifi service rate", options=[0, 1, 2, 3, 4, 5] , horizontal=True)
        online_booking = st.radio("Select Online booking rate", options=[0, 1, 2, 3, 4, 5] , horizontal=True)
        cleanliness = st.radio("Select Cleanliness rate", options=[0, 1, 2, 3, 4, 5] , horizontal=True)
        inflight_entertainment = st.radio("Select Inflight entertainment rate", options=[0, 1, 2, 3, 4, 5] , horizontal=True)
        inflight_service = st.radio("Select Inflight service rate", options=[0, 1, 2, 3, 4, 5] , horizontal=True)
        seat_comfort = st.radio("Select Seat comfort rate", options=[0, 1, 2, 3, 4, 5] , horizontal=True)
        checkin_service = st.radio("Select Checkin service rate", options=[0, 1, 2, 3, 4, 5] , horizontal=True)
        arrival_conv = st.radio("Select Arrival time convenience rate", options=[0, 1, 2, 3, 4, 5] , horizontal=True)       
       
        ## Create a button
        if st.button('Predict Satsfication', help='Click to predict satisfaction'):
            new_input = {'Gender': [gender], 'Customer Type': [cust_type], 'Age': [age], 'Type of Travel': [t_type], 'Class': [class_type], 'Flight Distance': [flight_Distance], 'Inflight wifi service': [inflight_wifi],
        'Departure/Arrival time convenient': [arrival_conv],'Ease of Online booking':[online_booking],'Gate location':[gate_loc],'Food and drink':[food_drink],'Online boarding':[online_boarding],'Seat comfort':[seat_comfort],'Inflight entertainment':[inflight_entertainment],'On-board service':[onboard_service],'Leg room service':[Leg_room],'Baggage handling':[baggage_handling],'Checkin service':[checkin_service],'Inflight service':[inflight_service],'Cleanliness':[cleanliness],'Departure Delay in Minutes':[dep_delay],'Arrival Delay in Minutes':[arrival_delay]}
            new_input=pd.DataFrame(new_input)
            loaded_scaler = joblib.load('minmax_scaler_model.joblib')
            loaded_scaled_data = joblib.load('scaled_data.joblib')
            X_test_scaled = loaded_scaler.transform(new_input)

            # Load the pickled model
            with open('model.pkl', 'rb') as file:
                model = pickle.load(file)
            
            #sample_processed = new_process(new_sample=new_input)
            pred = model.predict(X_test_scaled)

            ## Display Results
            if pred == 'satisfied':
                st.success(f'Given the above ratings, the passenger is predicted to be {pred}')
            elif pred == 'neutral or dissatisfied':
                st.error(f'Given the above ratings, the passenger is predicted to be {pred}')
            
            if (pred == "satisfied"):
                st.image("satisfied_customer.jpeg")
            elif (pred =="neutral or dissatisfied"):
                st.image("unsatisfied_customer.jpg",width=250)

    with tab5:
        #with st.expander("Upload File"):
        st.markdown('<p style="text-align:justify;font-weight:bold;">This section allows you to upload a new passenger survey dataset. Make sure to upload a survey data file of the specified file format which follows the dataset allowed factors list</p>',unsafe_allow_html = True)
        uploaded_file = st.file_uploader("Please upload the test data in csv file format", type=['xlsx',"csv"])
        if uploaded_file is not None:
            # File upload successful
            

            # Process the uploaded file (you can customize this part based on your needs)
            try:
                if uploaded_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                    df = pd.read_excel(uploaded_file)
                else:

                    df = pd.read_csv(uploaded_file)
                    columns_equal = list(df.columns) == list(flight_df_original.columns)
                    df_equal = df.equals(flight_df_original)
                    if columns_equal and df_equal:
                        st.success("File uploaded successfully to the database!")
                        st.write("Uploaded Data:")
                        st.write(df)
                    else:
                        st.error('Invalid file format')              
                # Display the uploaded data
                
                
                # Add further processing or analysis as needed
            except Exception as e:
                st.error(f"Error reading the file: {e}")
            
        


#ANALYSIS RESULTS
elif selected == "Analysis Results":
    st.markdown('<h2 style="color:black";font-size:20px;">Key Takeaways</h2>', unsafe_allow_html=True)
    st.markdown("""
    **This summary report represents the analysis of overall passenger satisfaction parameters and the impact of each factor on their travel experience. The displayed data is subject to weekly updates, reflecting real-time survey data collected by our R&D team.**
    """, unsafe_allow_html=True)
    st.markdown("""
    <style>
    .custom_bullet {
        list-style-type: none;
    }
    </style>

    <div class="custom_bullet">
        <p><b>&rarr; A major concern for the airline is that 56.7% of passengers are either neutral or dissatisfied.</p>
        <p><b>&rarr; Passenger satisfaction does not appear to be influenced by gender. However, it seems to be affected by factors such as age, flight delays, and specific services, among other variables.</b></p>
        <p><b>&rarr; The majority of the passengers appear to be neutral or unsatisfied, with the majority of the travelers being female.</b></p>
        <p><b>&rarr; Most of the travelers fall in the age group of 22yrs -50yrs. People who are satisfied tend to be in their 40s to 60s. Most of the unhappy passengers are between the ages of 20 and 40.</b></p>
        <p><b>&rarr; When it comes to travelers on business trips, they are typically a little older than those traveling for personal reasons.</b></p>
        <p><b>&rarr; The distance range of passengers travelling for Personal reasons travel uptil a distance range of 2500 miles whereas for Business travel purposes they travel farther.</b></p>
        <p><b>&rarr; Airlines' services are rated a 4 out of 5, with luggage handling and in-flight service being the best and in-flight Wi-Fi service being the worst.</b></p>
    </div>
    """, unsafe_allow_html=True)

#MANAGER FEEDBACK
elif selected == "Manager Feedback":
    st.markdown('<h2 style="color:black";font-size:20px;">Suggestion from the Manager to the Research and Development team of FlyHigh</h3>', unsafe_allow_html=True)

    input_text = st.text_input("Type in you're feedback here")
    arrow_clicked = st.button("Share")
    # Check if the arrow button is clicked
    if arrow_clicked and input_text:
        # Perform actions based on the input text
        st.success(f"Suggestion shared succefully!")
    if arrow_clicked and not input_text:
        st.error(f"Please enter a suggestion")
#elif selected == 'Contact Us':
    #st.sidebar.markdown(f'<a href="https://flyhighproject-7fmy8ekgwxnxu8d4cwyqhr.streamlit.app"><button>Logout</button> </a>', unsafe_allow_html=True)
st.sidebar.markdown(f'<a href="https://flyhighmainpage-l9t2hc8dwoagy3cpn63mju.streamlit.app"><button>Logout</button> </a>', unsafe_allow_html=True)


#Standard scalar
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
LE = LabelEncoder()
print(flight_df)
flight_df['Class'] = LE.fit_transform(flight_df['Class'])
flight_df['satisfaction'] = LE.fit_transform(flight_df['satisfaction'])
flight_df['Type of Travel'] = LE.fit_transform(flight_df['Type of Travel'])
flight_df['Gender'] = LE.fit_transform(flight_df['Gender'])
flight_df['Customer Type'] = LE.fit_transform(flight_df['Customer Type'])

features = flight_df.drop(columns=['satisfaction','Age_Group'],axis=1)
target = flight_df['satisfaction']


X_train,X_test,y_train,y_test = train_test_split(features,target,test_size=0.2,random_state=42)

sd = StandardScaler()
X_train_scaled = sd.fit_transform(X_train)
X_test_scaled = sd.transform(X_test)

# X_train_scaled has the features scaled to one scale for further predictive modelling for Phase 2 of the project

        



            
        
        
        
