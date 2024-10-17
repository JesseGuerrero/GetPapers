import os
import arxiv
import pickle
from scholarly import scholarly

# Function to convert an arXiv result to BibTeX format
def result_to_bibtex(result: arxiv.Result) -> str:
	# Generate the BibTeX entry type
	entry_type = "@article"

	# Extract necessary fields for BibTeX
	title = result.title
	authors = " and ".join([author.name for author in result.authors])
	year = result.published.year
	month = result.published.strftime('%B') if result.published else ""
	arxiv_id = result.get_short_id()
	url = result.entry_id
	doi = result.doi if result.doi else "N/A"
	journal_ref = result.journal_ref if result.journal_ref else "arXiv preprint"
	comment = result.comment if result.comment else ""
	categories = ", ".join(result.categories)

	# Create the BibTeX entry string with additional details
	bibtex_entry = f"""
    {entry_type}{{arxiv:{arxiv_id},
        title = {{{title}}},
        author = {{{authors}}},
        year = {{{year}}},
        month = {{{month}}},
        journal = {{{journal_ref}}},
        archivePrefix = {{arXiv}},
        eprint = {{{arxiv_id}}},
        primaryClass = {{{result.primary_category}}},
        categories = {{{categories}}},
        doi = {{{doi}}},
        url = {{{url}}},
        comment = {{{comment}}}
    }}
    """

	return bibtex_entry


# Fetch papers from arXiv in 'cs.CV' (Computer Vision)
def fetch_arxiv_papers(category: str, keyword: str, year: int, max_results=10):
	query = f"cat:{category} AND {keyword} AND submittedDate:[{year}0101 TO {year+1}1231]"
	search = arxiv.Search(
		query=query,
		max_results=max_results,
		sort_by=arxiv.SortCriterion.Relevance
	)
	return list(search.results())


# Example of sorting by title before generating BibTeX
def sort_by_title(results):
	return sorted(results, key=lambda result: result.title.lower())  # Sorting by title case-insensitively





# Main execution
if __name__ == "__main__":
	entries = []
	if os.path.exists('data/arXiV_CV.pkl'):
		with open('data/arXiV_CV.pkl', 'rb') as file:  # 'rb' is read binary mode
			entries = pickle.load(file)

	countPerCategory = 100
	years = list(range(1991, 2025))
	categories = ["cs.CV"]
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
					papers = fetch_arxiv_papers(category, keyword, year, countPerCategory)
					sorted_results = sort_by_title(papers)
					entries = entries + [result_to_bibtex(result) for result in sorted_results]

					#log success
					log1 = f"ArXiV\nCategory: {category}, Keyword: {keyword}, Year: {year}\n"
					log2 = f"Number of papers processed: {len(sorted_results)}\n\n"
					log_file.write(log1)
					log_file.write(log2)
					print(log1 + log2)

					# Save the updated entries to the .pkl file
					with open('data/arXiV_CV.pkl', 'wb') as file:
						pickle.dump(list(set(entries)), file)