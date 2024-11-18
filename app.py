# app.py
import streamlit as st
import requests
from bs4 import BeautifulSoup
import joblib
import numpy as np
from urllib.parse import urlparse
import re
import collections
from tld import get_tld

# Load the trained model, scaler, and label encoder
model = joblib.load('voting_classifier_model.pkl')
scaler = joblib.load('scaler.pkl')
lb = joblib.load('label_encoder.pkl')

# Function to fetch webpage content
def fetch_webpage_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        st.error("Error fetching webpage content.")
        st.error(e)
        return None

# Function to extract features from the URL
def extract_features(url):
    def url_length(url):
        return len(str(url))

    def hostname_len(url):
        return len(urlparse(url).netloc)

    def count_www(url):
        return url.count('www')

    def count_https(url):
        return url.count('https')

    def count_http(url):
        return url.count('http')

    def count_dot(url):
        return url.count('.')

    def count_per(url):
        return url.count('%')

    def count_ques(url):
        return url.count('?')

    def count_hyphen(url):
        return url.count('-')

    def count_equal(url):
        return url.count('=')

    def count_atrate(url):
        return url.count('@')

    def no_of_dir(url):
        urldir = urlparse(url).path
        return urldir.count('/')

    def no_of_embed(url):
        urldir = urlparse(url).path
        return urldir.count('//')

    def shortening_service(url):
        match = re.search(
            'bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
            'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
            'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
            'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
            'db\.tt|qr\.ae|adataset\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
            'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
            'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
            'tr\.im|link\.zip\.net', url)
        if match:
            return 1
        else:
            return 0

    def fd_length(url):
        urlpath = urlparse(url).path
        try:
            return len(urlpath.split('/')[1])
        except:
            return 0

    def tld_length(url):
        try:
            tld = get_tld(url, fail_silently=True)
            return len(tld) if tld else -1
        except:
            return -1

    def suspicious_words(url):
        match = re.search(
            'PayPal|login|signin|bank|account|update|free|lucky|service|bonus|ebayisapi|webscr', url)
        return 1 if match else 0

    def digit_count(url):
        return sum(c.isdigit() for c in url)

    def letter_count(url):
        return sum(c.isalpha() for c in url)

    def calculate_entropy(url):
        prob = [float(url.count(c)) / len(url) for c in dict(collections.Counter(url))]
        entropy = -sum([p * np.log2(p) for p in prob])
        return entropy

    def having_ip_address(url):
        match = re.search(
            '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
            '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
            '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)'  # IPv4 in hexadecimal
            '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
        return 1 if match else 0

    features = np.array([
        having_ip_address(url), count_www(url), count_atrate(url),
        no_of_dir(url), no_of_embed(url), shortening_service(url),
        count_https(url), count_http(url), count_per(url), count_ques(url),
        count_hyphen(url), count_equal(url), url_length(url), hostname_len(url),
        suspicious_words(url), fd_length(url), tld_length(url),
        digit_count(url), letter_count(url), calculate_entropy(url)
    ]).reshape(1, -1)

    return features

# Streamlit app
st.title("URL Classification")

url = st.text_input("Enter URL:")

if st.button("Classify URL"):
    features = extract_features(url)
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)
    label = lb.inverse_transform(prediction)
    st.write(f"The URL is classified as: {label[0]}")
