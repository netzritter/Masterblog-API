from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
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

    new_id = max([post["id"] for post in POSTS], default=0) + 1

    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"]
    }

    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    for index, post in enumerate(POSTS):
        if post["id"] == post_id:
            del POSTS[index]
            return jsonify({
                "message": f"Post with id {post_id} has been deleted successfully."
            }), 200

    return jsonify({"error": f"Post with id {post_id} not found."}), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Missing JSON body"}), 400

    for post in POSTS:
        if post["id"] == post_id:
            # Update only if fields are provided
            post["title"] = data.get("title", post["title"])
            post["content"] = data.get("content", post["content"])

            return jsonify(post), 200

    return jsonify({"error": f"Post with id {post_id} not found."}), 404

@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    matching_posts = []

    for post in POSTS:
        title_matches = title_query in post['title'].lower() if title_query else False
        content_matches = content_query in post['content'].lower() if content_query else False

        if title_matches or content_matches:
            matching_posts.append(post)

    return jsonify(matching_posts), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
