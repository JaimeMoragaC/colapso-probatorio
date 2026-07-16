import urllib.request
import urllib.parse
import re

def get_scholar_url(query):
    url = "https://scholar.google.com/scholar?q=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        match = re.search(r'href="(/scholar_case\?case=[^"]+)"', html)
        if match:
            return "https://scholar.google.com" + match.group(1).replace("&amp;", "&")
        return None
    except Exception as e:
        return str(e)

print(get_scholar_url('"United States v. O\'Keefe" 537 F. Supp. 2d 14'))
print(get_scholar_url('"United States v. Vayner" 769 F.3d 125'))
