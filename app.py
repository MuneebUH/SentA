from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import re
import pickle
import base64
from io import BytesIO
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import time
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

nltk.download('stopwords')

app = Flask(__name__)
CORS(app)

# Load models
model_xgb = pickle.load(open('model_xgb.pkl', 'rb'))
cv = pickle.load(open('countVectorizer.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))
STOPWORDS = set(stopwords.words('english'))
stemmer = PorterStemmer()

@app.route('/')
def index():
    return render_template("index.html")

def preprocess_reviews(df):
    corpus = []
    for review in df['review_body'].astype(str):
        review = re.sub('[^a-zA-Z]', ' ', review)
        review = review.lower().split()
        review = [stemmer.stem(word) for word in review if word not in STOPWORDS]
        corpus.append(' '.join(review))
    return corpus

def generate_base64_plot(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return f'<img src="data:image/png;base64,{encoded}" style="max-width:100%; margin-bottom:20px;" />'

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith('.xlsx'):
            df = pd.read_excel(file)
        else:
            return jsonify({'error': 'Unsupported file format'}), 400

        if 'star_rating' not in df.columns or 'review_body' not in df.columns:
            return jsonify({'error': "'star_rating' and 'review_body' columns required"}), 400

        time.sleep(1)
        corpus = preprocess_reviews(df)
        X = cv.transform(corpus).toarray()
        X_scaled = scaler.transform(X)
        y_preds = model_xgb.predict(X_scaled)
        df['predicted_sentiment'] = y_preds

        charts_html = ""

        # Rating Bar Chart
        fig1, ax1 = plt.subplots()
        df['star_rating'].value_counts().sort_index().plot.bar(ax=ax1, color='skyblue')
        ax1.set_title('Rating Count')
        charts_html += generate_base64_plot(fig1)

        # Rating Pie Chart
        fig2, ax2 = plt.subplots()
        df['star_rating'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, ax=ax2)
        ax2.set_ylabel('')
        ax2.set_title('Star Rating Distribution')
        charts_html += generate_base64_plot(fig2)

        # Word Cloud
        reviews = " ".join(df['review_body'].astype(str))
        wc = WordCloud(background_color='white', max_words=50).generate(reviews)
        fig3, ax3 = plt.subplots()
        ax3.imshow(wc, interpolation='bilinear')
        ax3.axis('off')
        ax3.set_title('Word Cloud for Reviews')
        charts_html += generate_base64_plot(fig3)

        # Sentiment Bar Chart
        fig4, ax4 = plt.subplots()
        df['predicted_sentiment'].value_counts().plot.bar(ax=ax4, color='orange')
        ax4.set_title('Sentiment Count')
        charts_html += generate_base64_plot(fig4)

        # Sentiment Pie Chart
        fig5, ax5 = plt.subplots()
        df['predicted_sentiment'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, ax=ax5)
        ax5.set_ylabel('')
        ax5.set_title('Sentiment Distribution')
        charts_html += generate_base64_plot(fig5)

        preview_html = df[['review_body', 'star_rating', 'predicted_sentiment']].head(20).to_html(classes='data', index=False)

        return jsonify({
            'preview': preview_html,
            'chartsHtml': charts_html
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
