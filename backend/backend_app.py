from flask import Flask, jsonify, request, flash, get_flashed_messages
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'supersecretkey'
CORS(app)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Retrieve all posts, with optional sorting by title or content.
    Query parameters:
        - sort: field to sort by (title or content)
        - direction: sorting direction (asc or desc)
    Returns:
        JSON response with the list of posts and any flashed messages.
    """
    sort_field = request.args.get('sort')
    direction = request.args.get('direction', 'asc')
    if sort_field not in ['title', 'content', None]:
        flash("Invalid sort field", "error")
        return jsonify({"error": "Invalid sort field", "flashes": get_flashed_messages(with_categories=True)}), 400
    if direction not in ['asc', 'desc']:
        flash("Invalid direction", "error")
        return jsonify({"error": "Invalid direction", "flashes": get_flashed_messages(with_categories=True)}), 400
    posts = POSTS.copy()
    if sort_field:
        posts.sort(key=lambda x: x[sort_field].lower(), reverse=direction == 'desc')
    return jsonify({"posts": posts, "flashes": get_flashed_messages(with_categories=True)}), 200


@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    Add a new post.
    Expects JSON body with:
        - title: post title
        - content: post content
    Returns:
        JSON response with the created post and any flashed messages.
    """
    data = request.get_json()
    if not data:
        flash("Missing JSON body", "error")
        return jsonify({"error": "Missing JSON body", "flashes": get_flashed_messages(with_categories=True)}), 400
    missing_fields = []
    if not data.get("title"):
        missing_fields.append("title")
    if not data.get("content"):
        missing_fields.append("content")
    if missing_fields:
        msg = f"Missing required field(s): {', '.join(missing_fields)}"
        flash(msg, "error")
        return jsonify({"error": msg, "flashes": get_flashed_messages(with_categories=True)}), 400
    new_id = max((post['id'] for post in POSTS), default=0) + 1
    new_post = {"id": new_id, "title": data["title"], "content": data["content"]}
    POSTS.append(new_post)
    flash(f"Post created with id {new_id}", "success")
    return jsonify({**new_post, "flashes": get_flashed_messages(with_categories=True)}), 201


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Update an existing post by its ID.
    Expects JSON body with optional fields:
        - title: updated title
        - content: updated content
    Returns:
        JSON response with the updated post or an error message.
    """
    data = request.get_json()
    if not data:
        flash("Missing JSON body", "error")
        return jsonify({"error": "Missing JSON body", "flashes": get_flashed_messages(with_categories=True)}), 400
    for post in POSTS:
        if post["id"] == post_id:
            post["title"] = data.get("title", post["title"])
            post["content"] = data.get("content", post["content"])
            flash(f"Post {post_id} updated", "success")
            return jsonify({**post, "flashes": get_flashed_messages(with_categories=True)}), 200
    flash(f"Post {post_id} not found", "error")
    return jsonify({"error": f"Post {post_id} not found", "flashes": get_flashed_messages(with_categories=True)}), 404


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Delete a post by its ID.
    Returns:
        JSON response indicating success or failure with any flashed messages.
    """
    for index, post in enumerate(POSTS):
        if post["id"] == post_id:
            del POSTS[index]
            flash(f"Post {post_id} deleted", "success")
            return jsonify({"message": f"Post {post_id} deleted", "flashes": get_flashed_messages(with_categories=True)}), 200
    flash(f"Post {post_id} not found", "error")
    return jsonify({"error": f"Post {post_id} not found", "flashes": get_flashed_messages(with_categories=True)}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Search posts by title or content using query parameters.
    Query parameters:
        - title: partial title to match
        - content: partial content to match
    Returns:
        JSON response with matching posts and any flashed messages.
    """
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()
    matches = [post for post in POSTS if title_query in post['title'].lower() or content_query in post['content'].lower()]
    flash(f"{len(matches)} posts found", "info")
    return jsonify({"matches": matches, "flashes": get_flashed_messages(with_categories=True)}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
