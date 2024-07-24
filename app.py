from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

def calculate_average_weekly_weight_loss(file_path):
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df['days_diff'] = (df['Date'] - df['Date'].shift()).dt.days
    df['weight_diff'] = df['Weight'].shift() - df['Weight']
    df['weekly_weight_loss'] = df['weight_diff'] / df['days_diff'] * 7
    average_weekly_weight_loss = df['weekly_weight_loss'].mean()
    return average_weekly_weight_loss

@app.route('/calculate', methods=['POST'])
def calculate():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    if file:
        file_path = "/tmp/" + file.filename
        file.save(file_path)
        avg_loss = calculate_average_weekly_weight_loss(file_path)
        return jsonify({"average_weekly_weight_loss": avg_loss})

if __name__ == '__main__':
    app.run(debug=True)
