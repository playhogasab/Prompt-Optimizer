from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__, template_folder='../templates')

# API Key Setup (Vercel Environment Variable se ayega)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Model Configuration
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "max_output_tokens": 1024,
}
model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        user_input = data.get('prompt')
        mode = data.get('mode')  # 'optimizer' or 'story'

        if not user_input:
            return jsonify({'error': 'Please enter some text'}), 400

        # Prompt Logic
        if mode == 'optimizer':
            system_instruction = f"Act as an expert Prompt Engineer. Optimize the following prompt to be highly detailed, professional, and suitable for LLMs or Image Generators: '{user_input}'"
        else:
            system_instruction = f"Write a creative and engaging short story based on this idea: '{user_input}'. Keep it under 300 words."

        response = model.generate_content(system_instruction)
        return jsonify({'result': response.text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Vercel ke liye zaroori hai
if __name__ == '__main__':
    app.run(debug=True)
