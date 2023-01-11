# First need to run this in the terminal "pip install rake-nltk" To install RAKE and

# "pip install BeautifulSoup4" to install Beautiful Soup

from rake_nltk import Rake
from urllib.request import urlopen
from bs4 import BeautifulSoup

# ------------------------------------ (Section) To extracting text from HTML Obtained from https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python----


url = "https://www.telegraph.co.uk/football/2022/09/07/thomas-tuchel-sacked-chelsea-owner-todd-boehly/"
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()  # rip it out

# get text


text_page = """

            """
text = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
r = Rake(min_length=1, max_length=3)

# COMMON USE


# print the desired number of most common word
#
# print(r.extract_keywords_from_text(text))
# print(r.get_ranked_phrases_with_scores())

r.extract_keywords_from_text(text)
a= r.get_ranked_phrases_with_scores()
print(a)

print(a[0][1])

# Eliminate ratings which are too low/ eliminate single words
# for rating, keyword in r.get_ranked_phrases_with_scores():
#     if rating > 5:
#         print(rating, keyword)



