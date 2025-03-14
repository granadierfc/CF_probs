from flask import Flask, request, jsonify, send_from_directory
import requests
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="static")
CORS(app)  # Enable cross-origin requests

def get_solved_problems_by_tags(handle, tags, min_rating=0):
    # Fetch user submissions
    submissions_url = f'https://codeforces.com/api/user.status?handle={handle}'
    submissions_response = requests.get(submissions_url)
    submissions = submissions_response.json().get('result', [])

    # Fetch problemset to get problem tags and ratings
    problemset_url = 'https://codeforces.com/api/problemset.problems'
    problemset_response = requests.get(problemset_url)
    problemset = problemset_response.json().get('result', {})
    problems = problemset.get('problems', [])

    # Create a dictionary to map problem indices to their tags and ratings
    problem_data = {}
    for problem in problems:
        problem_id = (problem.get('contestId'), problem.get('index'))
        problem_data[problem_id] = {
            'tags': problem.get('tags', []),
            'rating': problem.get('rating', 0)
        }

    # Filter solved problems by tags and rating
    solved_problems = []
    for submission in submissions:
        if submission.get('verdict') == 'OK':
            problem = submission.get('problem', {})
            problem_id = (problem.get('contestId'), problem.get('index'))
            problem_info = problem_data.get(problem_id, {})
            problem_tags = problem_info.get('tags', [])
            problem_rating = problem_info.get('rating', 0)
            if any(tag in problem_tags for tag in tags) and problem_rating >= min_rating:
                problem_name = problem.get('name')
                contest_id = problem.get('contestId')
                index = problem.get('index')
                problem_url = f'https://codeforces.com/contest/{contest_id}/problem/{index}'
                solved_problems.append({'name': problem_name, 'url': problem_url})

    return solved_problems

@app.route('/api/solved_problems', methods=['GET'])
def solved_problems():
    handle = request.args.get('handle')
    tags = request.args.get('tags', '').split(',')
    min_rating = int(request.args.get('min_rating', 0))

    if not handle:
        return jsonify({'error': 'Codeforces handle is required'}), 400

    problems = get_solved_problems_by_tags(handle, tags, min_rating)
    return jsonify({'problems': problems})

# Serve frontend files
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)