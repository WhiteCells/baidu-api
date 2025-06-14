from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/api', methods=['POST'])
def api():
    # 返回请求的 json
    return jsonify(request.json)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
