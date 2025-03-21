import requests
import json
from config import Config


def fetch_codeforces_data(handle):
    """Fetch user data from Codeforces API"""
    if not handle:
        return {
            'status': 'error',
            'message': 'No Codeforces handle provided',
            'data': None
        }

    try:
        # Fetch user info
        user_url = f"{Config.CODEFORCES_API}user.info?handles={handle}"
        user_response = requests.get(user_url)
        user_data = user_response.json()

        if user_data.get('status') != 'OK':
            return {
                'status': 'error',
                'message': user_data.get('comment', 'Failed to fetch Codeforces data'),
                'data': None
            }

        # Fetch user submissions
        submissions_url = f"{Config.CODEFORCES_API}user.status?handle={handle}&from=1&count=100"
        submissions_response = requests.get(submissions_url)
        submissions_data = submissions_response.json()

        # Process the data
        user_info = user_data['result'][0]
        submissions = submissions_data.get('result', [])

        # Calculate statistics
        solved_problems = set()
        for submission in submissions:
            if submission.get('verdict') == 'OK':
                problem_key = f"{submission['problem']['contestId']}-{submission['problem']['index']}"
                solved_problems.add(problem_key)

        processed_data = {
            'handle': handle,
            'rating': user_info.get('rating', 0),
            'max_rating': user_info.get('maxRating', 0),
            'rank': user_info.get('rank', 'unrated'),
            'solved_count': len(solved_problems),
            'submissions': len(submissions),
            'submissions_data': [
                {
                    'time': sub['creationTimeSeconds'],
                    'problem_name': sub['problem']['name'],
                    'verdict': sub.get('verdict', 'UNKNOWN'),
                    'tags': sub['problem'].get('tags', []),
                    'rating': sub['problem'].get('rating', 0)
                }
                for sub in submissions[:20]  # Limit to recent 20
            ]
        }

        return {
            'status': 'success',
            'message': 'Data fetched successfully',
            'data': processed_data
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error fetching Codeforces data: {str(e)}',
            'data': None
        }


def fetch_leetcode_data(handle):
    """Fetch user data from LeetCode API"""
    if not handle:
        return {
            'status': 'error',
            'message': 'No LeetCode handle provided',
            'data': None
        }

    try:
        # LeetCode GraphQL query
        query = """
        query userProfile($username: String!) {
          matchedUser(username: $username) {
            username
            submitStats {
              acSubmissionNum {
                difficulty
                count
                submissions
              }
              totalSubmissionNum {
                difficulty
                count
                submissions
              }
            }
            profile {
              ranking
              reputation
              starRating
            }
          }
          recentSubmissionList(username: $username, limit: 20) {
            id
            title
            titleSlug
            timestamp
            statusDisplay
            lang
          }
        }
        """

        variables = {'username': handle}

        headers = {
            'Content-Type': 'application/json',
            'Referer': 'https://leetcode.com/'
        }

        response = requests.post(
            Config.LEETCODE_API,
            json={'query': query, 'variables': variables},
            headers=headers
        )

        data = response.json()

        if 'errors' in data or not data.get('data', {}).get('matchedUser'):
            return {
                'status': 'error',
                'message': 'Failed to fetch LeetCode data or user not found',
                'data': None
            }

        # Process the data
        user_data = data['data']['matchedUser']
        submissions = data['data'].get('recentSubmissionList', [])

        submit_stats = user_data.get('submitStats', {}).get('acSubmissionNum', [])
        total_solved = sum(item.get('count', 0) for item in submit_stats)

        processed_data = {
            'handle': handle,
            'ranking': user_data.get('profile', {}).get('ranking', 0),
            'reputation': user_data.get('profile', {}).get('reputation', 0),
            'star_rating': user_data.get('profile', {}).get('starRating', 0),
            'solved_count': total_solved,
            'solved_by_difficulty': {
                item.get('difficulty'): item.get('count', 0)
                for item in submit_stats if 'difficulty' in item
            },
            'recent_submissions': [
                {
                    'id': sub.get('id'),
                    'title': sub.get('title'),
                    'status': sub.get('statusDisplay'),
                    'timestamp': sub.get('timestamp'),
                    'language': sub.get('lang')
                }
                for sub in submissions
            ]
        }

        return {
            'status': 'success',
            'message': 'Data fetched successfully',
            'data': processed_data
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error fetching LeetCode data: {str(e)}',
            'data': None
        }


def fetch_codechef_data(handle):
    """Fetch user data from CodeChef API"""
    if not handle:
        return {
            'status': 'error',
            'message': 'No CodeChef handle provided',
            'data': None
        }

    try:
        # Note: CodeChef doesn't have an open API, so this is a mock implementation
        # In a real app, you would need to use web scraping or find alternate ways to get data

        # Mock data for demonstration
        mock_data = {
            'handle': handle,
            'rating': 1842,
            'highest_rating': 1923,
            'global_rank': 3245,
            'country_rank': 243,
            'solved_count': 127,
            'fully_solved': {
                'school': 15,
                'easy': 42,
                'medium': 53,
                'hard': 17
            },
            'contests': [
                {
                    'name': 'March Long Challenge 2025',
                    'rating': 1842,
                    'rank': 243,
                    'solved': 7
                },
                {
                    'name': 'February Cook-Off 2025',
                    'rating': 1835,
                    'rank': 356,
                    'solved': 4
                },
                {
                    'name': 'January Lunchtime 2025',
                    'rating': 1857,
                    'rank': 198,
                    'solved': 5
                }
            ]
        }

        return {
            'status': 'success',
            'message': 'Data fetched successfully (mock data)',
            'data': mock_data
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error fetching CodeChef data: {str(e)}',
            'data': None
        }