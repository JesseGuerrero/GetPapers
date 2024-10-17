import os
import pickle
import requests

# Function to read the API key from the file
def read_api_key(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, 'r') as file:
        # Read the first line and strip any surrounding whitespace or newlines
        api_key = file.readline().strip()

    return api_key

# Example usage
api_key_file = "ScienceDirectKey"
API_KEY = read_api_key(api_key_file)

# Function to convert a ScienceDirect result to BibTeX format
def result_to_bibtex(result) -> str:
    print(result)
    entry_type = "@article"

    # Extract necessary fields for BibTeX
    title = result.get('dc:title', "N/A")

    # Handling both cases where authors could be a list of dicts or a string
    authors_list = result.get('authors', {}).get('author', [])
    if isinstance(authors_list, str):
        authors = authors_list  # If it's a string, use it directly
    else:
        # If it's a list of dictionaries, retrieve the value from the appropriate key ('$')
        authors = " and ".join(
            [author.get('$', "N/A") if isinstance(author, dict) else str(author) for author in authors_list])

    # Extract year from publicationDate if available
    year = result.get('prism:coverDate', "N/A")[:4]

    # Extract journal name (publicationName)
    journal = result.get('prism:publicationName', "ScienceDirect")

    # Extract URL, handling potential variations in the link structure
    link_list = result.get('link', [])
    url = "N/A"
    if link_list:
        url = link_list[0].get('@href', "N/A")

    # Extract DOI if available
    doi = result.get('prism:doi', result.get('dc:identifier', "N/A").replace("DOI:", ""))

    # Create the BibTeX entry string with additional details
    bibtex_entry = f"""
    {entry_type}{{
        title = {{{title}}},
        author = {{{authors}}},
        year = {{{year}}},
        journal = {{{journal}}},
        url = {{{url}}},
        doi = {{{doi}}}
    }}
    """
    return bibtex_entry


# Fetch papers from ScienceDirect
def fetch_sciencedirect_papers(category: str, keyword: str, year: int, max_results=10) -> list:
    headers = {
        'X-ELS-APIKey': API_KEY,
        'Content-Type': 'application/json'
    }

    # Create the query string
    query = f"{category} {keyword} AND PUBYEAR IS {year}"

    # ScienceDirect API URL for search
    url = "https://api.elsevier.com/content/search/sciencedirect"

    params = {
        'query': query,
        'count': max_results
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
        return []

    data = response.json()
    results = data.get('search-results', {}).get('entry', [])
    return results

# Example of sorting by title before generating BibTeX
def sort_by_title(results):
    return sorted(results, key=lambda result: result.get('title', "").lower())  # Sorting by title

# Main execution
if __name__ == "__main__":
    entries = []
    if os.path.exists('data/ScienceDirect_CV.pkl'):
        with open('data/ScienceDirect_CV.pkl', 'rb') as file:  # 'rb' is read binary mode
            entries = pickle.load(file)

    countPerCategory = 3
    years = list(range(2022, 2024))
    categories = ["vision"]
    keywords = [
        "literature",
		# "review", "survey", "multimodal", "llm", "neural network", "deep learning", "transformer", "cnn",
        # "convolution", "image", "3D", "radiance field", "encoder", "decoder", "attention", "segment", "video",
        # "dataset", "generative", "synthetic", "diffusion", "gaussian", "language"
    ]
    papers = []

    # Open the log file in append mode
    with open('data/log.txt', 'a') as log_file:
        for year in years:
            for category in categories:
                for keyword in keywords:
                    # Fetch papers and process them
                    papers = fetch_sciencedirect_papers(category, keyword, year, countPerCategory)
                    sorted_results = sort_by_title(papers)
                    entries = entries + [result_to_bibtex(result) for result in sorted_results]

                    # Log success
                    log1 = f"Category: {category}, Keyword: {keyword}, Year: {year}\n"
                    log2 = f"Number of papers processed: {len(sorted_results)}\n\n"
                    log_file.write(log1)
                    log_file.write(log2)
                    print(log1 + log2)

                    # Save the updated entries to the .pkl file
                    with open('data/ScienceDirect_CV.pkl', 'wb') as file:
                        pickle.dump(list(set(entries)), file)
