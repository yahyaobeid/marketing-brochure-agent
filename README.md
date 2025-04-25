# Marketing Brochure Generator

A web application that automatically generates professional marketing brochures for companies by analyzing their websites. The application uses AI to create compelling, well-structured brochures that highlight a company's key products, services, and value propositions.

## Features

- **Web Interface**: Simple and intuitive web interface for inputting company information
- **Automated Analysis**: Scrapes and analyzes company websites to gather relevant information
- **AI-Powered Content**: Uses OpenAI's GPT models to generate professional marketing copy
- **Real-time Generation**: Background processing with status updates
- **Multiple Formats**: Supports markdown output with HTML preview
- **Downloadable Results**: Generated brochures can be downloaded for further use

## Prerequisites

- Python 3.7+
- OpenAI API key
- Internet connection for website scraping

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd marketing-brochure-agent
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Enter the company name and website URL in the form

4. Wait for the brochure generation process to complete

5. View and download the generated brochure

## Project Structure

- `app.py`: Main Flask application and web interface
- `brochure_generator.py`: Core brochure generation logic
- `templates/`: HTML templates for the web interface
- `brochures/`: Directory for storing generated brochures
- `requirements.txt`: Python package dependencies

## Dependencies

- Flask: Web framework
- OpenAI: AI-powered content generation
- BeautifulSoup4: Web scraping
- Python-dotenv: Environment variable management
- Markdown: Markdown processing
- Werkzeug: WSGI utilities

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 