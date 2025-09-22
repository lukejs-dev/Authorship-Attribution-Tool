## Notes
Code comments and verbose prints were added using assistance from AI.

## Installation
1. Clone the repository

2. Install required packages

3. Download spaCy language model

## Usage
Place channel export CSV files in 'sample_data/context' directory and the unknown text(s) in the 'sample_data/individual' directory.

Then, run the analysis from project root

Example:
```bash
python src/main.py --channels sample_data/context --target sample_data/individual
```

## Methods
This tool uses stylometry to identify authors. It extracts 3 feature types: character n-grams, word n-grams, and function word frequencies. The features are vectorized using TF-IDF and combined into single feature vector for each "user". The similarity between the target document(s) and each user is calculated using Cosine Similarity.

# Considerations
This tool provides probabilistic evidence, not definitive proof. The results are intended to a be a starting point for further qualitative investigation and not a final conclusion. The underlying methodology has multiple important limitations that must be understood to interpret results responsibly.

## Technical and Methodological Limitations
Topic Influence vs Stylistic Signaling: The TF-IDF vectorizer is effective at finding vocabulary patterns but often struggles to distinguish between unique writing style and unique topic of discussion. If a niche subject is frequently discussed (like a specific programming library) and the target document is about the same subject then the similarity score will likely be inflated due to shared vocabulary and not just writing style.
Feature Scope: The model uses a combination of linguistic n-grams and function frequencies but it doesn't capture all aspects of an author's style like sentence complexity and punctuation habits or spelling errors.
Relative Scoring: Similarity scores are not absolute probabilities and are only meaningful when compared to one another within the same analysis. The difference between the top-ranked user and the runners-up can indicate whether multiple users have a similar profile according to the methodology.

Sample size sensitivity: The most important factor is how large the individual's sample is, high scores for low message counts are not particularly indicative of a conclusion due to small sample bias.
Context shift: A user's style profile changes depending on the context (e.g. chat room vs blog post) and this tool inherently assumes that these styles are reasonably consistent which is often not true.
Temporal drift: A user's style profile also changes over time and old messages are generally less effective at predicting recent documents.

Misuse: The output of this tool shouldn't be the sole basis for punitive actions.
Privacy: Analysis is performed using user-generated content and users are responsible for garnering permission to analyze the data.
Confirmation bias: It is easy to look at results and focus only on the candidate you suspect, always perform qualitative review of potential candidates and don't rely solely on numbers.

## License
This project is license under MIT license, see license file for details.