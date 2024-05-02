Overview
This project implements a simple chatbot using Flask, BM25Okapi, and T5 models from the Hugging Face Transformers library. The chatbot fetches data from the TED blog endpoint, processes it, and generates responses based on user queries.

Code Quality
The code is well-structured and organized, with clear separation of concerns.
Error handling is implemented for invalid inputs and exceptions during data fetching and response generation.
Endpoint handling is effective, with the Flask endpoint (/chat) handling POST requests efficiently.
Installation
To run the chatbot, follow these steps:

Clone the repository to your local machine.
Install the required dependencies by running pip install -r requirements.txt.
Run the Flask app by executing python chatbot.py in your terminal.
Usage
Once the Flask app is running, you can interact with the chatbot endpoint by sending POST requests to http://127.0.0.1:5000/chat. The chatbot expects JSON data with a "query" field containing the user's query.

Testing
To test the chatbot, you can use the provided testing code (test_chatbot.py). This code contains sample queries and expected responses, allowing you to verify the chatbot's functionality.

Additional Notes
The chatbot fetches data from the TED blog endpoint (https://blog.ted.com/wp-json/wp/v2/posts).
The response generation uses BM25Okapi for retrieval and T5 models for generation.
Ensure that you have a stable internet connection to fetch data from the endpoint and access the Hugging Face models.
