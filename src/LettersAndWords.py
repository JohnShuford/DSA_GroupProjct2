import re
import nltk
from nltk.corpus import stopwords

try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')

# Preprocessing Function for a Gutenberg Project Book
def process_book(input_file, output_file, start_marker, end_marker):

    # Read full text file
    with open(input_file, "r", encoding="utf-8") as file:
        book = file.read()

    # Separate main text from Gutenberg markers
    if start_marker in book and end_marker in book:
        main_text = book.split(start_marker, 1)[1].split(end_marker, 1)[0].strip()
    else:
        raise ValueError("Start or end marker not found in text file.")

    # Convert to lowercase
    main_text = main_text.lower()

    # Remove punctuation, digits, and special characters using regex (keep only letters and spaces)
    clean_text = re.sub(r'[^a-zA-Z\s]', '', main_text)

    # Normalize whitespace
    clean_text = re.sub(r"\s+", " ", clean_text).strip()

    # Write cleaned text to a new file
    with open(output_file, "w", encoding="utf-8") as new_file:
        new_file.write(clean_text)

    return clean_text

# Tokenize by whitespace
def tokenize(text):
    tokens = text.strip().split()
    return tokens

# Remove stopwords using nltk
def remove_stopwords(tokens):
    stop_words = set(stopwords.words('english'))

    # Remove punctuation/digits/special characters to match our format
    clean_stop_words = [re.sub(r'[^a-zA-Z\s]','', word) for word in list(stop_words)]

    words = [t for t in tokens if t not in clean_stop_words]
    
    # get rid of word 'chapter' (so ToC does not affect word analysis)
    ## This word does appear within the main body of the novel but word is not frequent enough to significantly affect analysis
    lw = [word for word in words if word != "chapter"]
    
    return lw, clean_stop_words