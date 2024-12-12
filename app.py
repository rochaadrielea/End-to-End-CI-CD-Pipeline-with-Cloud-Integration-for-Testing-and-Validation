from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('test_engineer.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS test_results (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        test_name TEXT,
                        result TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                     )''')
    conn.commit()
    conn.close()

# Home route
@app.route('/')
def home():
    return "<h1>Welcome to the Digital Solution Test Engineer Demo App</h1>"

# Route for adding test results via a web form
@app.route('/add-test')
def add_test_form():
    return '''
    <h1>Add Test Result</h1>
    <form action="/api/tests" method="post">
        <label for="test_name">Test Name:</label><br>
        <input type="text" id="test_name" name="test_name"><br>
        <label for="result">Result:</label><br>
        <select id="result" name="result">
            <option value="pass">Pass</option>
            <option value="fail">Fail</option>
        </select><br><br>
        <button type="submit">Add Test</button>
    </form>
    '''

# API route to add test results (JSON or form data)
@app.route('/api/tests', methods=['POST'])
def add_test_result():
    try:
        if request.is_json:
            data = request.json
            test_name = data['test_name']
            result = data['result']
        else:
            test_name = request.form['test_name']
            result = request.form['result']

        conn = sqlite3.connect('test_engineer.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO test_results (test_name, result) VALUES (?, ?)', (test_name, result))
        conn.commit()
        conn.close()

        return jsonify({"message": "Test result added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API route to get all test results (JSON format)
@app.route('/api/tests', methods=['GET'])
def get_test_results():
    try:
        conn = sqlite3.connect('test_engineer.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM test_results')
        rows = cursor.fetchall()
        conn.close()

        results = [
            {"id": row[0], "test_name": row[1], "result": row[2], "timestamp": row[3]} for row in rows
        ]
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to view test results in a table format
@app.route('/view-tests')
def view_tests():
    try:
        conn = sqlite3.connect('test_engineer.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM test_results')
        rows = cursor.fetchall()
        conn.close()

        html = '<h1>Test Results</h1><table border="1">'
        html += '<tr><th>ID</th><th>Test Name</th><th>Result</th><th>Timestamp</th></tr>'
        for row in rows:
            html += f'<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>'
        html += '</table>'
        return html
    except Exception as e:
        return f'<h1>Error</h1><p>{str(e)}</p>'
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)