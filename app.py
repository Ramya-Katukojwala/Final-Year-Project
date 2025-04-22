from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory
from pyngrok import ngrok
import os
import json

# Flask app setup
app = Flask(__name__)

# Temporary folder to store uploaded files
UPLOAD_FOLDER = "/content/drive/MyDrive/Project Demo Try -2/uploaded images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Allowed file extensions for upload
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}

# Function to check if the file extension is allowed
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Sample JSON data (you can replace this with your own logic to generate JSON)
def generate_json_data():
    return {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3"
    }

# Page 1: Upload Image
@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        # Check if a file was uploaded
        if "file" not in request.files:
            return "No file uploaded!", 400

        file = request.files["file"]

        # Check if the file is valid
        if file.filename == "":
            return "No file selected!", 400

        if file and allowed_file(file.filename):
            # Save the uploaded file
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)

            # Redirect to the JSON editing page
            return redirect(url_for("edit_json", file_name=file.filename))

        return "Invalid file type!", 400

    # Render the upload form
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Upload Image</title>
        </head>
        <body>
            <h1>Upload an Image</h1>
            <form method="POST" enctype="multipart/form-data">
                <input type="file" name="file" accept=".jpg,.jpeg,.png,.gif">
                <button type="submit">Submit</button>
            </form>
        </body>
        </html>
    ''')

# Page 2: Edit JSON
@app.route("/edit/<file_name>", methods=["GET", "POST"])
def edit_json(file_name):
    if request.method == "POST":
        # Get the updated JSON data from the form
        updated_json = {}
        for key in request.form:
            updated_json[key] = request.form[key]

        # Redirect to the display page with the updated JSON
        return redirect(url_for("display_json", file_name=file_name, json_data=json.dumps(updated_json)))

    # Generate sample JSON data (replace with your logic)
    json_data = generate_json_data()

    # Render the JSON editing page
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Edit JSON</title>
        </head>
        <body>
            <h1>Edit JSON</h1>
            <img src="{{ url_for('uploaded_file', filename=file_name) }}" alt="Uploaded Image" style="max-width: 500px;">
            <form method="POST">
                {% for key, value in json_data.items() %}
                    <label for="{{ key }}">{{ key }}:</label>
                    <input type="text" id="{{ key }}" name="{{ key }}" value="{{ value }}"><br>
                {% endfor %}
                <button type="submit">Submit</button>
            </form>
        </body>
        </html>
    ''', file_name=file_name, json_data=json_data)

# Page 3: Display JSON
@app.route("/display/<file_name>", methods=["GET"])
def display_json(file_name):
    # Get the JSON data from the query parameters
    json_data = request.args.get("json_data")
    if json_data:
        json_data = json.loads(json_data)
    else:
        json_data = generate_json_data()  # Fallback to sample data

    # Render the display page
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Display JSON</title>
        </head>
        <body>
            <h1>Final JSON Data</h1>
            <table border="1">
                <tr>
                    <th>Key</th>
                    <th>Value</th>
                </tr>
                {% for key, value in json_data.items() %}
                    <tr>
                        <td>{{ key }}</td>
                        <td>{{ value }}</td>
                    </tr>
                {% endfor %}
            </table>
        </body>
        </html>
    ''', json_data=json_data)

# Serve uploaded files
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# Start the app
if __name__ == "__main__":
    # Connect Ngrok
    ngrok_url = ngrok.connect(5000)
    print(f"App running at: {ngrok_url}")

    # Run the Flask app
    app.run(port=5000)
