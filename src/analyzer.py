# src/analyzer.py
import time
import numpy as np
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src import data_loader, preprocessor, feature_extractor

class AuthorshipAnalyzer:
    def __init__(self, channels_dir, target_dir):
        self.channels_dir = channels_dir
        self.target_dir = target_dir
        self.results = []

    def run(self):
        """Public method to execute the entire analysis pipeline."""
        # 1. Load Data
        user_messages, self.user_counts = data_loader.load_and_group_discord_data(self.channels_dir)
        target_content = data_loader.load_and_combine_target_documents(self.target_dir)

        if not user_messages or not target_content:
            raise ValueError("Failed to load necessary user or target data.")

        # 2. Preprocess Data
        user_ids = list(user_messages.keys())
        all_raw_texts = list(user_messages.values()) + [target_content]
        cleaned_texts = [preprocessor.clean_text_for_nlp(text) for text in all_raw_texts]
        
        docs = preprocessor.process_text_with_spacy(cleaned_texts)
        
        processed_data = []
        for doc in docs:
            # The original cleaned string is useful for char-level features
            original_string = doc.text
            tokens = preprocessor.extract_tokens_from_doc(doc)
            processed_data.append({'string': original_string, 'tokens': tokens})
        
        # 3. Feature Extraction & Comparison
        self._extract_and_compare(user_ids, processed_data)

    def _extract_and_compare(self, user_ids, processed_data):
        """Handles vectorization, feature combination, and similarity calculation."""
        user_data = processed_data[:-1]
        target_data = processed_data[-1]

        all_strings = [d['string'] for d in user_data] + [target_data['string']]
        all_token_strings = [" ".join(d['tokens']) for d in user_data] + [" ".join(target_data['tokens'])]
        all_token_lists = [d['tokens'] for d in user_data] + [target_data['tokens']]
        
        # Feature 1: Char n-grams
        char_vect = TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5), min_df=3)
        char_features = char_vect.fit_transform(all_strings)
        
        # Feature 2: Word n-grams
        word_vect = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=3)
        word_features = word_vect.fit_transform(all_token_strings)
        
        # Feature 3: Function Words
        fw_features = np.array([feature_extractor.calculate_function_word_frequencies(tl) for tl in all_token_lists])
        
        # Combine all features
        combined_features = hstack([char_features, word_features, fw_features]).tocsr()
        
        target_vector = combined_features[-1]
        user_vectors = combined_features[:-1]
        
        # Calculate similarity
        sim_scores = cosine_similarity(target_vector, user_vectors)[0]
        
        for i, user_id in enumerate(user_ids):
            self.results.append((user_id, sim_scores[i], self.user_counts.get(user_id, 0)))
            
        self.results.sort(key=lambda item: item[1], reverse=True)

    def display_results(self, top_n=20):
        """Prints the final ranked results and interpretation notes."""
        if not self.results:
            print("No analysis has been run or no results were generated.")
            return

        print("\n--- 🏆 Authorship Likelihood Ranking 🏆 ---")
        print(f"{'Rank':<5} | {'AuthorID':<19} | {'Similarity Score':<18} | {'Message Count':<15}")
        print("-" * 68)
        
        for rank, (user_id, score, count) in enumerate(self.results[:top_n], 1):
            print(f"{rank:<5} | {user_id:<19} | {score:<18.4f} | {count:<15}")
        
        print("\n--- Interpretation Notes ---")
        print("Scores range from 0 (dissimilar) to 1 (identical). A higher score suggests a stronger stylistic match.")
        print("Consider the 'Message Count' as a confidence metric; a high score from a user with many messages is more significant.")