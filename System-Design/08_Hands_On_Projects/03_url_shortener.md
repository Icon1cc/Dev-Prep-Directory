# Project 3: URL Shortener

Build a simple URL shortener service.

## Problem Description

```
┌────────────────────────────────────────────────────────────────┐
│                     URL SHORTENER                               │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Build a service that:                                         │
│  • Shortens long URLs to short codes                           │
│  • Redirects short codes to original URLs                      │
│                                                                 │
│  Example:                                                       │
│  Input:  https://www.example.com/very/long/path?query=param   │
│  Output: http://short.url/abc123                               │
│                                                                 │
│  When visiting http://short.url/abc123 → redirect to original │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

## Design Discussion

### Short Code Generation

```
APPROACH: Counter + Base62 Encoding

Why Base62?
• Characters: a-z, A-Z, 0-9 = 62 characters
• 6 characters = 62^6 = 56.8 billion unique URLs
• 7 characters = 62^7 = 3.5 trillion unique URLs

Conversion:
• Counter: 12345
• Base62: 12345 → "dnh"
• Reverse: "dnh" → 12345

┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  BASE62 ALPHABET:                                               │
│  0-9:   0123456789                     (indices 0-9)            │
│  a-z:   abcdefghijklmnopqrstuvwxyz     (indices 10-35)          │
│  A-Z:   ABCDEFGHIJKLMNOPQRSTUVWXYZ     (indices 36-61)          │
│                                                                  │
│  Example: 12345                                                  │
│  12345 / 62 = 199 remainder 7  → '7'                           │
│  199 / 62   = 3   remainder 11 → 'b'                           │
│  3 / 62     = 0   remainder 3  → '3'                           │
│  Result: "3b7"                                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Python Implementation

```python
import string
from typing import Optional
import threading

class URLShortener:
    """Simple URL shortener with in-memory storage."""

    # Base62 characters
    ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase
    BASE = len(ALPHABET)

    def __init__(self):
        self.url_to_code = {}  # long_url -> short_code
        self.code_to_url = {}  # short_code -> long_url
        self.counter = 1000    # Start from 1000 for longer codes
        self.lock = threading.Lock()

    def shorten(self, long_url: str) -> str:
        """Convert a long URL to a short code."""
        # Return existing code if URL was already shortened
        if long_url in self.url_to_code:
            return self.url_to_code[long_url]

        with self.lock:
            # Generate new code
            short_code = self._encode(self.counter)
            self.counter += 1

            # Store mappings
            self.url_to_code[long_url] = short_code
            self.code_to_url[short_code] = long_url

        return short_code

    def expand(self, short_code: str) -> Optional[str]:
        """Convert a short code back to the original URL."""
        return self.code_to_url.get(short_code)

    def _encode(self, num: int) -> str:
        """Encode a number to base62 string."""
        if num == 0:
            return self.ALPHABET[0]

        result = []
        while num > 0:
            result.append(self.ALPHABET[num % self.BASE])
            num //= self.BASE

        return ''.join(reversed(result))

    def _decode(self, code: str) -> int:
        """Decode a base62 string to number."""
        num = 0
        for char in code:
            num = num * self.BASE + self.ALPHABET.index(char)
        return num


# Simple HTTP server for testing
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

shortener = URLShortener()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == '/shorten':
            # Shorten URL: /shorten?url=https://example.com
            params = parse_qs(parsed.query)
            if 'url' in params:
                long_url = params['url'][0]
                short_code = shortener.shorten(long_url)

                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(f"Short URL: http://localhost:8000/{short_code}".encode())
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing 'url' parameter")

        elif len(parsed.path) > 1:
            # Redirect: /{short_code}
            short_code = parsed.path[1:]  # Remove leading /
            long_url = shortener.expand(short_code)

            if long_url:
                self.send_response(302)
                self.send_header('Location', long_url)
                self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Short URL not found")
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
                <h1>URL Shortener</h1>
                <p>Usage: /shorten?url=YOUR_LONG_URL</p>
            """)

    def log_message(self, format, *args):
        print(f"{args[0]}")  # Simplified logging


def run_server():
    server = HTTPServer(('localhost', 8000), RequestHandler)
    print("Server running at http://localhost:8000")
    print("Try: http://localhost:8000/shorten?url=https://www.google.com")
    server.serve_forever()


if __name__ == "__main__":
    # Unit tests
    print("Running tests...")

    s = URLShortener()

    # Test shortening
    url1 = "https://www.example.com/very/long/path"
    code1 = s.shorten(url1)
    print(f"Shortened: {url1} -> {code1}")

    # Test expansion
    expanded = s.expand(code1)
    assert expanded == url1, "Expansion failed!"
    print(f"Expanded: {code1} -> {expanded}")

    # Test duplicate URL
    code1_again = s.shorten(url1)
    assert code1 == code1_again, "Same URL should return same code!"
    print("Duplicate URL returns same code ✓")

    # Test different URL
    url2 = "https://www.different.com/path"
    code2 = s.shorten(url2)
    assert code1 != code2, "Different URLs should have different codes!"
    print(f"Different URL: {url2} -> {code2}")

    print("\nAll tests passed! Starting server...\n")
    run_server()
```

---

## How to Run

```bash
# Run the URL shortener server
python url_shortener.py

# In another terminal, test it:
# Shorten a URL
curl "http://localhost:8000/shorten?url=https://www.google.com"

# Visit the short URL in browser to redirect
```

---

## Java Implementation

```java
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicLong;

public class URLShortener {

    private static final String ALPHABET =
        "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    private static final int BASE = ALPHABET.length();

    private Map<String, String> urlToCode = new HashMap<>();
    private Map<String, String> codeToUrl = new HashMap<>();
    private AtomicLong counter = new AtomicLong(1000);

    public synchronized String shorten(String longUrl) {
        // Return existing code if already shortened
        if (urlToCode.containsKey(longUrl)) {
            return urlToCode.get(longUrl);
        }

        // Generate new code
        String shortCode = encode(counter.getAndIncrement());

        // Store mappings
        urlToCode.put(longUrl, shortCode);
        codeToUrl.put(shortCode, longUrl);

        return shortCode;
    }

    public String expand(String shortCode) {
        return codeToUrl.get(shortCode);
    }

    private String encode(long num) {
        StringBuilder sb = new StringBuilder();
        while (num > 0) {
            sb.append(ALPHABET.charAt((int)(num % BASE)));
            num /= BASE;
        }
        return sb.reverse().toString();
    }

    private long decode(String code) {
        long num = 0;
        for (char c : code.toCharArray()) {
            num = num * BASE + ALPHABET.indexOf(c);
        }
        return num;
    }

    public static void main(String[] args) {
        URLShortener shortener = new URLShortener();

        String url1 = "https://www.example.com/very/long/path";
        String code1 = shortener.shorten(url1);
        System.out.println("Shortened: " + url1 + " -> " + code1);

        String expanded = shortener.expand(code1);
        System.out.println("Expanded: " + code1 + " -> " + expanded);

        // Test duplicate
        String code1Again = shortener.shorten(url1);
        System.out.println("Same URL returns same code: " + code1.equals(code1Again));

        System.out.println("All tests passed!");
    }
}
```

---

## Extensions

### 1. Custom Short Codes
```python
def shorten_custom(self, long_url: str, custom_code: str) -> str:
    """Allow user to specify custom short code."""
    if custom_code in self.code_to_url:
        raise ValueError("Custom code already taken")

    self.url_to_code[long_url] = custom_code
    self.code_to_url[custom_code] = long_url
    return custom_code
```

### 2. Expiration
```python
def shorten_with_ttl(self, long_url: str, ttl_seconds: int) -> str:
    """Short URL expires after TTL."""
    code = self.shorten(long_url)
    expiry = time.time() + ttl_seconds
    self.expiry_times[code] = expiry
    return code

def expand(self, short_code: str) -> Optional[str]:
    if short_code in self.expiry_times:
        if time.time() > self.expiry_times[short_code]:
            return None  # Expired
    return self.code_to_url.get(short_code)
```

### 3. Analytics
```python
def expand_with_analytics(self, short_code: str) -> Optional[str]:
    """Track access count and timestamp."""
    url = self.code_to_url.get(short_code)
    if url:
        if short_code not in self.analytics:
            self.analytics[short_code] = {'count': 0, 'accesses': []}
        self.analytics[short_code]['count'] += 1
        self.analytics[short_code]['accesses'].append(time.time())
    return url
```

---

*Next: [Consistent Hashing](04_consistent_hashing.md) →*
