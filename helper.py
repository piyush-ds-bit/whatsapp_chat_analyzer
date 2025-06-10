from wordcloud import WordCloud
import re
import pandas as pd
from collections import Counter
import emoji
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk


def fetch_stats(selected_user,df):
    if selected_user == 'OverAll':
        num_messages=df.shape[0]
        media=df['Messages'].astype(str).str.count("<Media omitted>\n").sum()
        words=[]
        links = []
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        for messages in df['Messages']:
            words.extend(messages.split())

            found_links = url_pattern.findall(messages)
            links.extend(found_links)
        return num_messages,len(words),media,len(links)
    else:
        new_df=df[df['Users'] == selected_user]
        num_messages=new_df.shape[0]
        media=new_df['Messages'].str.count("<Media omitted>\n").sum()
        words=[]
        links=[]
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        for messages in new_df['Messages']:
            words.extend(messages.split())
            found_links = url_pattern.findall(messages)
            links.extend(found_links)
        return num_messages,len(words),media,len(links)

def most_busy_users(df):
    busy_log=df['Users'].value_counts().head()
    most_df = round((df["Users"].value_counts()/df.shape[0])*100,2).reset_index()
    most_df.rename(columns={"count": "% count"}, inplace=True)
    return busy_log,most_df

def word_cloud(selected_user,df):
    if selected_user != 'OverAll':
        df=df[df["Users"]==selected_user]

    wc = WordCloud(height=500,width=500,min_font_size=10,background_color='white')
    df_wc=wc.generate(df["Messages"].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):

    f = open("stop_hinglish.txt","r")
    stop_words = f.read()

    if selected_user != 'OverAll':
        df=df[df["Users"]==selected_user]

    temp = df[df["Users"] != "Group notifications"]
    temp = temp[temp["Messages"] != " <Media omitted>\n"]
    word_list = []
    for messages in temp["Messages"]:
        for words in messages.lower().split():
            if words not in stop_words:
                word_list.append(words)
    most_common_df = pd.DataFrame(Counter(word_list).most_common(20))
    return most_common_df

def emojis_used(selected_user,df):
    if selected_user != 'OverAll':
        df=df[df["Users"]==selected_user]

    emojis = []
    for messages in df["Messages"]:
        emojis.extend([c for c in messages if emoji.is_emoji(c)])
    emojis_df=pd.DataFrame(Counter(emojis).most_common(20))
    return emojis_df

def monthly_timeline(selected_user,df):
    if selected_user != 'OverAll':
        df=df[df["Users"]==selected_user]

    Monthly_timeline=df.groupby(["Year","Month_num","Month"]).count()["Messages"].reset_index()
    time=[]
    for i in range(Monthly_timeline.shape[0]):
        time.append(Monthly_timeline["Month"][i]+'-'+str(Monthly_timeline["Year"][i]))
    Monthly_timeline["Time"]=time
    return Monthly_timeline

def daily_timeline(selected_user,df):
    if selected_user != 'OverAll':
        df=df[df["Users"]==selected_user]

    Daily_timeline=df.groupby(["Only_Date"]).count()["Messages"].reset_index()
    return Daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'OverAll':
        df=df[df["Users"]==selected_user]

    return df["Day_name"].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'OverAll':
        df=df[df["Users"]==selected_user]

    return df["Month"].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'OverAll':
        df = df[df['Users'] == selected_user]

    user_heatmap = df.pivot_table(index='Day_name', columns='Period', values='Messages', aggfunc='count').fillna(0)

    return user_heatmap

def sentiments_analysis(selected_user,df):
    if selected_user != 'OverAll':
        df = df[df['Users'] == selected_user]

    temp_2= df[df["Users"] != "Group notifications"]
    temp_2= temp_2[temp_2["Messages"] != " <Media omitted>\n"]
    nltk.download('vader_lexicon')
    sia = SentimentIntensityAnalyzer()
    temp_2['Sentiment_Score'] = temp_2['Stemmed_Messages'].apply(lambda x: sia.polarity_scores(x)['compound'])
    def get_sentiment_label(score):
        if score >= 0.05:
            return "Positive"
        elif score <= -0.05:
            return "Negative"
        else:
            return "Neutral"
    temp_2['Sentiments_Label']=temp_2['Sentiment_Score'].apply(get_sentiment_label)
    return temp_2[['Users','Messages','Sentiments_Label']]

def top_user_sentiments(temp_2):
    top_users_sentiment = temp_2.groupby(['Users', 'Sentiments_Label']).size().unstack().fillna(0)
    top_positive = top_users_sentiment.sort_values(by='Positive', ascending=False).head(5)
    top_neutral = top_users_sentiment.sort_values(by='Neutral', ascending=False).head(5)
    top_negative = top_users_sentiment.sort_values(by='Negative', ascending=False).head(5)
    return top_positive,top_neutral,top_negative

def personality_one_liner(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['Users'] == selected_user]

    total_msgs = df.shape[0]
    total_words = df['Messages'].astype(str).apply(lambda x: len(x.split())).sum()
    media_msgs = df['Messages'].astype(str).str.contains('<Media omitted>').sum()
    emoji_count = df['Messages'].astype(str).str.count(r'[^\w\s,]').sum()
    question_marks = df['Messages'].astype(str).str.count(r'\?').sum()
    caps_count = df['Messages'].astype(str).apply(lambda x: x.isupper()).sum()
    avg_msg_len = total_words / total_msgs if total_msgs > 0 else 0
    night_msgs = df[df['Hour'].between(0, 5)].shape[0]

    tags = []

    if total_msgs < 20:
        tags.append("Silent Observer 👀")
    if media_msgs / total_msgs > 0.3:
        tags.append("Media Spammer 📸")
    if emoji_count / total_msgs > 1:
        tags.append("The Emoji King 🤴")
    if night_msgs / total_msgs > 0.5:
        tags.append("Midnight Philosopher 🌙")
    if question_marks / total_msgs > 0.2:
        tags.append("The Question Machine ❓")
    if caps_count / total_msgs > 0.1:
        tags.append("Caps Lock Commander 🔊")
    if avg_msg_len > 25:
        tags.append("The Storyteller 📖")

    if not tags:
        tags.append("Just Vibin’ 😎")

    return tags
