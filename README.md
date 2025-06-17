# 📊 WhatsApp Chat Analyzer

A user-friendly tool built with **Python** and **Streamlit** that allows you to upload exported WhatsApp chats (`.txt` files) and generate deep insights including **sentiment analysis**, **user activity**, **message trends**, **word clouds**, and more!

---

## 🎯 Motivation

As a passionate learner of data science and Python, I wanted to build a real-world, interactive project using **personal data** we all generate — WhatsApp chats!

This project was born out of curiosity to **visually explore conversation patterns**, **analyze user behavior**, and use **NLP** for sentiment insights — all with a click.

---

## 🚀 Features

- 📁 Upload exported WhatsApp chat text files directly
- 👤 User-wise message count, emoji usage, and word contribution
- 📈 Timeline analysis (daily/monthly activity trends)
- 📊 Most active days, months, and hours
- 🧠 Sentiment analysis using NLP
- 🌥️ WordCloud of most used words
- 🔥 Top keywords & common words
- 🎉 Group stats (for group chats) & overall engagement metrics

---

## 🛠️ Technologies Used

- **Python** (Core Language)
- **Pandas** – for data manipulation
- **NumPy** – for numerical operations
- **Matplotlib & Seaborn** – for visualizations
- **Streamlit** – for building interactive UI
- **NLTK / TextBlob** – for sentiment analysis
- **WordCloud** – to visualize common terms
- **Regular Expressions (regex)** – to parse and clean text

---

## 💡 How It Works

1. Export your WhatsApp chat (`.txt`) from phone
2. Launch the app locally via Streamlit
3. Upload the file and choose a user or “Overall”
4. Boom! 📊 The app generates stats, charts, and emotion insights

---

## 🧗‍♂️ Challenges I Faced

### 1. Parsing WhatsApp Chat Format
- WhatsApp exports have different structures based on language and device (iOS/Android)
- I handled this using regex, careful preprocessing, and exceptions for edge cases

### 2. Sentiment Analysis Accuracy
- WhatsApp messages are short, slangy, and informal
- I tested different models (TextBlob, VADER) and chose the one that gave the best consistent output for small texts

### 3. Performance with Large Files
- Chats with 50,000+ messages were slowing down processing
- I optimized by caching and vectorized Pandas operations

---

## Future Improvements

- Add support for multilingual chat parsing
- Enable download of reports as PDF
- Add predictive insights (e.g., peak days for replies)

---
## Contact

Piyush Kumar Singh  
Website: https://piyushkrsingh.lovable.app  
Email: piyushjuly04@gmail.com

---
## Star This Project

If you liked the project, consider starring it on GitHub and sharing it with friends who love data and WhatsApp stats!
