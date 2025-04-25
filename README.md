# Marketing Brochure Generator

A Flask application that generates professional marketing brochures using OpenAI's GPT-3.5 API and converts them to PDF format.

## Features

- Generate customized marketing brochures based on company information
- Support for different industries and target audiences
- Professional PDF output with clean formatting
- Customizable tone and style

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Send a POST request to `/generate` with the following JSON body:
   ```json
   {
     "company_name": "Your Company",
     "industry": "Technology",
     "target_audience": "Small businesses",
     "key_features": ["Feature 1", "Feature 2", "Feature 3"],
     "tone": "professional"
   }
   ```

3. The server will respond with a PDF file containing the generated brochure.

## API Endpoints

### POST /generate

Generates a marketing brochure and returns it as a PDF file.

**Request Body:**
- `company_name` (required): Name of the company
- `industry` (required): Industry sector
- `target_audience` (required): Target audience description
- `key_features` (required): List of key features to highlight
- `tone` (optional): Desired tone of the brochure (default: "professional")

**Response:**
- PDF file attachment

## Dependencies

- Flask: Web framework
- OpenAI: GPT-3.5 API integration
- WeasyPrint: PDF generation
- python-dotenv: Environment variable management
- markdown: Markdown to HTML conversion 