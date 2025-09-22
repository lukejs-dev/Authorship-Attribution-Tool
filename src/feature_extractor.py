# src/feature_extractor.py
import numpy as np
from collections import Counter
from src.preprocessor import STOP_WORDS # Import the shared stop words set

# Create a sorted list for consistent vector ordering
SORTED_STOP_WORDS = sorted(list(STOP_WORDS))

def calculate_function_word_frequencies(tokens_list):
    """
    Calculates the frequency of predefined function words in a list of tokens.
    Returns a numpy array of frequencies.
    """
    if not tokens_list:
        return np.zeros(len(SORTED_STOP_WORDS))

    token_counts = Counter(tokens_list)
    
    placeholders = {'[mention]', '[emoji]', '[url]', '[code_block]', '[inline_code]'}
    total_real_tokens = sum(1 for token in tokens_list if token not in placeholders)
    
    if total_real_tokens == 0:
        return np.zeros(len(SORTED_STOP_WORDS))
        
    fw_counts = [token_counts.get(word, 0) for word in SORTED_STOP_WORDS]
    
    return np.array(fw_counts) / total_real_tokens