import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    initial_probability = (1 - damping_factor) / len(corpus)
    probability = {}
    for pages in corpus:
        probability[pages] = initial_probability
    links = corpus[page]
    if len(links) > 0:
        link_prob = damping_factor / len(links)
        for link in links:
            probability[link] += link_prob
    else:
        for pages in corpus:
            probability[pages] += damping_factor / len(corpus)
    return probability
            
    

def sample_pagerank(corpus, damping_factor, n):
    count = {}
    for page in corpus:
        count[page] = 0
    pages = list(corpus.keys())
    current_page = random.choice(pages)
    count[current_page] += 1
    for i in range(1,n):
        probability_2 = transition_model(corpus, current_page, damping_factor)
        dict_2 = list(probability_2.keys())
        prob_2 = list(probability_2.values())
        next_page = random.choices(dict_2, prob_2)[0]
        count[next_page] += 1
        current_page = next_page
    pagerank = {}
    for pages in count:
        pagerank[pages] = count[pages] / n
    return pagerank
          
        


def iterate_pagerank(corpus, damping_factor):
    N = len(corpus.keys())
    pagerank = {}
    for page in corpus:
        pagerank[page] = 1/N
    while True:
        old_ranks = pagerank.copy()
        new_ranks = {}
        for page in corpus:
            new_ranks[page] = (1 - damping_factor) / N
            for p in corpus:
                if page in corpus[p]:
                    new_ranks[page] += damping_factor * old_ranks[p] / len(corpus[p])
                elif len(corpus[p]) == 0: 
                    new_ranks[page] += damping_factor * old_ranks[p] / N
        change = True
        for page in pagerank:
            if abs(new_ranks[page] - old_ranks[page]) > 0.001:
                change = False
        if change:
                break
        else:
            pagerank = new_ranks
    return pagerank 

       



if __name__ == "__main__":
    main()
