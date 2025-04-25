# Marketing Brochure Generator Web App

This is a web-based version of the Marketing Brochure Generator. It provides a user-friendly interface for generating marketing brochures from company websites.

## Features

- Simple web interface for entering company information
- Background processing of brochure generation
- Real-time status updates
- Download generated brochures in Markdown format
- Responsive design for mobile and desktop

## Installation

1. Make sure you have the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and add your OpenAI API key:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and replace `your_api_key_here` with your actual OpenAI API key

## Usage

1. Start the web application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

3. Enter the company name and website URL

4. Wait for the brochure to be generated

5. Download the generated brochure

## Project Structure

- `app.py` - Main Flask application
- `brochure_generator.py` - Core brochure generation logic
- `templates/` - HTML templates for the web interface
  - `index.html` - Main form for entering company information
  - `loading.html` - Loading page while brochure is being generated
  - `download.html` - Download page for the generated brochure
- `brochures/` - Directory where generated brochures are stored

## Troubleshooting

If you encounter any issues:

1. Make sure your OpenAI API key is correctly set in the `.env` file
2. Check that you have a working internet connection
3. Verify that the website URL is accessible
4. Check the console output for any error messages

## Notes

- The brochure generation process may take several minutes depending on the website size
- The application uses background processing to prevent timeouts
- Generated brochures are stored in the `brochures/` directory 