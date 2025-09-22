# src/preprocessor.py
import re
import spacy

def _load_spacy_model():
    """Loads the spaCy model, disabling unnecessary components for performance."""
    disabled = ['parser', 'ner', 'attribute_ruler', 'tok2vec']
    try:
        model = spacy.load("en_core_web_sm", disable=disabled)
    except OSError:
        print("Downloading spaCy model 'en_core_web_sm'...")
        spacy.cli.download("en_core_web_sm")
        model = spacy.load("en_core_web_sm", disable=disabled)
    print("SpaCy model loaded successfully.")
    return model

# Load model and stop words once when the module is imported
nlp = _load_spacy_model()
STOP_WORDS = set(nlp.Defaults.stop_words)

def clean_text_for_nlp(text):
    """Applies Discord-specific and general cleaning to a raw text string."""
    if not isinstance(text, str):
        return ""
    
    text = re.sub(r'```.*?```', ' [CODE_BLOCK] ', text, flags=re.DOTALL)
    text = re.sub(r'`.*?`', ' [INLINE_CODE] ', text)
    text = re.sub(r'<@!?\d+>', ' [MENTION] ', text)
    text = re.sub(r'<a?:.+?:\d+>', ' [EMOJI] ', text)
    text = re.sub(r'http[s]?://\S+', ' [URL] ', text)
    
    text = text.lower()
    text = re.sub(r'[^a-z\s\[\]_]', '', text) # Keep only letters, spaces, and our placeholders
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def process_text_with_spacy(texts):
    """
    Processes a list of cleaned texts in parallel using nlp.pipe for efficiency.
    Returns an iterator of spaCy Doc objects.
    """
    return nlp.pipe(texts, n_process=-1, batch_size=500)

def extract_tokens_from_doc(doc):
    """Extracts a list of lemmatized tokens from a spaCy Doc object."""
    if not doc:
        return []
    
    return [
        token.lemma_ for token in doc 
        if not token.is_space and not token.is_punct and token.lemma_ != '-PRON-'
    ]