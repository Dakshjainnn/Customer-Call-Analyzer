# Customer-Call-Analyzer
A simple Flask web application that uses the high-speed Groq API to analyze customer call transcripts for a concise summary and overall sentiment. The results are displayed in the UI and logged to a CSV file.

# About The Project
In customer service, quickly understanding the context of a call is crucial. This tool provides a simple interface to paste a call transcript and instantly receive:
  1.A 2-3 sentence summary of the conversation.
  2.The customer's sentiment (Positive, Neutral, or Negative).
All analyses are automatically saved to a call_analysis.csv file, creating a running log for record-keeping or further analysis. The application leverages the incredible inference speed of the Groq API to provide near-instant results.

# Features
1.Simple Web Interface: Easy-to-use UI for pasting transcripts and viewing results.
2.High-Speed Analysis: Leverages the Groq API and the Llama 3.1 8B Instant model for fast processing.
3.Automated Summarization: Condenses long transcripts into a short, easy-to-read summary.
4.Sentiment Extraction: Automatically determines if the customer's sentiment was Positive, Neutral, or Negative.
5.Persistent Logging: Saves the transcript, summary, and sentiment of every analysis into a local call_analysis.csv file.

# Built With
Flask: A lightweight Python web framework.
Groq API: For state-of-the-art LLM inference speed.
Python-dotenv: For managing environment variables.
HTML & CSS: For the simple frontend.

Check the Output File
A file named call_analysis.csv will be created in your project directory. Open it to see the log of all the transcripts you have analyzed.

Project Structure
/call-analyzer-app/
├── app.py              # Main Flask application logic
├── templates/
│   └── index.html      # Frontend UI template
├── .env                # Stores the API key (not committed to Git)
├── call_analysis.csv   # Output data file created on first run
├── requirements.txt    # Project dependencies
└── README.md           # This file
