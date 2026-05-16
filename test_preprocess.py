import pytest
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_clean_review_text():
    from scripts.preprocess_reviews import clean_review_text
    
    # Test cleaning
    assert clean_review_text("Good app!") == "good app"
    assert clean_review_text("") == ""
    assert clean_review_text(None) == ""
    assert clean_review_text("http://link.com Great") == "great"

def test_dataframe_structure():
    # This will run after scraping
    pass
