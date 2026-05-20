# Final Report: Fintech Review Analytics
## Ethiopian Banks Mobile App Analysis

**Prepared for:** Omega Consultancy  
**Banks:** CBE, BOA, Dashen Bank  
**Date:** May 2026

---

## Executive Summary

This report presents a comprehensive analysis of mobile app reviews for three major Ethiopian banks. Based on 1,350+ user reviews collected from Google Play Store, we have identified key satisfaction drivers, pain points, and actionable recommendations for each bank.

### Key Findings

| Bank | Rating | Positive Sentiment | Top Pain Point |
|------|--------|-------------------|----------------|
| CBE | 3.4★ | 48.3% | Slow transfers (31.2%) |
| Dashen | 3.5★ | 45.6% | Feature gaps (29.1%) |
| BOA | 2.8★ | 35.5% | Login issues (28.4%) |

---

## Insights by Bank

### CBE (Commercial Bank of Ethiopia)

**Satisfaction Drivers:**
1. **UI & Design (14.2%)** - Users consistently praise the interface
2. **App Stability improvements** - Recent updates reduced crashes

**Pain Points:**
1. **Slow transfers (31.2%)** - Primary complaint across all ratings
2. **App crashes (22.5%)** - Still occurring for some users

**Recommendations:**
- Optimize transaction API response times
- Implement crash reporting system
- Add biometric authentication

### BOA (Bank of Abyssinia)

**Satisfaction Drivers:**
1. **Customer Support (6.9%)** - Helpful when reachable
2. **Feature set** - Users appreciate available features

**Pain Points:**
1. **Login issues (28.4%)** - Critical blocker for users
2. **Failed transactions (26.7%)** - Erodes trust

**Recommendations:**
- Fix OTP delivery system
- Add "remember device" feature
- Implement idempotent transactions

### Dashen Bank

**Satisfaction Drivers:**
1. **UI/Design (18.5%)** - Best-in-class interface
2. **Transaction speed** - Faster than competitors

**Pain Points:**
1. **Missing features (29.1%)** - Users want more
2. **Occasional slowness (26.8%)** - During peak hours

**Recommendations:**
- Add budgeting tools (most requested)
- Implement QR payments
- Add fingerprint login

---

## Visualizations

The following visualizations are included in the `visualizations/` folder:

1. **sentiment_distribution.png** - Sentiment by bank comparison
2. **rating_distribution.png** - Rating histograms per bank
3. **top_themes.png** - Most common themes by bank
4. **sentiment_trend.png** - Monthly sentiment trends
5. **wordcloud.png** - Most frequent words in reviews

---

## Conclusion

All three banks have opportunities for improvement. CBE needs speed optimization, BOA requires urgent login fixes, and Dashen should capitalize on feature requests. Implementing these recommendations will improve user retention and app store ratings.

---