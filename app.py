import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import time


import helper
import preprocessor
from helper import most_common_words, emojis_used

st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="centered")
st.title("💬 WhatsApp Chat Analyzer")
st.markdown(
    """
    <style>
    .stApp {
        background-color: #06402B;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.title('WhatsApp Chat Analyzer')
uploaded_file = st.sidebar.file_uploader("Choose a chat file(.txt)")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()

    placeholder = st.empty()
    with placeholder.container():
        st.info("🔄 Uploading file...")
    time.sleep(2)
    placeholder.success("✅ File uploaded successfully!")
    time.sleep(2)
    placeholder.empty()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    # st.dataframe(df)
    st.markdown(
        "<h1 style='color: grey;'>-----------------------------------------------</h1>",
        unsafe_allow_html=True
    )
    user_list = df['Users'].dropna().unique().tolist()
    user_list = [user for user in user_list if user != 'Group notifications']
    user_list.sort()
    user_list.insert(0,'OverAll')

    selected_user=st.sidebar.selectbox("Run Analysis on",user_list)

    if st.sidebar.button("Show Chat Analysis"):
        st.header("TOP STATISTICS")
        st.dataframe(df)
        st.markdown(
            "<h1 style='color: grey;'>-----------------------------------------------</h1>",
            unsafe_allow_html=True
        )
        num_messages,words,media,links = helper.fetch_stats(selected_user,df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Links Shared")
            st.title(links)
        with col4:
            st.header("Media Shared")
            st.title(media)


        if selected_user=="OverAll":

            st.title("Most Busy Log")
            busy_log,most_df = helper.most_busy_users(df)
            fig , ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(busy_log.index,busy_log.values,color="red")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(most_df)
        # st.title("----------------------------------------------")
        st.markdown(
            "<h1 style='color: grey;'>-----------------------------------------------</h1>",
            unsafe_allow_html=True
        )


        df_wc=helper.word_cloud(selected_user,df)
        st.title("Word Cloud")
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        st.markdown(
            "<h1 style='color: grey;'>-----------------------------------------------</h1>",
            unsafe_allow_html=True
        )
        most_common_df=most_common_words(selected_user,df)
        emojis_df=emojis_used(selected_user,df)
        col1, col2 = st.columns(2)

        with col1:
            st.header("Mostly Used Words")
            most_common_df.columns = ["Words","Frequency"]
            st.dataframe(most_common_df)
        with col2:
            st.header("Words Analysis")
            fig,ax = plt.subplots(figsize=(6,6))
            ax.bar(most_common_df["Words"],most_common_df["Frequency"])
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        st.markdown(
            "<h1 style='color: grey;'>-----------------------------------------------</h1>",
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:
            st.header("Mostly Used Emojis")
            emojis_df.columns=["Emojis","Frequency"]
            st.dataframe(emojis_df)

        with col2:
            st.header("Emojis Analysis")
            fig,ax = plt.subplots()
            ax.pie(emojis_df["Frequency"].head(10),labels=emojis_df["Emojis"].head(10),autopct="%0.2f")
            st.pyplot(fig)
        st.markdown(
            "<h1 style='color: grey;'>-----------------------------------------------</h1>",
            unsafe_allow_html=True
        )

        Monthly_timeline=helper.monthly_timeline(selected_user,df)
        Daily_timeline=helper.daily_timeline(selected_user,df)
        col1, col2 = st.columns(2)
        with col1:
            st.header("Monthly Timeline")
            fig,ax = plt.subplots()
            ax.plot(Monthly_timeline["Time"],Monthly_timeline["Messages"],color='orange')
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        with col2:
            st.header("Daily Timeline")
            fig,ax = plt.subplots(figsize=(6,5))
            ax.plot(Daily_timeline["Only_Date"],Daily_timeline["Messages"],color='orange')
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        st.markdown(
            "<h1 style='color: grey;'>-----------------------------------------------</h1>",
            unsafe_allow_html=True
        )

        Weekly_analysis=helper.week_activity_map(selected_user,df)
        Monthly_analysis=helper.month_activity_map(selected_user,df)
        col1, col2 = st.columns(2)
        with col1:
            st.header("Most Busy Day")
            fig,ax = plt.subplots()
            ax.bar(Weekly_analysis.index,Weekly_analysis.values,color="green")
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            fig,ax = plt.subplots()
            ax.bar(Monthly_analysis.index,Monthly_analysis.values,color='brown')
            st.pyplot(fig)
        st.markdown(
            "<h1 style='color: grey;'>-----------------------------------------------</h1>",
            unsafe_allow_html=True
        )




        st.title("Heat Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        if selected_user != "OverAll":

            if "generate_summary" not in st.session_state:
                st.session_state.generate_summary = False

            if st.button("Generate Personality Summary"):
                st.session_state.generate_summary = True

            if st.session_state.generate_summary:
                tags = helper.personality_one_liner(selected_user, df)
                st.success("🧠 Personality Insight:")
                for tag in tags:
                    st.markdown(f"- {tag}")



        st.text("-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-           -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-")
        st.markdown("<h1 style='text-align: center;'>Dhanyavaad</h1>", unsafe_allow_html=True)
        st.markdown(
            "<h1 style='color: grey;'>-----------------------------------------------</h1>",
            unsafe_allow_html=True
        )
    if st.sidebar.button("Show Sentiments Analysis"):
        st.header("🤯Sentiments Analysis")
        temp_2 = helper.sentiments_analysis(selected_user,df)
        st.dataframe(temp_2)
        st.markdown(
            "<h1 style='color: grey;'>-----------------------------------------------</h1>",
            unsafe_allow_html=True
        )
        Top_postive_sentiments,Top_Neutral_sentiments,Top_Negative_sentiments=helper.top_user_sentiments(temp_2)
        st.title('Top 5 Positive users')
        st.bar_chart(Top_postive_sentiments)
        st.markdown(
            "<h1 style='color: grey;'>-----------------------------------------------</h1>",
            unsafe_allow_html=True
        )
        st.title('Top 5 Neutral users')
        st.bar_chart(Top_Neutral_sentiments)
        st.markdown(
            "<h1 style='color: grey;'>-----------------------------------------------</h1>",
            unsafe_allow_html=True
        )
        st.title('Top 5 Negative users')
        st.bar_chart(Top_Negative_sentiments)
        st.markdown(
            "<h1 style='color: grey;'>-----------------------------------------------</h1>",
            unsafe_allow_html=True
        )

        st.text("-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-           -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-")
        st.markdown("<h1 style='text-align: center;'>Dhanyavaad</h1>", unsafe_allow_html=True)
        st.markdown(
            "<h1 style='color: grey;'>-----------------------------------------------</h1>",
            unsafe_allow_html=True
        )

else:
    st.markdown(
    """
    <div style="text-align: center;">
        <h3>👈 Upload your chat file to begin</h3>
        <p style="color: gray;">We support WhatsApp exported .txt files only</p>
    </div>
    """, unsafe_allow_html=True
)
