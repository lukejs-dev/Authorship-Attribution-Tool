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

## Considerations


## License
This project is license under MIT license, see license file for details.