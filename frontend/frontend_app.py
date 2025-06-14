from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# In-memory list to store blog posts
posts = []

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/api/posts', methods=['POST'])
def new_blogpost():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    missing_fields = []
    if not data.get("title"):
        missing_fields.append("title")
    if not data.get("content"):
        missing_fields.append("content")

    if missing_fields:
        return jsonify({
            "error": f"Missing required field(s): {', '.join(missing_fields)}"
        }), 400

    # Generate new ID based on existing posts
    new_id = max([post["id"] for post in posts], default=0) + 1

    post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"]
    }

    posts.append(post)

    return jsonify(post), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
