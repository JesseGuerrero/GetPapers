import os
import pickle
import bibtexparser

# Main execution
if __name__ == "__main__":
    entries = []
    if os.path.exists('data/arXiV_CV.pkl'):
        with open('data/arXiV_CV.pkl', 'rb') as file:
            entries = pickle.load(file)

    for entry in entries:
        print(entry)
