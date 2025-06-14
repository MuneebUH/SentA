# 🧠 Customer Review Sentiment Analyzer (Flask App)

A web application built using **Flask** that allows users to upload product reviews in `.csv` or `.xlsx` format, processes and classifies the sentiment of the reviews, and generates visual insights such as bar charts, pie charts, and a word cloud.

---

## App Interface
![Interface](interface/SentA.jpg)

## 🚀 Features

- Upload customer reviews (`CSV`/`Excel`)
- Preprocesses and vectorizes text data
- Predicts sentiment using a pre-trained **XGBoost** model
- Visualizes:
  - Star rating distribution (bar & pie charts)
  - Word cloud from review text
  - Predicted sentiment distribution (bar & pie charts)
- Preview top 20 classified reviews in a clean table

---

## 📦 Requirements

Install the required dependencies using:

```bash
Flask
Flask-CORS
pandas
matplotlib
nltk
wordcloud
scikit-learn
xgboost
openpyxl
```
## 📁 File Structure

```
└── 📁project
    └── 📁static
        └── script.js
        └── style.css
    └── 📁templates
        └── index.html
    └── app.py
    └── countVectorizer.pkl
    └── model_xgb.pkl
    └── README.md
    └── scaler.pkl
```
## How It Works?

- Upload File: 
        Users upload a .csv or .xlsx file containing two required columns: star_rating and review_body.

- Preprocessing:

        Clean text with regex

        Remove stopwords

        Apply stemming using PorterStemmer

- Vectorization & Scaling:

        Vectorize using CountVectorizer

        Scale features using StandardScaler

- Prediction:

        Predict sentiment labels using a trained XGBoost model

- Visualization:

        Generate bar and pie charts for ratings and sentiment

        Create a word cloud from the review corpus

## Example Input Format
| star\_rating | review\_body                       |
| ------------ | ---------------------------------- |
| 5            | This product is excellent!         |
| 1            | Terrible quality, broke in a week. |

## 🌐 Run the App Locally
```bash
python app.py
```

## 📊 Output Preview
- Top 20 reviews with predicted sentiment

- Rating & sentiment bar charts

- Rating & sentiment pie charts

- Word cloud for most frequent review words
