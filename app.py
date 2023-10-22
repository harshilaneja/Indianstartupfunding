import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='Startup Analysis')
df=pd.read_csv('startup_cleaned.csv')
df['date']=pd.to_datetime(df['date'],errors='coerce')
df['month']=df['date'].dt.month
df['year']=df['date'].dt.year

def load_overall_analysis():
    st.title('Overall Analysis')
    total=round(df['amount'].sum())
    # max amount
    max_funding=df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    avg_funding=df.groupby('startup')['amount'].sum().mean()
    #total funded start up

    num_startups= df['startup'].nunique()

    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric('Total', str(total) + 'Cr')
    with col2:
        st.metric('Max', str(max_funding) + 'Cr')
    with col3:
        st.metric('Avg', str(round(avg_funding)) + 'Cr')
    with col4:
        st.metric('Funded startups', str(num_startups) + 'Cr')

    st.header('MOM graph')
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    fig5, ax5 = plt.subplots()
    ax5.plot(temp_df['x_axis'], temp_df['amount'])
    st.pyplot(fig5)




def load_investor_details(investor):
    st.title(investor)
    # load recent 5 investment of investor
    last5_df=df[df['investors'].str.contains(investor)].head()[
        ['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    col1,col2=st.columns(2)
    with col1:
        #biggest investment

        big_series=df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)

    with col2:
        verical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()

        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(verical_series, labels=verical_series.index, autopct="%0.01f%%")

        st.pyplot(fig1)

    col3, col4 = st.columns(2)
    with col3:


        round_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Round of Investments')
        fig2, ax2 = plt.subplots()
        ax2.pie(round_series,labels=round_series.index, autopct="%0.01f%%")
        st.pyplot(fig2)

    with col4:
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()

        st.subheader('cities invested in')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels=city_series.index, autopct="%0.01f%%")

        st.pyplot(fig3)



    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()

    st.subheader('YoY Investment')
    fig4, ax4 = plt.subplots()
    ax4.plot(year_series.index, year_series.values)

    st.pyplot(fig4)

    investor_sectors = df[df['investors'].str.contains(investor)]['vertical'].unique()


    similar_investors_by_sector = df[df['vertical'].isin(investor_sectors) & ~df['investors'].str.contains(investor)][
        'investors'].unique()[:5]


    st.title(f'Similar Investors to {investor}')
    st.subheader('Investors with Similar Sectors:')
    st.write(", ".join(similar_investors_by_sector))

def load_startup_details(selected_startup):
    st.title('Startup Analysis')
    st.write(selected_startup)
    st.write(df[df['startup'] == selected_startup][['vertical','subvertical','city','investors','round','date']])



st.sidebar.title('Startup Funding Analysis')

option=st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

if option =='Overall Analysis':
    load_overall_analysis()


elif option =='Startup':
    selected_startup=st.sidebar.selectbox('select startup',sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button('Find startup Details')

    if btn1:
        load_startup_details(selected_startup)
        startup_details = df[df['startup'] == selected_startup]
        similar_companies = df[
            (df['vertical'] == startup_details['vertical'].iloc[0]) &  # Matching vertical


            (df['startup'] != selected_startup)  # Exclude the selected startup
            ][:5]
        if not similar_companies.empty:
            st.subheader('Similar Companies:')
            st.dataframe(similar_companies)
        else:
            st.write('No similar companies found.')

elif option=='Investor':
    selected_investor=st.sidebar.selectbox('select startup',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find investors Details')
    if btn2:
        load_investor_details(selected_investor)


