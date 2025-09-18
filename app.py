import os
import csv
import json
from flask import Flask, render_template, request
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Configure the Groq API client
try:
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables.")
    client = Groq(api_key=groq_api_key)
except Exception as e:
    print(f"Error initializing Groq client: {e}")
    client = None

# Define the output CSV file
CSV_FILE = 'call_analysis.csv'

def analyze_transcript(transcript: str) -> dict:
    """
    Analyzes the transcript using the Groq API to get summary and sentiment.
    """
    if not client:
        return {
            "summary": "Error: Groq client not initialized. Check API key.",
            "sentiment": "Unknown"
        }

    # This is the core prompt engineering part.
    # We ask the model to return a structured JSON object for reliable parsing.
    system_prompt = """
    You are an expert in customer service call analysis.
    Analyze the following customer call transcript.
    Your task is to:
    1.  Provide a concise summary of the conversation in 2-3 sentences.
    2.  Determine the customer's sentiment from one of the following options: Positive, Neutral, or Negative.

    Respond with ONLY a valid JSON object with two keys: "summary" and "sentiment".
    Do not include any other text, explanations, or markdown formatting before or after the JSON object.
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": f"Here is the transcript:\n\n---\n{transcript}\n---",
                },
            ],
            model="llama-3.1-8b-instant",
            temperature=0.2,
            # This ensures the output is a parsable JSON object
            response_format={"type": "json_object"},
        )
        
        response_content = chat_completion.choices[0].message.content
        # Convert the JSON string response into a Python dictionary
        analysis_result = json.loads(response_content)
        return analysis_result

    except Exception as e:
        print(f"An error occurred while contacting the Groq API: {e}")
        return {
            "summary": f"Error during analysis: {e}",
            "sentiment": "Error"
        }


def save_to_csv(transcript: str, summary: str, sentiment: str):
    """
    Saves the analysis result into a CSV file.
    Appends a new row for each analysis.
    """
    # Check if the file exists to determine if we need to write the header
    file_exists = os.path.isfile(CSV_FILE)
    
    try:
        # Open the file in append mode ('a')
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # If the file is new, write the header row first
            if not file_exists:
                writer.writerow(['Transcript', 'Summary', 'Sentiment'])
            
            # Write the data row
            writer.writerow([transcript, summary, sentiment])
        print(f"Successfully saved analysis to {CSV_FILE}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")


# Define the main route for the web application
@app.route('/', methods=['GET', 'POST'])
def index():
    # Default values to pass to the template
    analysis_data = {
        'summary': None,
        'sentiment': None,
        'transcript_text': None
    }

    if request.method == 'POST':
        # Get the transcript from the form submission
        transcript = request.form['transcript']
        
        if transcript:
            # Call the analysis function
            result = analyze_transcript(transcript)
            summary = result.get('summary', 'Could not generate summary.')
            sentiment = result.get('sentiment', 'Could not determine sentiment.')

            # Print results to the console as requested
            print("\n--- NEW ANALYSIS ---")
            print(f"Original Transcript:\n{transcript}\n")
            print(f"Summary:\n{summary}\n")
            print(f"Sentiment: {sentiment}")
            print("--------------------\n")

            # Save the results to the CSV file
            save_to_csv(transcript, summary, sentiment)
            
            # Update data to be displayed on the webpage
            analysis_data['summary'] = summary
            analysis_data['sentiment'] = sentiment
            analysis_data['transcript_text'] = transcript

    # Render the HTML page
    return render_template('index.html', **analysis_data)


# Run the Flask application
if __name__ == '__main__':
    # You can change the port if needed, e.g., app.run(debug=True, port=5001)
    app.run(debug=True)