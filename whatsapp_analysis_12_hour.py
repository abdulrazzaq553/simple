
import streamlit as st
import re

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import emoji
import seaborn as sns

import link
import link2nd


st.set_page_config(page_title="WhatsApp Chat Analysis", page_icon="📊", layout="wide")

# Sidebar styling
st.sidebar.markdown("<h2 style='text-align: center; color: #4A90E2;'>📊 WhatsApp Chat Analysis</h2>", unsafe_allow_html=True)

# File uploader
upload_file = st.sidebar.file_uploader('📁 Choose a File', type=['txt'])


# Check if a file is uploaded
if upload_file is not None:
    bytess_data = upload_file.getvalue()
    chat = bytess_data.decode('utf-8')
    k1 = link.start(chat)
    # st.dataframe(k1)
    st.title('📈 Whatsapp Chat Analysis')

    # User selection
    user_list = k1['User'].unique().tolist()
    user_list.insert(0, 'Overall')
    select_user = st.sidebar.selectbox('👤 Choose User', user_list)

    # Show Analysis button
    if st.sidebar.button('Show Analysis'): 
        total_mesage, total_words = link2nd.select(select_user, k1)
        media_shared = link2nd.media_shared(select_user, k1)
        links = link2nd.url(select_user, k1)
        st.subheader('📝 Message Types')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric('Total Messages', total_mesage)
        with col2:
            st.metric('Total Words', total_words)
        with col3:
            st.metric('Media Shared', media_shared)
        with col4:
            st.metric('Links Shared', links)
        st.subheader('🏆 Most Active Users')
        col1, col2,col3= st.columns(3)
        x1, x2,x3= link2nd.busy_user(select_user, k1)
        with col1:
            fig, ax = plt.subplots()
            ax.bar(x1.index, x1.values, color='g')
            plt.xticks(rotation=90, size=12)
            st.pyplot(fig)
        with col2:
            st.dataframe(x2)
        with col3:
            st.dataframe(x3)

        # Busy Days Section
        st.subheader('📅 Busy Days')
        col1, col2 = st.columns(2)
        with col1:
            days2 = link2nd.days(select_user, k1)
            fig, ax = plt.subplots()
            ax.bar(days2['dayss'], days2['Message'], color='skyblue')
            st.pyplot(fig)
        with col2:
            days = link2nd.days(select_user, k1)
            st.dataframe(days)

        # Most Common Words Section


        # Common Words Bar Chart Section
        st.subheader('🔠WordsCloud(Common_Words')
        counts = link2nd.wordscount(select_user, k1)
        fig, ax = plt.subplots()
        ax.imshow(counts)
        st.pyplot(fig)

        
        st.subheader('📊 Common Words Bar Chart')
        col1, col2 = st.columns(2)
        with col1:
            
            commom = link2nd.common_words(select_user, k1)
            fig, ax = plt.subplots()
            ax.bar(commom[0], commom[1], color='orange')
            plt.xticks(rotation=90)
            plt.figure(figsize=(2,2))
            st.pyplot(fig)
            
        with col2:
            commom = link2nd.common_words(select_user, k1)
            st.dataframe(commom)

        # Most Common Emojis Section
        st.subheader('😃 Most Common Emojis')
        emoji = link2nd.emojis(select_user, k1)
        st.dataframe(emoji)

        st.subheader('📅 Monthly Stats')
        col1, col2 = st.columns(2)
        with col1:
            month = link2nd.Month(select_user, k1)
            fig, ax = plt.subplots()
            ax.pie(month['count'], labels=month['NEW_Month'], autopct='%.2f%%', colors=sns.color_palette('pastel'))
            st.pyplot(fig)
        with col2:
            st.dataframe(month)

        # Month by Year Section
        st.subheader('📈 Month by Year')
        year = link2nd.year(select_user, k1)
        fig, ax = plt.subplots()
        ax.plot(year['new'], year['Message'], marker='o', color='purple')
        plt.xticks(rotation=90)
        plt.grid(True)
        st.pyplot(fig)


        st.subheader('📅 Timeline Analysis')
        daily=link2nd.daily(select_user,k1)

        st.dataframe(daily)

        st.subheader('🔥Timeline Heatmap')
        time_intervals = {
           '12AM': '12AM-1AM', '1AM': '1AM-2AM', '2AM': '2AM-3AM', '3AM': '3AM-4AM', '4AM': '4AM-5AM', 
            '5AM': '5AM-6AM', '6AM': '6AM-7AM', '7AM': '7AM-8AM', '8AM': '8AM-9AM', '9AM': '9AM-10AM', 
           '10AM': '10AM-11AM', '11AM': '11AM-12PM', '12PM': '12PM-1PM', '1PM': '1PM-2PM', 
           '2PM': '2PM-3PM', '3PM': '3PM-4PM', '4PM': '4PM-5PM', '5PM': '5PM-6PM', 
           '6PM': '6PM-7PM', '7PM': '7PM-8PM', '8PM': '8PM-9PM', '9PM': '9PM-10PM', 
           '10PM': '10PM-11PM', '11PM': '11PM-12AM'
            }
        k1['tem']=k1['Times'].map(time_intervals)
        if select_user=='Overall':
           

            
# Group by 'Days' and 'Time_Interval' and count the number of messages
            message_count = k1.groupby(['dayss', 'tem']).size().unstack(fill_value=0)

# Reorder the days of the week if necessary
            days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            message_count = message_count.reindex(days_order, axis=0)

# Convert the string counts to integers (if necessary)
            message_count = message_count.astype(int)

# Plotting the heatmap
            plt.figure(figsize=(22, 18)) 
            fig,ax=plt.subplots()
            sns.heatmap(message_count, cmap="YlGnBu", annot=True, fmt="d", linewidths=.5)
            st.pyplot(fig)
            plt.title("Message Count by Day and Time Interval")
            plt.ylabel("Day") 
            plt.xlabel("Time Interval")
            plt.xticks(rotation=45)
            plt.show()
        else:
            check=k1[k1['User']==select_user]
            message_count = check.groupby(['dayss', 'tem']).size().unstack(fill_value=0)

# Reorder the days of the week if necessary
            days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            message_count = message_count.reindex(days_order, axis=0)

# Convert the string counts to integers (if necessary)
            message_count = message_count.astype(int)

# Plotting the heatmap
            plt.figure(figsize=(12, 8)) 
            fig,ax=plt.subplots()
            sns.heatmap(message_count, cmap="YlGnBu", annot=True, fmt="d", linewidths=.5)
            st.pyplot(fig)
            plt.title("Message Count by Day and Time Interval")
            plt.ylabel("Day") 
            plt.xlabel("Time Interval")
            plt.xticks(rotation=45)
            plt.show()

        st.subheader('📋 Full Data')
        check=link2nd.search(select_user,k1)
        st.dataframe(check)

# Add a horizontal line for separation
st.sidebar.markdown("<hr style='border: 2px solid #4A90E2; margin: 10px 0;'>", unsafe_allow_html=True)

# Display the creator's information with custom styling
st.sidebar.markdown("""
    <div style='text-align: center;'>
        <h4 style='color: #4A90E2; margin-bottom: -6px;'>💻Developed By:</h4>
        <h2 style='color: #4A90E2; font-family: Arial, sans-serif; margin: -24px;'>👤Abdul Razzaq</h2>
        <p style='color: #4A90E2; font-size: 14px; margin-top: 6px;'>📊Data Scientist</p>
        <p style='color: #4A90E2; font-size: 14px; margin-top: -20px;'><a href='mailto:arazzaq7789@gmail.com' style='color: #4A90E2; text-decoration: none;'>📧arazzaq7789@gmail.com</a></p>
    </div>
    <hr style='border: 2px solid #4A90E2; margin: 10px 0;'>
""", unsafe_allow_html=True)
