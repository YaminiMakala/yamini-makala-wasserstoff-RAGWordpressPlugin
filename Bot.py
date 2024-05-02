import requests
from bs4 import BeautifulSoup
from transformers import T5Tokenizer, T5ForConditionalGeneration
from rank_bm25 import BM25Okapi
from flask import Flask, request, jsonify

# Fetch data from a source (e.g., blog posts)
def fetch_data(api_endpoint):
    try:
        response = requests.get(api_endpoint)
        response.raise_for_status()
        data = response.json()
        posts = [post["content"]["rendered"] for post in data]
        return posts
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

# Preprocess data (e.g., extract text from HTML)
def preprocess_data(posts):
    cleaned_posts = []
    for post in posts:
        soup = BeautifulSoup(post, "html.parser")
        text = soup.get_text(separator='\n')
        cleaned_posts.append(text)
    return cleaned_posts

# Initialize tokenizer and model for T5
tokenizer = T5Tokenizer.from_pretrained('t5-base')
model_t5 = T5ForConditionalGeneration.from_pretrained('t5-base')

# Initialize Flask app
app = Flask(__name__)

# Endpoint for chatbot
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    query = data.get('query', '')

    # Error handling for invalid inputs
    if not query:
        return jsonify({'response': "Invalid input. Please provide a query."})

    # Fetch and preprocess data
    api_endpoint = "https://blog.ted.com/wp-json/wp/v2/posts"
    posts = fetch_data(api_endpoint)
    if not posts:
        return jsonify({'response': "Error fetching data. Please try again later."})
    cleaned_posts = preprocess_data(posts)

    # Perform retrieval using BM25
    bm25 = BM25Okapi([doc.split() for doc in cleaned_posts])
    tokenized_query = query.lower().split()
    top_n = bm25.get_top_n(tokenized_query, cleaned_posts, n=5)

    # Perform generation using T5
    inputs = tokenizer.encode("summarize: " + ' '.join(top_n) + " | " + query, return_tensors="pt", max_length=512, truncation=True)
    try:
        outputs = model_t5.generate(inputs, max_length=150, num_beams=2, early_stopping=True)
        response = tokenizer.decode(outputs[0])
    except Exception as e:
        print(f"Error generating response: {e}")
        return jsonify({'response': "Error generating response. Please try again later."})

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
