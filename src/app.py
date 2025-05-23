from flask import Flask, render_template, request, jsonify
import sys
import os

# Ensure src directory is in path to import main (Assistant)
# This might need adjustment based on how you run Flask (e.g., `flask run` from root vs. `python src/app.py`)
# If running `python src/app.py` from the root, this is fine.
# If using `flask run`, Flask might handle paths differently, often expecting `src` to be a package.
# For simplicity with `python src/app.py` execution:
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__))) # Add current dir (src) to path
from main import Assistant # Expects main.py in the same directory (src)

app = Flask(__name__, template_folder='templates', static_folder='static')
assistant_instance = Assistant() # Instantiate the assistant once

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_command', methods=['POST'])
def process_command():
    if request.is_json:
        data = request.get_json()
        user_command = data.get('command')
    else: # Fallback for form data if not JSON
        user_command = request.form.get('command')

    if not user_command:
        return jsonify({'error': 'No command provided'}), 400

    # --- This is the part that will need Assistant to return data ---
    # For now, let's assume handle_command might still print,
    # and we'll capture that or get a direct return value in the next step.
    # Placeholder for actual response handling:
    
    # In the NEXT STEP, we will modify Assistant methods to return strings/JSON.
    # For now, let's try to capture print output if that's what handle_command does,
    # or get a direct return if it's already modified (unlikely per plan).
    
    # Option 1: If handle_command could return a string (ideal future state)
    # response_text = assistant_instance.handle_command(user_command)
    
    # Option 2: If handle_command still prints (current state of main.py)
    # We need to capture stdout. This is more complex in a web server context
    # and ideally should be avoided by refactoring main.py.
    # For a temporary measure if refactoring is strictly next step:
    import io
    from contextlib import redirect_stdout
    f = io.StringIO()
    with redirect_stdout(f):
        assistant_instance.handle_command(user_command) # This will print to f
    response_text = f.getvalue()
    
    if not response_text: # If it was empty or handle_command returned None
        response_text = "Assistant processed: " + user_command # Fallback

    return jsonify({'response': response_text.strip()})
    # --- End of placeholder ---

if __name__ == '__main__':
    app.run(debug=True, port=5000) # Running on port 5000
