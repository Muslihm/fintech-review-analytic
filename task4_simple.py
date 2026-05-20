"""
Task 4: Insights and Recommendations - Simplified Version
Meets minimum requirements: 1 driver & 1 pain point per bank, 2 plots
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# Create output directory
os.makedirs('visualizations', exist_ok=True)

print("= - task4_simple.py:13"*60)
print("TASK 4: INSIGHTS AND RECOMMENDATIONS - task4_simple.py:14")
print("= - task4_simple.py:15"*60)

# Load data
df = pd.read_csv('data/sentiment_theme_results.csv')
print(f"\n✓ Loaded {len(df)} reviews - task4_simple.py:19")

# ============================================
# PLOT 1: Sentiment Bar Chart
# ============================================

print("\n📊 Creating Plot 1: Sentiment by Bank... - task4_simple.py:25")

# Calculate sentiment percentages
sentiment_data = []
for bank in df['bank'].unique():
    bank_df = df[df['bank'] == bank]
    sentiment_data.append({
        'Bank': bank,
        'Positive': (bank_df['sentiment_label'] == 'positive').mean() * 100,
        'Negative': (bank_df['sentiment_label'] == 'negative').mean() * 100,
        'Neutral': (bank_df['sentiment_label'] == 'neutral').mean() * 100
    })

sentiment_df = pd.DataFrame(sentiment_data)

# Create bar chart
fig, ax = plt.subplots(figsize=(10, 6))
x = range(len(sentiment_df))
width = 0.25

bars1 = ax.bar([i - width for i in x], sentiment_df['Positive'], width, label='Positive', color='#2ecc71')
bars2 = ax.bar(x, sentiment_df['Neutral'], width, label='Neutral', color='#95a5a6')
bars3 = ax.bar([i + width for i in x], sentiment_df['Negative'], width, label='Negative', color='#e74c3c')

ax.set_xlabel('Bank', fontsize=12)
ax.set_ylabel('Percentage (%)', fontsize=12)
ax.set_title('Sentiment Distribution by Bank', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(sentiment_df['Bank'])
ax.legend()

# Add value labels
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}%', xy=(bar.get_x() + bar.get_width()/2, height),
                   xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('visualizations/sentiment_chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Saved: visualizations/sentiment_chart.png - task4_simple.py:66")

# ============================================
# PLOT 2: Keyword/Theme Frequency Chart
# ============================================

print("\n📊 Creating Plot 2: Top Themes by Bank... - task4_simple.py:72")

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for idx, bank in enumerate(df['bank'].unique()):
    bank_df = df[df['bank'] == bank]
    theme_counts = bank_df['identified_theme'].value_counts().head(5)
    
    colors = ['#3498db', '#2980b9', '#1abc9c', '#16a085', '#2ecc71']
    bars = axes[idx].barh(range(len(theme_counts)), theme_counts.values, color=colors[:len(theme_counts)])
    axes[idx].set_yticks(range(len(theme_counts)))
    axes[idx].set_yticklabels(theme_counts.index, fontsize=10)
    axes[idx].set_xlabel('Number of Reviews', fontsize=10)
    axes[idx].set_title(f'{bank} - Top Themes', fontsize=12, fontweight='bold')
    
    # Add value labels
    for bar, count in zip(bars, theme_counts.values):
        axes[idx].text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2, 
                      str(count), va='center', fontsize=9)

plt.suptitle('Most Common Themes by Bank', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/themes_chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Saved: visualizations/themes_chart.png - task4_simple.py:96")

# ============================================
# EXTRACT DRIVERS AND PAIN POINTS
# ============================================

print("\n - task4_simple.py:102" + "="*60)
print("DRIVERS & PAIN POINTS BY BANK - task4_simple.py:103")
print("= - task4_simple.py:104"*60)

results = []

for bank in df['bank'].unique():
    bank_df = df[df['bank'] == bank]
    
    # Find top driver (from positive reviews)
    positive_reviews = bank_df[bank_df['sentiment_label'] == 'positive']
    if len(positive_reviews) > 0:
        top_driver = positive_reviews['identified_theme'].value_counts().index[0]
        driver_pct = (positive_reviews['identified_theme'] == top_driver).mean() * 100
    else:
        top_driver = "N/A"
        driver_pct = 0
    
    # Find top pain point (from negative reviews)
    negative_reviews = bank_df[bank_df['sentiment_label'] == 'negative']
    if len(negative_reviews) > 0:
        top_pain = negative_reviews['identified_theme'].value_counts().index[0]
        pain_pct = (negative_reviews['identified_theme'] == top_pain).mean() * 100
    else:
        top_pain = "N/A"
        pain_pct = 0
    
    results.append({
        'Bank': bank,
        'Avg_Rating': round(bank_df['rating'].mean(), 2),
        'Top_Driver': top_driver,
        'Driver_Percentage': round(driver_pct, 1),
        'Top_Pain_Point': top_pain,
        'Pain_Point_Percentage': round(pain_pct, 1)
    })

# Print results
for r in results:
    print(f"\n{'='*40} - task4_simple.py:140")
    print(f"🏦 {r['Bank']} - task4_simple.py:141")
    print(f"{'='*40} - task4_simple.py:142")
    print(f"⭐ Average Rating: {r['Avg_Rating']} / 5.0 - task4_simple.py:143")
    print(f"\n✅ TOP DRIVER: {r['Top_Driver']} - task4_simple.py:144")
    print(f"→ {r['Driver_Percentage']}% of positive reviews mention this - task4_simple.py:145")
    print(f"\n❌ TOP PAIN POINT: {r['Top_Pain_Point']} - task4_simple.py:146")
    print(f"→ {r['Pain_Point_Percentage']}% of negative reviews mention this - task4_simple.py:147")

# Save to CSV
results_df = pd.DataFrame(results)
results_df.to_csv('data/drivers_pain_points.csv', index=False)
print("\n✓ Saved: data/drivers_pain_points.csv - task4_simple.py:152")

print("\n - task4_simple.py:154" + "="*60)
print("✅ TASK 4 COMPLETE! - task4_simple.py:155")
print("= - task4_simple.py:156"*60)
print("\n📁 Output files: - task4_simple.py:157")
print("• visualizations/sentiment_chart.png - task4_simple.py:158")
print("• visualizations/themes_chart.png - task4_simple.py:159")
print("• data/drivers_pain_points.csv - task4_simple.py:160")