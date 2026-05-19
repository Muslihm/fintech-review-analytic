"""
Task 2: Sentiment and Thematic Analysis
Using TextBlob for sentiment classification
"""

import pandas as pd
import re
from collections import defaultdict, Counter
from textblob import TextBlob
import warnings
import os

warnings.filterwarnings('ignore')

print("= - sentiment_textblob.py:15"*70)
print("TASK 2: SENTIMENT AND THEMATIC ANALYSIS - sentiment_textblob.py:16")
print("Using TextBlob for Sentiment Analysis - sentiment_textblob.py:17")
print("= - sentiment_textblob.py:18"*70)

# ============================================
# LOAD DATA
# ============================================

print("\n📂 Loading data... - sentiment_textblob.py:24")

# Check if cleaned data exists
if not os.path.exists('data/cleaned_reviews.csv'):
    print("❌ Cleaned data not found. Please run preprocessing first. - sentiment_textblob.py:28")
    print("Run: python scripts/preprocess_reviews.py - sentiment_textblob.py:29")
    exit()

df = pd.read_csv('data/cleaned_reviews.csv')
print(f"✓ Loaded {len(df)} reviews - sentiment_textblob.py:33")

# ============================================
# SENTIMENT ANALYSIS WITH TEXTBLOB
# ============================================

print("\n📊 Performing sentiment analysis with TextBlob... - sentiment_textblob.py:39")

def get_textblob_sentiment(text):
    """
    Get sentiment using TextBlob
    Returns: (sentiment_label, confidence_score)
    """
    if not isinstance(text, str) or len(text.strip()) < 3:
        return 'neutral', 0.5
    
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # Range: -1 (negative) to +1 (positive)
        
        # Convert polarity to label
        if polarity >= 0.1:
            return 'positive', polarity
        elif polarity <= -0.1:
            return 'negative', -polarity
        else:
            return 'neutral', 0.5
    except:
        return 'neutral', 0.5

# Apply sentiment analysis
sentiments = []
scores = []

for idx, row in df.iterrows():
    text = row.get('cleaned_review', row.get('review', ''))
    sentiment, score = get_textblob_sentiment(str(text))
    sentiments.append(sentiment)
    scores.append(score)
    
    if (idx + 1) % 200 == 0:
        print(f"Processed {idx + 1}/{len(df)} reviews - sentiment_textblob.py:74")

df['sentiment_label'] = sentiments
df['sentiment_score'] = scores

# Calculate coverage
coverage = (df['sentiment_label'].notna().sum() / len(df)) * 100
print(f"\n✓ Sentiment coverage: {coverage:.1f}% (target: 90%+) - sentiment_textblob.py:81")

# ============================================
# THEME EXTRACTION
# ============================================

print("\n🎯 Extracting themes... - sentiment_textblob.py:87")

# Define themes and keywords
themes = {
    'Transaction Performance': {
        'keywords': ['slow', 'fast', 'transfer', 'transaction', 'processing', 
                   'timeout', 'speed', 'pending', 'taking long', 'lag',
                   'payment', 'send', 'receive', 'instant']
    },
    'Account Access': {
        'keywords': ['login', 'log in', 'sign in', 'otp', 'password', 'access',
                   'verification', 'authentication', "can't log", 'unable',
                   'forgot', 'reset', 'locked']
    },
    'App Stability': {
        'keywords': ['crash', 'freeze', 'stuck', 'close', 'error', 'bug',
                   'glitch', 'not working', 'fails', 'unresponsive']
    },
    'UI and Design': {
        'keywords': ['ui', 'interface', 'design', 'layout', 'navigation',
                   'user friendly', 'intuitive', 'looks', 'appearance', 'clean']
    },
    'Feature Requests': {
        'keywords': ['fingerprint', 'biometric', 'dark mode', 'qr', 'budget',
                   'notification', 'alert', 'add', 'would be great', 'wish',
                   'suggest', 'improve', 'enhance']
    },
    'Customer Support': {
        'keywords': ['support', 'help', 'customer service', 'agent', 'call',
                   'chat', 'response', 'resolved', 'complaint', 'assistance']
    }
}

def assign_theme(text):
    """Assign a theme based on keyword matching"""
    if not isinstance(text, str):
        return 'Other'
    
    text_lower = text.lower()
    theme_scores = {}
    
    for theme, theme_info in themes.items():
        score = 0
        for keyword in theme_info['keywords']:
            if keyword in text_lower:
                score += 1
        if score > 0:
            theme_scores[theme] = score
    
    if theme_scores:
        return max(theme_scores, key=theme_scores.get)
    return 'Other'

df['identified_theme'] = df['cleaned_review'].apply(assign_theme)

# ============================================
# PRINT RESULTS
# ============================================

print("\n - sentiment_textblob.py:146" + "="*70)
print("SENTIMENT ANALYSIS RESULTS - sentiment_textblob.py:147")
print("= - sentiment_textblob.py:148"*70)

# Overall sentiment
print("\n📈 Overall Sentiment Distribution: - sentiment_textblob.py:151")
sentiment_dist = df['sentiment_label'].value_counts()
total = len(df)
for label, count in sentiment_dist.items():
    pct = (count / total) * 100
    bar = "█" * int(pct / 2)
    print(f"{label.upper():8}: {count:4} ({pct:5.1f}%) {bar} - sentiment_textblob.py:157")

# Sentiment by bank
print("\n🏦 Sentiment by Bank: - sentiment_textblob.py:160")
for bank in df['bank'].unique():
    bank_df = df[df['bank'] == bank]
    pos_pct = (bank_df['sentiment_label'] == 'positive').mean() * 100
    neg_pct = (bank_df['sentiment_label'] == 'negative').mean() * 100
    neu_pct = (bank_df['sentiment_label'] == 'neutral').mean() * 100
    avg_score = bank_df['sentiment_score'].mean()
    
    print(f"\n   {bank}: - sentiment_textblob.py:168")
    print(f"Positive: {pos_pct:.1f}%  |  Negative: {neg_pct:.1f}%  |  Neutral: {neu_pct:.1f}% - sentiment_textblob.py:169")
    print(f"Average sentiment score: {avg_score:.3f} - sentiment_textblob.py:170")

# Sentiment by rating
print("\n⭐ Sentiment vs Star Rating: - sentiment_textblob.py:173")
for rating in sorted(df['rating'].unique()):
    rating_df = df[df['rating'] == rating]
    avg_score = rating_df['sentiment_score'].mean()
    pos_pct = (rating_df['sentiment_label'] == 'positive').mean() * 100
    print(f"{rating}★ ({len(rating_df)} reviews): Avg score = {avg_score:.3f} | Positive = {pos_pct:.1f}% - sentiment_textblob.py:178")

# ============================================
# THEMATIC RESULTS
# ============================================

print("\n - sentiment_textblob.py:184" + "="*70)
print("THEMATIC ANALYSIS RESULTS - sentiment_textblob.py:185")
print("= - sentiment_textblob.py:186"*70)

# Theme distribution by bank
for bank in df['bank'].unique():
    bank_df = df[df['bank'] == bank]
    print(f"\n🏦 {bank}: - sentiment_textblob.py:191")
    
    theme_counts = bank_df['identified_theme'].value_counts()
    theme_pcts = (theme_counts / len(bank_df)) * 100
    
    for theme, count in theme_counts.head(5).items():
        pct = theme_pcts[theme]
        bar = "█" * int(pct / 2)
        print(f"{theme:25}: {count:3} reviews ({pct:5.1f}%) {bar} - sentiment_textblob.py:199")
    
    # Show example for top theme
    top_theme = theme_counts.index[0] if len(theme_counts) > 0 else None
    if top_theme:
        example = bank_df[bank_df['identified_theme'] == top_theme]['review'].iloc[0]
        print(f"\n   📝 Example ({top_theme}): - sentiment_textblob.py:205")
        print(f"\"{example[:100]}{'...' if len(example) > 100 else ''}\" - sentiment_textblob.py:206")

# ============================================
# KEYWORD EXTRACTION (Without sklearn)
# ============================================

print("\n - sentiment_textblob.py:212" + "="*70)
print("TOP KEYWORDS BY BANK - sentiment_textblob.py:213")
print("= - sentiment_textblob.py:214"*70)

# Common stopwords to exclude
stopwords = {'the', 'and', 'for', 'that', 'this', 'with', 'from', 'have', 'are', 
             'was', 'were', 'app', 'bank', 'please', 'very', 'really', 'just', 
             'but', 'not', 'can', 'get', 'has', 'you', 'your', 'it', 'they', 
             'all', 'been', 'will', 'would', 'could', 'should', 'about', 'because'}

for bank in df['bank'].unique():
    # Combine all reviews for this bank
    bank_reviews = df[df['bank'] == bank]['cleaned_review'].str.lower().tolist()
    all_text = ' '.join(bank_reviews)
    
    # Find words (3+ characters)
    words = re.findall(r'\b[a-z]{3,}\b', all_text)
    
    # Count word frequencies (excluding stopwords)
    word_counts = {}
    for word in words:
        if word not in stopwords and len(word) > 3:
            word_counts[word] = word_counts.get(word, 0) + 1
    
    # Get top 10 words
    top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    print(f"\n   {bank}: - sentiment_textblob.py:239")
    for word, count in top_words:
        print(f"• {word}: {count} times - sentiment_textblob.py:241")

# ============================================
# SENTIMENT VS RATING MATRIX
# ============================================

print("\n - sentiment_textblob.py:247" + "="*70)
print("SENTIMENT VS RATING MATRIX - sentiment_textblob.py:248")
print("= - sentiment_textblob.py:249"*70)
print("\nHow TextBlob sentiment aligns with star ratings: - sentiment_textblob.py:250")
print("Rows = Star Ratings | Columns = Predicted Sentiment - sentiment_textblob.py:251")
print(""*50)

# Create cross tabulation manually
ratings = [1, 2, 3, 4, 5]
sentiment_labels = ['positive', 'neutral', 'negative']

print(f"\n{'Rating':<8} - sentiment_textblob.py:258", end='')
for label in sentiment_labels:
    print(f"{label.upper():>12} - sentiment_textblob.py:260", end='')
print()
print(""*50)

for rating in ratings:
    rating_df = df[df['rating'] == rating]
    total = len(rating_df)
    if total > 0:
        print(f"{rating}★{' ':<6} - sentiment_textblob.py:268", end='')
        for label in sentiment_labels:
            count = (rating_df['sentiment_label'] == label).sum()
            pct = (count / total) * 100
            print(f"{pct:>11.1f}% - sentiment_textblob.py:272", end='')
        print()

# ============================================
# SAVE RESULTS
# ============================================

print("\n - sentiment_textblob.py:279" + "="*70)
print("SAVING RESULTS - sentiment_textblob.py:280")
print("= - sentiment_textblob.py:281"*70)

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Save full results
output_columns = ['review', 'cleaned_review', 'rating', 'date', 'bank', 
                 'sentiment_label', 'sentiment_score', 'identified_theme']
output_df = df[output_columns].copy()
output_df.to_csv('data/sentiment_theme_results.csv', index=False)
print("✓ Saved: data/sentiment_theme_results.csv - sentiment_textblob.py:291")

# Save aggregated by bank and rating
agg_data = []
for bank in df['bank'].unique():
    bank_df = df[df['bank'] == bank]
    for rating in [1, 2, 3, 4, 5]:
        rating_df = bank_df[bank_df['rating'] == rating]
        if len(rating_df) > 0:
            agg_data.append({
                'bank': bank,
                'rating': rating,
                'count': len(rating_df),
                'avg_sentiment_score': rating_df['sentiment_score'].mean(),
                'positive_pct': (rating_df['sentiment_label'] == 'positive').mean() * 100,
                'negative_pct': (rating_df['sentiment_label'] == 'negative').mean() * 100,
                'neutral_pct': (rating_df['sentiment_label'] == 'neutral').mean() * 100
            })

agg_df = pd.DataFrame(agg_data)
agg_df.to_csv('data/sentiment_by_bank_rating.csv', index=False)
print("✓ Saved: data/sentiment_by_bank_rating.csv - sentiment_textblob.py:312")

# Save theme summary
theme_summary = []
for bank in df['bank'].unique():
    bank_df = df[df['bank'] == bank]
    for theme in themes.keys():
        count = (bank_df['identified_theme'] == theme).sum()
        if count > 0:
            theme_summary.append({
                'bank': bank,
                'theme': theme,
                'count': count,
                'percentage': round((count / len(bank_df)) * 100, 1)
            })

theme_df = pd.DataFrame(theme_summary)
theme_df.to_csv('data/theme_summary.csv', index=False)
print("✓ Saved: data/theme_summary.csv - sentiment_textblob.py:330")

# ============================================
# SUMMARY STATISTICS FOR REPORT
# ============================================

print("\n - sentiment_textblob.py:336" + "="*70)
print("SUMMARY STATISTICS FOR YOUR REPORT - sentiment_textblob.py:337")
print("= - sentiment_textblob.py:338"*70)

# Calculate key metrics for the report
print("\n📊 Key Metrics: - sentiment_textblob.py:341")
print(f"Total reviews analyzed: {len(df)} - sentiment_textblob.py:342")
print(f"Sentiment coverage: {coverage:.1f}% - sentiment_textblob.py:343")
print(f"Overall positive rate: {(df['sentiment_label'] == 'positive').mean() * 100:.1f}% - sentiment_textblob.py:344")
print(f"Overall negative rate: {(df['sentiment_label'] == 'negative').mean() * 100:.1f}% - sentiment_textblob.py:345")

print("\n🏦 Bank Rankings: - sentiment_textblob.py:347")
bank_positive = df.groupby('bank').apply(lambda x: (x['sentiment_label'] == 'positive').mean() * 100)
for bank, pct in bank_positive.sort_values(ascending=False).items():
    print(f"{bank}: {pct:.1f}% positive - sentiment_textblob.py:350")

print("\n🎯 Most Common Themes: - sentiment_textblob.py:352")
theme_counts = df['identified_theme'].value_counts()
for theme, count in theme_counts.head(3).items():
    pct = (count / len(df)) * 100
    print(f"{theme}: {pct:.1f}% of all reviews - sentiment_textblob.py:356")

print("\n - sentiment_textblob.py:358" + "="*70)
print("✅ TASK 2 COMPLETED SUCCESSFULLY! - sentiment_textblob.py:359")
print("= - sentiment_textblob.py:360"*70)

print("\n📁 Output files generated: - sentiment_textblob.py:362")
print("1. data/sentiment_theme_results.csv  Full analysis results - sentiment_textblob.py:363")
print("2. data/sentiment_by_bank_rating.csv  Aggregated by bank and rating - sentiment_textblob.py:364")
print("3. data/theme_summary.csv  Theme distribution by bank - sentiment_textblob.py:365")

print("\n🔧 Tool used: TextBlob - sentiment_textblob.py:367")
print("Polarity range: 1 (very negative) to +1 (very positive) - sentiment_textblob.py:368")
print("Classification: positive (>0.1), neutral (0.1 to 0.1), negative (<0.1) - sentiment_textblob.py:369")