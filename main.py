from flask import Flask, request, send_file, jsonify
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '✅ Server is running! POST /generate-report with JSON: {"summary": "your text"}'

# @app.route('/generate-report', methods=['POST'])
# def generate_report():
#     data = request.get_json()
#     if not data or 'summary' not in data:
#         return jsonify({'error': 'Missing "summary" in request body'}), 400

#     summary = data['summary']

#     # Load the image template from static folder
#     template_path = os.path.join('static', 'Lab_Summary.png')
#     try:
#         image = Image.open(template_path).convert('RGB')
#     except FileNotFoundError:
#         return jsonify({'error': 'Template image not found.'}), 404

#     draw = ImageDraw.Draw(image)

#     # Load font
#     try:
#         font = ImageFont.truetype("arial.ttf", size=20)
#     except IOError:
#         font = ImageFont.load_default()

#     # Position for text
#     start_x = 100
#     start_y = 700  # Below "NOTES:"
#     line_spacing = 30
#     max_chars_per_line = 90

#     # Wrap and draw text
#     lines = textwrap.wrap(summary, width=max_chars_per_line)
#     for i, line in enumerate(lines):
#         draw.text((start_x, start_y + i * line_spacing), line, font=font, fill="black")

#     # Save output to BytesIO
#     img_io = io.BytesIO()
#     image.save(img_io, 'PNG')
#     img_io.seek(0)

#     return send_file(img_io, mimetype='image/png')
@app.route('/generate-report', methods=['POST'])
def generate_report():
    data = request.get_json()
    if not data or 'summary' not in data:
        return jsonify({'error': 'Missing "summary" in request body'}), 400

    summary = data['summary']

    # Load and resize image
    template_path = os.path.join('static', 'Lab_Summary.png')
    try:
        image = Image.open(template_path).convert('RGB')
    except FileNotFoundError:
        return jsonify({'error': 'Template image not found.'}), 404

    # Resize image (optional, depending on your design)
    desired_width = 1240  # For better quality (e.g., 1240x1754 ~ A4 at 150 DPI)
    aspect_ratio = image.height / image.width
    resized_height = int(desired_width * aspect_ratio)
    image = image.resize((desired_width, resized_height))

    draw = ImageDraw.Draw(image)

    # Dynamically scale font size with image size
    font_size = 80  # Adjustable scaling factor
    try:
        font = ImageFont.truetype("arial.ttf", size=font_size)
    except IOError:
        font = ImageFont.load_default()

    # Define position and wrapping
    start_x = int(desired_width * 0.07)
    start_y = int(resized_height * 0.43)
    line_spacing = int(font_size * 1.6)
    max_chars_per_line = 80

    lines = textwrap.wrap(summary, width=max_chars_per_line)
    for i, line in enumerate(lines):
        draw.text((start_x, start_y + i * line_spacing), line, font=font, fill="black")

    # Return image
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
