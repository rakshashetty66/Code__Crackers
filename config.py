import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-codecracker'
    # Add database configuration for a production app

    # API endpoints
    LEETCODE_API = 'https://leetcode.com/graphql'
    CODECHEF_API = 'https://www.codechef.com/api/'
    HACKERRANK_API = 'https://www.hackerrank.com/rest/contests/tracking'  # Example, adjust as needed
    CODEFORCES_API = 'https://codeforces.com/api/' #Add API endpoint for codeforces

    # In a real app, you would store these in environment variables
    # or a secure configuration management system
