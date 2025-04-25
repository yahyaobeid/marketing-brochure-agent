import os
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import openai
from urllib.parse import urljoin, urlparse
import sys
import traceback
import markdown
import re

# Load environment variables
load_dotenv()

# Validate environment variables
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY not found in environment variables")
    print("Please create a .env file with your OpenAI API key")
    sys.exit(1)

# Initialize OpenAI client
openai.api_key = api_key
MODEL = os.getenv("MODEL", "gpt-4-turbo-preview")

# Headers for web requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

# System prompts for OpenAI
link_system_prompt = """You are a helpful assistant that analyzes website links and categorizes them.
For each link found, determine its type (e.g., 'About Us', 'Products', 'Services', 'Contact', etc.).
Return the results as a JSON object with a 'links' array containing objects with 'url' and 'type' fields."""

brochure_system_prompt = """You are a professional marketing copywriter who creates engaging brochures.
Analyze the company's website content and create a compelling brochure that:
1. Matches the company's tone and industry
2. Highlights key products/services
3. Includes relevant links and their purposes
4. Maintains a professional yet engaging style
5. Is structured in clear sections

The brochure should be concise but informative, typically 2-3 pages when rendered."""

class Website:
    """A utility class to represent a Website that we have scraped, with links and content analysis."""

    def __init__(self, url, base_url=None):
        self.url = url
        self.base_url = base_url or url
        try:
            print(f"Accessing website: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            self.body = response.content
            soup = BeautifulSoup(self.body, 'html.parser')
            self.title = soup.title.string if soup.title else "No title found"
            
            # Clean up the body content
            if soup.body:
                for irrelevant in soup.body(["script", "style", "img", "input"]):
                    irrelevant.decompose()
                self.text = soup.body.get_text(separator="\n", strip=True)
            else:
                self.text = ""
            
            # Process links
            links = []
            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    # Convert relative URLs to absolute
                    absolute_url = urljoin(self.base_url, href)
                    # Only include links from the same domain
                    if urlparse(absolute_url).netloc == urlparse(self.base_url).netloc:
                        links.append(absolute_url)
            self.links = list(set(links))  # Remove duplicates
            print(f"Found {len(self.links)} links on {url}")
        except requests.RequestException as e:
            print(f"Error accessing {url}: {str(e)}")
            self.body = b""
            self.title = "Error: Could not access website"
            self.text = ""
            self.links = []

    def get_contents(self):
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"

def get_links(url):
    """Analyze the website and categorize its links using OpenAI."""
    website = Website(url)
    try:
        print(f"Analyzing links for {url} using OpenAI API...")
        response = openai.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": link_system_prompt},
                {"role": "user", "content": f"Analyze these links from {url}:\n{json.dumps(website.links)}"}
            ],
            response_format={"type": "json_object"}
        )
        result = json.loads(response.choices[0].message.content)
        print(f"Successfully analyzed {len(result.get('links', []))} links")
        return result
    except Exception as e:
        print(f"Error analyzing links: {str(e)}")
        print(f"Error details: {traceback.format_exc()}")
        return {"links": []}

def get_all_details(url):
    """Gather all relevant information from the website and its linked pages."""
    result = "Landing page:\n"
    website = Website(url)
    result += website.get_contents()
    
    links = get_links(url)
    print("Found links:", links)
    
    for link in links.get("links", []):
        try:
            result += f"\n\n{link['type']}\n"
            result += Website(link["url"], base_url=url).get_contents()
        except Exception as e:
            print(f"Error processing {link.get('url', 'unknown URL')}: {str(e)}")
            continue
    
    return result

def get_brochure_user_prompt(company_name, url):
    """Generate a prompt for creating the company brochure."""
    user_prompt = f"You are looking at a company called: {company_name}\n"
    user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
    user_prompt += get_all_details(url)
    user_prompt = user_prompt[:5_000]  # Truncate if more than 5,000 characters
    return user_prompt

def generate_brochure(company_name, website_url, output_format='markdown'):
    """
    Generate brochure content using OpenAI's API.
    """
    try:
        # Get website content
        website = Website(website_url)
        content = website.get_contents()
        
        # Get categorized links
        links = get_links(website_url)
        
        # Create the prompt based on output format
        format_instructions = """
        Format the brochure in clean, professional """ + output_format + """ format.
        If PDF format is selected, ensure proper page breaks, headers, and footers.
        Remove any markdown code block markers or HTML tags.
        Use consistent styling throughout the document.
        """
        
        prompt = f"""
        Create a professional marketing brochure for {company_name} based on their website content.
        
        Website Content:
        {content}
        
        Key Pages:
        {json.dumps(links, indent=2)}
        
        The brochure should include:
        1. An engaging headline
        2. Company overview
        3. Key products/services
        4. Target audience benefits
        5. Call to action
        
        {format_instructions}
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional marketing copywriter and document formatter."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating brochure: {str(e)}")
        raise

def main():
    """Main function to run the brochure generator."""
    print("Welcome to the Marketing Brochure Generator!")
    company_name = input("Enter the company name: ")
    url = input("Enter the company website URL: ")
    output_format = input("Enter output format (markdown/pdf): ").lower()
    
    if output_format not in ['markdown', 'pdf']:
        output_format = 'markdown'
    
    print("\nGenerating brochure... This may take a few minutes.")
    try:
        brochure = generate_brochure(company_name, url, output_format)
        
        # Save the brochure to a file
        filename = f"{company_name.lower().replace(' ', '_')}_brochure.{output_format}"
        with open(filename, 'w') as f:
            f.write(brochure)
        
        print(f"\nBrochure has been generated and saved to {filename}")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        print(f"Error details: {traceback.format_exc()}")
        print("Please make sure you have:")
        print("1. A valid OpenAI API key in your .env file")
        print("2. A working internet connection")
        print("3. A valid website URL")

if __name__ == "__main__":
    main() 