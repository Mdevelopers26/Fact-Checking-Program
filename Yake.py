# "pip install BeautifulSoup4" to install Beautiful Soup

import yake
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

kw_extractor = yake.KeywordExtractor()
keywords = kw_extractor.extract_keywords(text)


for kw in keywords:
    print(kw)

#Print the keyword with highest Rating
print(keywords[-1][0])