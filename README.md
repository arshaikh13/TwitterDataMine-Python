# 🐦 Twitter Data Scraper (CLI App)

A command-line application built with **Python**, **Tweepy**, and **Pandas** to scrape recent tweets by keyword or username using the Twitter API v2. Data is analyzed and saved in `.csv` format for further exploration.

---

## 🚀 Features

- 🔍 Search recent tweets by **keyword**
- 👤 Fetch recent tweets from a **specific user**
- 📊 View tweet **statistics** (total, average likes/retweets, most liked tweet)
- 📁 Save results to a **CSV file**
- 🛡️ Handles **rate limiting** gracefully (waits & retries)
- ✅ Secure credentials via `.env`

---

## 📦 Requirements

- Python 3.7+
- Twitter Developer Account & Bearer Token
- Environment variables configured via `.env`

---

## 🔧 Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/twitter-data-scraper.git
cd twitter-data-scraper
```

### 2. Install dependencies
```bash
pip install tweepy python-dotenv pandas
```

### 3. Create a .env file to store your credentials
```bash
BEARER_TOKEN=your_bearer_token <br>
API_KEY=your_api_key<br>
API_SECRET=your_api_secret<br>
ACCESS_TOKEN=your_access_token<br>
ACCESS_SECRET=your_access_secret
```

## Usage

### Run the app
```bash
python your_script_name.py
```

### Sample Output
=== Tweet Statistics ===<br>
Total Tweets: 50<br>
Average Likes: 24.6<br>
Average Retweets: 7.1<br>

Most Popular Tweet:<br>
"The moon landing anniversary is today 🚀🌕 #NASA"
