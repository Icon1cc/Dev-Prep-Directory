"""
Problem 090: Interview Problem - Design a URL Shortener

Difficulty: Advanced
Topic: System Design Interview Question

=== PROBLEM DESCRIPTION ===

Design a URL shortening service like bit.ly or tinyurl.com.

Requirements:
- Generate short, unique codes for long URLs
- Redirect short URL to original URL
- Track click analytics (count, timestamps, referrers)
- Support custom short codes
- Handle expiration

Your Task:
-----------
1. Create `URL` entity:
   - `original_url`, `short_code`, `created_at`
   - `expires_at` (optional)
   - `click_count`

2. Create `ClickAnalytics`:
   - `timestamp`, `referrer`, `user_agent`, `ip_address`

3. Create `URLShortener` service:
   - `shorten(url, custom_code=None, expires_in=None)` -> short URL
   - `expand(short_code)` -> original URL
   - `get_analytics(short_code)` -> click stats
   - Generate unique short codes (base62 encoding)

4. Create `URLRepository`:
   - `save(url)`, `find_by_code(code)`, `find_by_original(url)`
   - In-memory storage for this exercise

5. Handle edge cases:
   - Duplicate URLs (return existing short code)
   - Invalid short codes
   - Expired URLs
   - Custom code conflicts

Expected Output:
----------------
URL Shortener Service

Shortening: https://www.example.com/very/long/path/to/page
Short URL: http://short.url/a1B2c3

Shortening same URL again...
Returns existing: http://short.url/a1B2c3

Custom short code: https://mysite.com -> http://short.url/mysite
  Success!

Expanding 'a1B2c3'...
Original URL: https://www.example.com/very/long/path/to/page
Click recorded!

Analytics for 'a1B2c3':
- Total clicks: 5
- Last 24 hours: 3
- Top referrers: ['google.com', 'twitter.com']

Expired URL 'old123':
Error: URL has expired

=== STARTER CODE ===
"""

from datetime import datetime, timedelta
from typing import Optional, List
import string
import random

# Write your solution below this line
# -----------------------------------



# Test your solution
# ------------------
# Create URL shortener and test various operations
