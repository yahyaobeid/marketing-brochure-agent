import os
import threading
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from werkzeug.utils import secure_filename
from brochure_generator import generate_brochure
import time
import uuid
from dotenv import load_dotenv
import markdown

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'brochures'

# Ensure the brochures directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Store for tracking brochure generation status
brochure_status = {}

def generate_brochure_background(company_name, website_url, task_id):
    try:
        # Generate a unique filename
        timestamp = int(time.time())
        base_filename = secure_filename(company_name.lower().replace(' ', '_'))
        filename = f"{base_filename}_{timestamp}.md"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Update status to processing
        brochure_status[task_id] = {
            'status': 'processing',
            'filename': filename
        }
        
        # Generate the brochure content
        brochure_content = generate_brochure(company_name, website_url)
        
        # Save the content to a file
        with open(filepath, 'w') as f:
            f.write(brochure_content)
        
        # Convert markdown to HTML for display
        html_content = markdown.markdown(brochure_content)
        
        # Update status to complete
        brochure_status[task_id] = {
            'status': 'complete',
            'filename': filename,
            'content': html_content
        }
    except Exception as e:
        # Update status to error
        brochure_status[task_id] = {
            'status': 'error',
            'error': str(e)
        }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        company_name = request.form.get('company_name')
        website_url = request.form.get('website_url')
        
        if not company_name or not website_url:
            flash('Please provide both company name and website URL', 'error')
            return redirect(url_for('index'))
        
        # Generate a unique task ID
        task_id = str(uuid.uuid4())
        
        # Start brochure generation in a background thread
        thread = threading.Thread(
            target=generate_brochure_background,
            args=(company_name, website_url, task_id)
        )
        thread.daemon = True
        thread.start()
        
        # Store task ID in session
        session['task_id'] = task_id
        
        # Redirect to loading page
        return redirect(url_for('loading'))
    
    return render_template('index.html')

@app.route('/loading')
def loading():
    task_id = session.get('task_id')
    
    if not task_id or task_id not in brochure_status:
        flash('No brochure generation task found', 'error')
        return redirect(url_for('index'))
    
    status = brochure_status[task_id]
    
    if status['status'] == 'complete':
        # Show the brochure content
        return render_template('brochure.html', 
                             content=status['content'],
                             filename=status['filename'])
    elif status['status'] == 'error':
        # Show error message
        flash(f'Error generating brochure: {status["error"]}', 'error')
        return redirect(url_for('index'))
    
    # Show loading page
    return render_template('loading.html')

@app.route('/download/<filename>')
def download_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        flash('File not found', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 