# CodeCracker - Competitive Programming Tracker
# Services package initialization

# Import utility functions and templates

def timestamp_to_date(timestamp):
    """Convert a UNIX timestamp to a formatted date string"""
    from datetime import datetime
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')

def gravatar_hash(email):
    """Generate MD5 hash for Gravatar"""
    import hashlib
    return hashlib.md5(email.lower().encode('utf-8')).hexdigest()

def format_date(date_str):
    """Format a date string to a more readable format"""
    from datetime import datetime
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%B %d, %Y')
    except:
        return date_str

# Register custom filters for Jinja templates
def register_filters(app):
    app.jinja_env.filters['timestamp_to_date'] = timestamp_to_date
    app.jinja_env.filters['gravatar_hash'] = gravatar_hash
    app.jinja_env.filters['format_date'] = format_date