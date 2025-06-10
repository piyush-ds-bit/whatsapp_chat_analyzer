import re
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import nltk
from dateutil import parser
def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s?[APap][Mm])?\s-\s'

    messages=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)
    df =pd.DataFrame({'Users-messages':messages,'message_date':dates})

    df['clean_ts'] = (
        df['message_date']
        .astype(str)
        .str.extract(r'^(.*?)(?:\s+-\s+|$)', expand=False)   # keep only the timestamp
        .str.strip()
    )
    def parse_any(ts: str):
        for dayfirst in (True, False):        #  loop twice → fast & reliable
            try:
                return parser.parse(ts, dayfirst=dayfirst)
            except (ValueError, OverflowError):
                continue
        return pd.NaT
    df['Date'] = pd.to_datetime(df['clean_ts'].map(parse_any), errors='coerce')
    df.drop(columns=['message_date', 'clean_ts'], inplace=True)

    # df['message_date']=pd.to_datetime(df['message_date'],format='%m/%d/%y, %H:%M - ')
    # df.rename(columns={'message_date': "Date"},inplace=True)

    Users=[]
    Messages=[]
    for i in df['Users-messages']:
        entry=re.split(r"^(.*?):",i)
        if entry[1:]:
            Users.append(entry[1])
            Messages.append(entry[2])
        else:
            Users.append('Group notifications')
            Messages.append(entry[0])


    df['Users']=Users
    df['Messages']=Messages
    df['Messages']=df['Messages'].astype(str)
    df.drop(columns='Users-messages',inplace=True)

    df['Year']=df['Date'].dt.year
    df["Month_num"]=df["Date"].dt.month
    df['Month']=df['Date'].dt.month_name()
    df["Only_Date"]=df["Date"].dt.date
    df['Day']=df['Date'].dt.day
    df["Day_name"]=df["Date"].dt.day_name()
    df['Hour']=df['Date'].dt.hour
    df['Minute']=df['Date'].dt.minute
    df.drop(columns='Date',inplace=True)

    period = []
    for hour in df[['Day_name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['Period'] = period

    f = open("stop_hinglish.txt","r")
    stop_words = f.read()
    nltk.download('stopwords')
    port_stem = PorterStemmer()
    def stemming(messages):

        stemmed_messages=re.sub('[^a-zA-Z]',' ',messages)
        stemmed_messages=stemmed_messages.lower()
        stemmed_messages=stemmed_messages.split()
        stemmed_messages=[port_stem.stem(word) for word in stemmed_messages if not word in stopwords.words('english') and stop_words]
        stemmed_messages=' '.join(stemmed_messages)
        return stemmed_messages
    df['Stemmed_Messages']=df['Messages'].apply(stemming)
    return df
