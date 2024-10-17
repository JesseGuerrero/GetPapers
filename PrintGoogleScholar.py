import os
import pickle
import bibtexparser

# Main execution
if __name__ == "__main__":
    entries = []
    if os.path.exists('data/GoogleScholar_CV.pkl'):
        with open('data/GoogleScholar_CV.pkl', 'rb') as file:
            entries = pickle.load(file)

    with open('data/GoogleScholarBib.txt', 'a', encoding='utf-8') as file:
        for entry in entries:
            file.write(entry)
