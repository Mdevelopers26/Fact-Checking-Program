# "pip install BeautifulSoup4" to install Beautiful Soup
# "pip install KeyBert" to install KeyBert

from urllib.request import urlopen
from bs4 import BeautifulSoup
from keybert import KeyBERT


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

kw_model = KeyBERT()
keywords = kw_model.extract_keywords(text)

print(keywords)

#To get the keyword with highest rating
print(keywords[0][0])