"""
Generate a simple text report from analysis results
"""

import pandas as pd
import os

print("="*70)
print("TASK 2 RESULTS REPORT")
print("="*70)

# Check if results exist
if not os.path.exists('data/sentiment_theme_results.csv'):
    print("❌ Results not found. Run sentiment analysis first.")
    exit()

# Load data
df = pd.read_csv('data/sentiment_theme_results.csv')
print(f"\n✓ Loaded {len(df)} review results")

# ============================================
# SENTIMENT SUMMARY
# ============================================

print("\n" + "="*70)
print("1. SENTIMENT SUMMARY")
print("="*70)

print("\nOverall Sentiment Distribution:")
sentiment_counts = df['sentiment_label'].value_counts()
for label, count in sentiment_counts.items():
    pct = (count / len(df)) * 100
    print(f"   {label}: {count} ({pct:.1f}%)")

print("\nSentiment by Bank:")
for bank in df['bank'].unique():
    bank_df = df[df['bank'] == bank]
    pos = (bank_df['sentiment_label'] == 'positive').mean() * 100
    neg = (bank_df['sentiment_label'] == 'negative').mean() * 100
    neu = (bank_df['sentiment_label'] == 'neutral').mean() * 100
    print(f"\n   {bank}:")
    print(f"      Positive: {pos:.1f}%")
    print(f"      Negative: {neg:.1f}%")
    print(f"      Neutral: {neu:.1f}%")

# ============================================
# THEME SUMMARY
# ============================================

print("\n" + "="*70)
print("2. THEME SUMMARY")
print("="*70)

for bank in df['bank'].unique():
    bank_df = df[df['bank'] == bank]
    print(f"\n{bank} - Top Themes:")
    theme_counts = bank_df['identified_theme'].value_counts().head(5)
    for theme, count in theme_counts.items():
        pct = (count / len(bank_df)) * 100
        print(f"   {theme}: {count} ({pct:.1f}%)")

# ============================================
# SAMPLE REVIEWS BY SENTIMENT
# ============================================

print("\n" + "="*70)
print("3. SAMPLE REVIEWS BY SENTIMENT")
print("="*70)

for sentiment in ['positive', 'negative', 'neutral']:
    print(f"\n{sentiment.upper()} REVIEWS (3 examples):")
    samples = df[df['sentiment_label'] == sentiment]['review'].head(3)
    for i, review in enumerate(samples, 1):
        print(f"   {i}. {review[:100]}{'...' if len(review) > 100 else ''}")

# ============================================
# SENTIMENT VS RATING
# ============================================

print("\n" + "="*70)
print("4. SENTIMENT VS STAR RATING")
print("="*70)

print("\nRating | Positive | Negative | Neutral")
print("-"*45)
for rating in [1, 2, 3, 4, 5]:
    rating_df = df[df['rating'] == rating]
    if len(rating_df) > 0:
        pos = (rating_df['sentiment_label'] == 'positive').mean() * 100
        neg = (rating_df['sentiment_label'] == 'negative').mean() * 100
        neu = (rating_df['sentiment_label'] == 'neutral').mean() * 100
        print(f"   {rating}★  |   {pos:5.1f}%   |   {neg:5.1f}%   |   {neu:5.1f}%")

# ============================================
# SAVE REPORT TO FILE
# ============================================

print("\n" + "="*70)
print("5. SAVING REPORT")
print("="*70)

# Save to text file
with open('docs/TASK2_REPORT.txt', 'w', encoding='utf-8') as f:
    f.write("="*70 + "\n")
    f.write("TASK 2: SENTIMENT AND THEMATIC ANALYSIS REPORT\n")
    f.write("="*70 + "\n\n")
    
    f.write("OVERALL SENTIMENT:\n")
    for label, count in sentiment_counts.items():
        pct = (count / len(df)) * 100
        f.write(f"  {label}: {count} ({pct:.1f}%)\n")
    
    f.write("\nSENTIMENT BY BANK:\n")
    for bank in df['bank'].unique():
        bank_df = df[df['bank'] == bank]
        pos = (bank_df['sentiment_label'] == 'positive').mean() * 100
        neg = (bank_df['sentiment_label'] == 'negative').mean() * 100
        f.write(f"\n{bank}:\n")
        f.write(f"  Positive: {pos:.1f}%\n")
        f.write(f"  Negative: {neg:.1f}%\n")
    
    f.write("\nTOP THEMES:\n")
    for bank in df['bank'].unique():
        bank_df = df[df['bank'] == bank]
        f.write(f"\n{bank}:\n")
        theme_counts = bank_df['identified_theme'].value_counts().head(3)
        for theme, count in theme_counts.items():
            pct = (count / len(bank_df)) * 100
            f.write(f"  {theme}: {pct:.1f}%\n")

print("✓ Report saved to: docs/TASK2_REPORT.txt")

print("\n" + "="*70)
print("✅ REPORT GENERATION COMPLETE")
print("="*70)