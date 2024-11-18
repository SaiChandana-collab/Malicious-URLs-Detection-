**Malicious URLs Detection**


### Purpose and Motivation:
- **Malicious URLs** pose significant cybersecurity threats, with phishing attacks leading to financial losses and compromised personal data.
- The project seeks to enhance phishing detection accuracy by combining **feature-based** and **content-based** analysis techniques.

### Techniques and Features Analyzed:
1. **Feature-Based Analysis:**
   - URL characteristics like length, hostname length, counts of "www," "https," "http," dots, question marks, hyphens, IP addresses, and entropy are evaluated.
   - These features aim to highlight unusual patterns often seen in phishing URLs.

2. **Content-Based Analysis:**
   - Direct inspection of webpage content, including HTML, textual content, and metadata.
   - Methods like **TF-IDF vectorization** and models like **Multinomial Naive Bayes** are used to classify content legitimacy.

3. **Hybrid Model:**
   - Integrates feature-based and content-based methods for a two-stage classification.
   - Feature-based analysis filters legitimate URLs; suspicious ones undergo further content-based evaluation.

### Machine Learning Models:
- Models such as **Random Forest, AdaBoost, Gradient Boosting**, and **KNeighborsClassifier** were implemented.
- **Random Forest** and **Ensemble Learning** proved highly effective, achieving **accuracy rates up to 99.69%**.

### Key Outcomes:
- The hybrid approach strengthens cybersecurity defenses, minimizing false positives while maximizing detection accuracy.

