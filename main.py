# pip install rake-nltk
#pip install BeautifulSoup4
#pip install yake
# pip install KeyBert
#pip install rake

import tkinter
import requests
from tkinter import *
from bs4 import BeautifulSoup
from typing import Counter
import yake
from urllib.request import urlopen
from rake_nltk import Rake
from keybert import KeyBERT


#The Api Key
api_key="AIzaSyDf3a4bvTM_o0uHS6z7axLYwnm_Y2uXS1s"





#---------------------------- Creating the GUI window. ---------------------------#
window = tkinter.Tk()
window.title("Fact checking program with Google API")
window.geometry("1800x1400")
# window.attributes('-fullscreen', True)

#Label
my_label = tkinter.Label(text="Fact checking program integrated to the Google API", font=("Arial", 13, "bold"))
my_label.grid(columnspan=4,column=0,row=0)

my_label1 = tkinter.Label(text="Word to query:", font=("Arial", 13, "bold"))
my_label1.grid(column=0,row=2)

my_label2 = tkinter.Label(text="URL for Webpage[Frequency]: ", font=("Arial", 13, "bold"))
my_label2.grid(column=0,row=3)

my_label3 = tkinter.Label(text="URL for Webpage[Yake]: ", font=("Arial", 13, "bold"))
my_label3.grid(column=0,row=4)

my_label4 = tkinter.Label(text="URL for Webpage[Keybert]: ", font=("Arial", 13, "bold"))
my_label4.grid(column=0,row=5)

my_label5 = tkinter.Label(text="URL for Webpage[RAKE]: ", font=("Arial", 13, "bold"))
my_label5.grid(column=0,row=6)

#Input boxes
#Entry Component for the Keyword Searh
input1 = Entry(width=10)
input1.grid(column=1,row=2)

#Entry Component for the url: most common word Search
input2=Entry(width=90)
input2.grid(column=1,row=3)

# Entry Component for the YAKE search
input3=Entry(width=90)
input3.grid(column=1,row=4)

# Entry Component for the Keybert search
input4=Entry(width=90)
input4.grid(column=1,row=5)

# Entry Component for the Rake search
input5=Entry(width=90)
input5.grid(column=1,row=6)

#Get the word that user entered
# a=str(input1.get())

#Written Text which shows what the keyword is
keyword_label = tkinter.Label(text=f"The Calculated keyword is: ", font=("Arial", 13, "bold"))
keyword_label.grid(column=1,row=7)


#TextBox where the results will be displayed
text_box = Text( width=95,height=50,borderwidth=2, relief="groove")
text_box.grid(column=1,row=8)

# #TextBox for most common word
# text_box1 = Text( width=20,height=15,)
# text_box.grid

def print_box():
    text_box.insert('end',"string")

#To fetch results for the keyword manually entered in the text box
def Query_word():
    parameters = {
        "query":input1.get(), #To get the input from the text box
        "key" :api_key,
        "languageCode":"en-gb" or "en-us",
        "pageSize":5,
    }
    #End point for the API Service; Needed to get the response
    response = requests.get(url="https://factchecktools.googleapis.com/v1alpha1/claims:search", params=parameters)
    #Reise an exception if there are any errors
    response.raise_for_status()
    #Get the data using the json Methodda
    data = response.json()
    # print(response.json())

    #Clear the text_box
    text_box.delete("1.0", "end")

    try:

    #Iterate through the json and print only the required fields
    # text_box.insert('end', "hhi")
        for claim in data['claims']:
            text_box.insert('end',(f"text: {claim['text']}"))
            text_box.insert('end', ('\n'))
            for review in claim['claimReview']:
                text_box.insert('end',(f"url: {review['url']}"))
                text_box.insert('end', ('\n'))
                text_box.insert('end',(f"title: {review['title']}"))
                text_box.insert('end', ('\n'))
                text_box.insert('end',(f"textualRating: {review['textualRating']}"))
                text_box.insert('end', ('\n'))
                text_box.insert('end',('\n'))


    #Google's Fact checking tool appears to not have reviewed claims on every word
    except KeyError:
        text_box.insert('end',"The Google's Fact checking tool doesn't have any Claims submitted for this Key word")

# Function to get the most common word from the article
def most_common():
    # list of words not to include)
    stop_list = ["that", "from", "sport", "sports", "about", "blog", "contact", "find", "full", "have", "list", "need",
                 "news", "their", "with", "your", "image","after","during","revels","while","shows","this"]

    # prepare a word counter
    word_count = Counter()

    # lets get our web page (adjust to the url you want to review)
    base_url = input2.get()
    r = requests.get(base_url)

    # parse the webpage into an element hierarchy and store in soup
    soup = BeautifulSoup(r.text, 'html.parser')

    # Get only the main text of the page as list of words
    all_words = soup.get_text(" ", strip=True).lower().split()

    # count words
    for word in all_words:
        cln_word = word.strip('.,?')
        # ignore words less 4 characters long
        if len(cln_word) > 3:
            # ignore words in our custom stop list
            if cln_word in stop_list:
                continue
            word_count[cln_word] += 1

    # print the desired number of most common word
    print(word_count.most_common(5))





    parameters = {
        "query": (word_count.most_common(1)[0][0]),  # Gets the most common word from the webpage
        "key": api_key,
        "languageCode": "en-gb" or "en-us",
        "pageSize": 5,
    }
    # End point for the API Service; Needed to get the response
    response = requests.get(url="https://factchecktools.googleapis.com/v1alpha1/claims:search", params=parameters)
    # Reise an exception if there are any errors
    response.raise_for_status()
    # Get the data using the json Methodda
    data = response.json()
    # print(response.json())

    # Clear the text_box
    text_box.delete("1.0", "end")

    # Show the most common word in the GUI
    b=word_count.most_common(1)[0][0]
    keyword_label.configure(text=f"The estimated Keyword is: {b}")

    # Iterate through the json and print only the required fields
    # text_box.insert('end', "hhi")
    try:
        for claim in data['claims']:
            text_box.insert('end', (f"text: {claim['text']}"))
            text_box.insert('end', ('\n'))
            for review in claim['claimReview']:
                text_box.insert('end', (f"url: {review['url']}"))
                text_box.insert('end', ('\n'))
                text_box.insert('end', (f"title: {review['title']}"))
                text_box.insert('end', ('\n'))
                text_box.insert('end', (f"textualRating: {review['textualRating']}"))
                text_box.insert('end', ('\n'))
            text_box.insert('end', ('\n'))

    #Google's Fact checking tool appears to not have reviewed claims on every word
    except KeyError:
        text_box.insert('end',"The Google's Fact checking tool doesn't have any Claims submitted for this Key word")


#Extract keyword using Yake
def yake1():
    # ------------------------------------ (Section) To extracting text from HTML Obtained from https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python----

    url = input3.get()
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
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------

    kw_extractor = yake.KeywordExtractor()
    keywords = kw_extractor.extract_keywords(text)

    for kw in keywords:
        print(kw)

    # Print the keyword with highest Rating
    print(keywords[-1][0])

    # Show the most common word in the GUI
    b = keywords[-1][0]
    keyword_label.configure(text=f"The estimated Keyword is: {b}")

    parameters = {
        "query": (keywords[-1][0]),  # Gets the word with the highest rating
        "key": api_key,
        "languageCode": "en-gb" or "en-us",
        "pageSize": 5,
    }
    # End point for the API Service; Needed to get the response
    response = requests.get(url="https://factchecktools.googleapis.com/v1alpha1/claims:search", params=parameters)
    # Reise an exception if there are any errors
    response.raise_for_status()
    # Get the data using the json Methodda
    data = response.json()
    # print(response.json())

    # Clear the text_box
    text_box.delete("1.0", "end")

    try:
        for claim in data['claims']:
            text_box.insert('end', (f"text: {claim['text']}"))
            text_box.insert('end', ('\n'))
            for review in claim['claimReview']:
                text_box.insert('end', (f"url: {review['url']}"))
                text_box.insert('end', ('\n'))
                text_box.insert('end', (f"title: {review['title']}"))
                text_box.insert('end', ('\n'))
                text_box.insert('end', (f"textualRating: {review['textualRating']}"))
                text_box.insert('end', ('\n'))
            text_box.insert('end', ('\n'))

    #Google's Fact checking tool appears to not have reviewed claims on every word
    except KeyError:
        text_box.insert('end',"The Google's Fact checking tool doesn't have any Claims submitted for this Key word")

#Extract keyword using KeyBert
def KeyBert1():
    # ------------------------------------ (Section) To extracting text from HTML Obtained from https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python----

    url = input4.get()
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
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------

    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(text)

    print(keywords)

    # To get the keyword with highest rating
    b= (keywords[0][0])
    keyword_label.configure(text=f"The estimated Keyword is: {b}")

    parameters = {
        "query": (keywords[0][0]),  # Gets the word with the highest rating
        "key": api_key,
        "languageCode": "en-gb" or "en-us",
        "pageSize": 5,
    }
    # End point for the API Service; Needed to get the response
    response = requests.get(url="https://factchecktools.googleapis.com/v1alpha1/claims:search", params=parameters)
    # Reise an exception if there are any errors
    response.raise_for_status()
    # Get the data using the json Methodda
    data = response.json()
    # print(response.json())

    # Clear the text_box
    text_box.delete("1.0", "end")

    try:
        for claim in data['claims']:
            text_box.insert('end', (f"text: {claim['text']}"))
            text_box.insert('end', ('\n'))
            for review in claim['claimReview']:
                text_box.insert('end', (f"url: {review['url']}"))
                text_box.insert('end', ('\n'))
                text_box.insert('end', (f"title: {review['title']}"))
                text_box.insert('end', ('\n'))
                text_box.insert('end', (f"textualRating: {review['textualRating']}"))
                text_box.insert('end', ('\n'))
            text_box.insert('end', ('\n'))

    #Google's Fact checking tool appears to not have reviewed claims on every word
    except KeyError:
        text_box.insert('end',"The Google's Fact checking tool doesn't have any Claims submitted for this Key word")

#Extract keyword using RAKE
def Rake1():
    # ------------------------------------ (Section) To extracting text from HTML Obtained from https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python----

    url = input5.get()
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
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------

    r = Rake(min_length=1, max_length=3)
    a = r.extract_keywords_from_text(text)
    b=r.get_ranked_phrases_with_scores()

    

    # To get the keyword with highest rating
    c= (b[0][1])
    keyword_label.configure(text=f"The estimated Keyword is: {c}")

    parameters = {
        "query": (c),  # Gets the word with the highest rating
        "key": api_key,
        "languageCode": "en-gb" or "en-us",
        "pageSize": 5,
    }
    # End point for the API Service; Needed to get the response
    response = requests.get(url="https://factchecktools.googleapis.com/v1alpha1/claims:search", params=parameters)
    # Reise an exception if there are any errors
    response.raise_for_status()
    # Get the data using the json Methodda
    data = response.json()
    # print(response.json())

    # Clear the text_box
    text_box.delete("1.0", "end")

    try:
        for claim in data['claims']:
            text_box.insert('end', (f"text: {claim['text']}"))
            text_box.insert('end', ('\n'))
            for review in claim['claimReview']:
                text_box.insert('end', (f"url: {review['url']}"))
                text_box.insert('end', ('\n'))
                text_box.insert('end', (f"title: {review['title']}"))
                text_box.insert('end', ('\n'))
                text_box.insert('end', (f"textualRating: {review['textualRating']}"))
                text_box.insert('end', ('\n'))
            text_box.insert('end', ('\n'))

    #Google's Fact checking tool appears to not have reviewed claims on every word
    except KeyError:
        text_box.insert('end',"The Google's Fact checking tool doesn't have any Claims submitted for this Key word")


#Buttons
# Trigger the function when the button is clicked
button = Button(text="Fetch Data", command=Query_word)
button.grid(column=2,row=2)

button1 = Button(text="Fetch Data", command=most_common)
button1.grid(column=2,row=3)

button2 = Button(text="Fetch Data", command=yake1)
button2.grid(column=2,row=4)

button2 = Button(text="Fetch Data", command=KeyBert1)
button2.grid(column=2,row=5)

button2 = Button(text="Fetch Data", command=Rake1)
button2.grid(column=2,row=6)




window.mainloop()





