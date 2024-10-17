import os
import pickle
import bibtexparser

# Main execution
if __name__ == "__main__":
    entries = []
    if os.path.exists('data/ScienceDirect_CV.pkl'):
        with open('data/ScienceDirect_CV.pkl', 'rb') as file:
            entries = pickle.load(file)

    with open('data/ScienceDirectBib.txt', 'a', encoding='utf-8') as file:
        for entry in entries:
            file.write(entry)