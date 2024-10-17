import os
import pickle
from scholarly import scholarly


# Function to convert a Google Scholar result to BibTeX format
def result_to_bibtex(result) -> str:
	entry_type = "@article"

	# Extract necessary fields for BibTeX
	title = result.get('bib', {}).get('title', "N/A")
	authors = " and ".join(result.get('bib', {}).get('author', []))
	year = result.get('bib', {}).get('pub_year', "N/A")
	url = result.get('pub_url', "N/A")
	journal = result.get('bib', {}).get('venue', "Google Scholar")
	abstract = result.get('bib', {}).get('abstract', "")
	citation_count = result.get('num_citations', 0)

	# Create the BibTeX entry string with additional details
	bibtex_entry = f"""
    {entry_type}{{
        title = {{{title}}},
        author = {{{authors}}},
        year = {{{year}}},
        journal = {{{journal}}},
        url = {{{url}}},
        abstract = {{{abstract}}},
        citations = {{{citation_count}}}
    }}
    """
	return bibtex_entry


# Fetch papers from Google Scholar
def fetch_google_scholar(category, keyword: str, year: int, max_results=10) -> list:
	search_query = scholarly.search_pubs(f'{category} {keyword}', year_low=year, year_high=year+1)
	results = []

	for i, result in enumerate(search_query):
		if i >= max_results:
			break
		results.append(result)

	return results


# Example of sorting by title before generating BibTeX
def sort_by_title(results):
	return sorted(results, key=lambda result: result.get('bib', {}).get('title', "").lower())  # Sorting by title


# Main execution
if __name__ == "__main__":
	entries = []
	if os.path.exists('data/GoogleScholar_CV.pkl'):
		with open('data/GoogleScholar_CV.pkl', 'rb') as file:  # 'rb' is read binary mode
			entries = pickle.load(file)

	countPerCategory = 10
	years = list(range(2023, 2025))
	categories = ["vision"]
	keywords = [
		"literature", "review", "survey", "multimodal", "llm", "neural network", "deep learning", "transformer", "cnn",
		"convolution", "image", "3D", "radiance field", "encoder", "decoder", "attention", "segment", "video",
		"dataset", "generative", "synthetic", "diffusion", "gaussian", "language"
	]
	papers = []

	# Open the log file in append mode
	with open('data/log.txt', 'a') as log_file:
		for year in years:
			for category in categories:
				for keyword in keywords:
					# Fetch papers and process them
					papers = fetch_google_scholar(category, keyword, year, countPerCategory)
					sorted_results = sort_by_title(papers)
					entries = entries + [result_to_bibtex(result) for result in sorted_results]

					# Log success
					log1 = f"Google Scholar\nCategory: {category}, Keyword: {keyword}, Year: {year}\n"
					log2 = f"Number of papers processed: {len(sorted_results)}\n\n"
					log_file.write(log1)
					log_file.write(log2)
					print(log1 + log2)

					# Save the updated entries to the .pkl file
					with open('data/GoogleScholar_CV.pkl', 'wb') as file:
						pickle.dump(list(set(entries)), file)
