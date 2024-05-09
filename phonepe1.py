import os
import pandas as pd
import json
import mysql.connector
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image


# streamlit:
icon = Image.open("logo.png")
st.set_page_config(page_title= "PHONEPE DATA VISUALIZATION",
                   layout= "wide")

# SQL connection:
mydb = mysql.connector.connect( host="localhost",
                                user="root",
                                password="Keerthanaa9799",
                                database="phonepe_data",
                                port="3306")

cursor = mydb.cursor()

with st.sidebar:
    select = option_menu("Menu", ["Home","Top Charts","Explore Data"], 
                icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})

if select == "Home":
    st.image("download.png")

elif select =="Top Charts":

    tab1,tab2,tab3 =st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])

    with tab1:

        method =  st.radio("Select The Method",["Agg_Insurance_Analysis","Agg_Transaction_Analysis","Agg_User_Analysis"])
        if method == "Agg_Insurance_Analysis":
                
                column1,column2= st.columns(2)

                with column1:
                  Year = st.slider("**Year**", min_value=2020, max_value=2023)
                
                cursor.execute(f"select State, sum(Transaction_count) as Total_Count,sum(Transaction_amount) as Total_Amount from agg_insu where years in (2018,2019,2020,2021,2022,2023) and quarter in(1,2,3,4) group by State order by Total_Amount desc limit 36")
                df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Count','Total_Amount'])
                fig = px.bar(df,
                                title='agg_insurance',
                                x="State",
                                y="Total_Amount",
                                orientation='h',
                                color='Total_Count',
                                color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)

        elif method == "Agg_Transaction_Analysis":
            column1,column2= st.columns(2)

            with column1:
                  Year = st.slider("**Year**", min_value=2018, max_value=2023)

            cursor.execute(f"select state, sum(Transaction_Count) as Total_Transaction_count, sum(Transaction_amount) as Total_Transaction_amount from agg_transaction where years in (2018,2019,2020,2021,2022,2023) and quarter in(1,2,3,4) group by state order by Total_Transaction_amount desc limit 36")
            df = pd.DataFrame(cursor.fetchall(), columns=['State','Transaction_Count','Transaction_amount'])

            fig = px.pie(df,values='Transaction_amount',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transaction_Count'],
                             labels={'Transaction_Count':'Transaction_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label') 
            st.plotly_chart(fig,use_container_width=True)

        elif method =="Agg_User_Analysis":
            column1,column2= st.columns(2)
            
            with column1:
                Year = st.slider("**Year**", min_value=2018, max_value=2023) 
            
            cursor.execute(f"select Brands, sum(Transaction_count) as Total_Count, avg(Percentage)*100 as Avg_Percentage from agg_user where years in (2018,2019,2020,2021,2022,2023) and quarter in(1,2,3,4) group by Brands order by Total_Count desc limit 36")
            df = pd.DataFrame(cursor.fetchall(), columns=['Brands', 'Total_Count','Avg_Percentage'])
            fig = px.bar(df,
                            title='Top 10',
                            x="Total_Count",
                            y="Brands",
                            orientation='h',
                            color='Avg_Percentage',
                            color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)
 
    with tab2:
        method2=st.radio("select the method",["Map_Insurance_Analysis","Map_Transaction_Analysis","Map_User_Analysis"])
        if method2 == "Map_Insurance_Analysis":
            column1,column2= st.columns(2)
            
            with column1:
                # Year = st.slider("**Year**", min_value=2020, max_value=2023)

             cursor.execute(f"select State, sum(Transaction_count) as Total_Counts, sum(Transaction_amount) as Total_Amounts from map_insurance where years in (2018,2019,2020,2021,2022,2023) and quarter in(1,2,3,4) group by State order by Total_Amounts desc limit 36")
             df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Counts','Total_Amounts'])
             fig = px.bar(df,
                            title='map insu',
                            x="State",
                            y="Total_Amounts",
                            orientation='h',
                            color='Total_Counts',
                            color_continuous_scale=px.colors.sequential.Agsunset)
             st.plotly_chart(fig,use_container_width=True)

        elif method2 == "Map_Transaction_Analysis":
            # column1,column2= st.columns(2)
            
            # with column1:
            #     Year = st.slider("**Year**", min_value=2018, max_value=2023)

            cursor.execute(f"select district , sum(Count) as Total_Count, sum(Amount) as Total from map_transaction where year in (2018,2019,2020,2021,2022,2023) and quarter in(1,2,3,4) group by district order by Total desc limit 36")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                                names='District',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

        elif method2 =="Map_User_Analysis":
            # column1,column2= st.columns(2)
            
            # with column1:
            #     Year = st.slider("**Year**", min_value=2018, max_value=2023)

            cursor.execute(f"select District, sum(RegisteredUser) as Total_Users, sum(Appopens) as Total_Appopens from map_user where years in (2018,2019,2020,2021,2022,2023) and quarter in(1,2,3,4) group by District order by Total_Users desc limit 36")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                title='Top 10',
                x="Total_Users",
                y="District",
                orientation='h',
                color='Total_Users',
                color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)
    
    with tab3:
        method3=st.radio("select the method",["Top_Insurance_Analysis","Top_Transaction_Analysis","Top_User_Analysis"])
        if method3 == "Top_Insurance_Analysis":
            # column1,column2= st.columns(2)
            
            # with column1:
            #     Year = st.slider("**Year**", min_value=2020, max_value=2023)

            cursor.execute(f"select State, sum(Transaction_count) as Total_Counts, sum(Transaction_amount) as Total_Amounts from top_insurance where years in (2018,2019,2020,2021,2022,2023) and quarter in(1,2,3,4) group by State order by Total_Amounts desc limit 36")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Counts','Total_Amounts'])
            fig = px.bar(df,
                            title='Top insu',
                            x="State",
                            y="Total_Amounts",
                            orientation='h',
                            color='Total_Counts',
                            color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)

        elif method3 == "Top_Transaction_Analysis":
            # column1,column2= st.columns(2)
            
            # with column1:
            #     Year = st.slider("**Year**", min_value=2018, max_value=2023)

            cursor.execute(f"select pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_transaction where years in (2018,2019,2020,2021,2022,2023) and quarter in(1,2,3,4) group by pincode order by Total desc limit 36")
            df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                                names='Pincode',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

        elif method3 =="Top_User_Analysis":
            # column1,column2= st.columns(2)
            
            # with column1:
            #     Year = st.slider("**Year**", min_value=2018, max_value=2023)

            cursor.execute(f"select Pincodes, sum(RegisteredUsers) as Total_Users from top_user where year in (2018,2019,2020,2021,2022,2023) and quarter in(1,2,3,4) group by Pincodes order by Total_Users desc limit 36")
            df = pd.DataFrame(cursor.fetchall(), columns=['Pincodes', 'Total_Users'])
            fig = px.bar(df,
                            title='Top 10',
                            x="Total_Users",
                            y="Pincodes",
                            orientation='h',
                            color='Total_Users',
                            color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)
            

elif select =="Explore Data":
    
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2022)
    Type = st.sidebar.selectbox("**Type**", ("Map_Transactions", "Map_Users"))
    col1,col2 = st.columns(2)

    with col1:
    # Overall state transaction:
      st.markdown("## :violet[Overall State Data - Transactions Amount]") 

    cursor.execute(f"select State, sum(Count) as Total_Count, sum(Amount) as Total_Amount from map_transaction where year in (2018,2019,2020,2021,2022,2023) and quarter in(1,2,3,4) group by State order by Total_Amount")
    df = pd.DataFrame(cursor.fetchall(), columns = ['State','Total_Count','Total_Amount'])
    df1 = pd.read_csv('map_trans.csv')
    df .state = df1


    fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color='Amount',
                color_continuous_scale='rainbow')

    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig,use_container_width=True)


# Bar Chart Top Payment type:
    cursor.execute(f"select state, sum(Transaction_Count) as Total_Transaction_count, sum(Transaction_amount) as Total_Transaction_amount from agg_transaction where years in (2018,2019,2020,2021,2022,2023) and quarter in (1,2,3,4) group by state order by Total_Transaction_amount desc limit 36")
    df = pd.DataFrame(cursor.fetchall(), columns=['State','Transaction_Count','Transaction_amount'])

    fig = px.bar(df,
                    title='Transaction_count vs Transaction_amount',
                    x="State",
                    y="Transaction_amount",
                    orientation='v',
                    color='Transaction_amount',
                    color_continuous_scale=px.colors.sequential.Agsunset)
    st.plotly_chart(fig,use_container_width=True)  


# Bar chart district wise data by transaction:
    st.markdown("## :violet[Select any State to explore more]")
    selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
    
    cursor.execute(f"select State, District,year,quarter, sum(Count) as Total_Transactions, sum(Amount) as Total_amount from map_transaction where year in (2018,2019,2020,2021,2022,2023) and quarter in (1,2,3,4) State in (selected_state) group by State, District,year,quarter order by state,district")
            
    df1 = pd.DataFrame(cursor.fetchall(), columns=['State','District','Year','Quarter',
                                                        'Total_Transactions','Total_amount'])
    fig = px.bar(df1,
                    title="selected_state",
                    x="District",
                    y="Total_Transactions",
                    orientation='v',
                    color='Total_amount',
                    color_continuous_scale=px.colors.sequential.Agsunset)
    st.plotly_chart(fig,use_container_width=True)

    

    with col2:
        cursor.execute(f"select state, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where years in(2018,2019,2020,2021,2022,2023) and quarter in (1,2,3,4) group by state order by Total_Appopens")
        df = pd.DataFrame(cursor.fetchall(), columns=['state', 'Total_Users','Total_Appopens'])
        df1 = pd.read_csv('map_user.csv')
        df .State = df1

        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='AppOpens',
                    color_continuous_scale='rainbow')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)



# Bar chart district wise data in map user:
st.markdown("## :violet[Select any State to explore more]")
selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
cursor.execute(f"select State,Years,Quarter,District,sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where years in(2018,2019,2020,2021,2022,2023) and quarter in (1,2,3,4) and state = ('selected_state') group by State, District,Years,Quarter order by state,district")
        
df = pd.DataFrame(cursor.fetchall(), columns=['State','Years', 'Quarter', 'District', 'Total_Users','Total_Appopens'])
df.Total_Users = df.Total_Users.astype(int)

fig = px.bar(df,
                title=selected_state,
                x="District",
                y="Total_Users",
                orientation='v',
                color='Total_Users',
                color_continuous_scale=px.colors.sequential.Agsunset)
st.plotly_chart(fig,use_container_width=True)      




