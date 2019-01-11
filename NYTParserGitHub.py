import pandas as pd
import requests
from bs4 import BeautifulSoup
import string
import os.path
import csv
import sys

def allSundays(year): #NYT released all marriage announcements for 2018 every Sunday, this function returns all the dates for every Sunday in 2018
    return pd.date_range(start=str(year), end=str(year+1), freq='W-SUN').strftime('%Y/%m/%d').tolist() #returns list of Sundays

def addtoBaseURLs(dates): #function returns a URL formatted with the date for every Sunday to be used in scraping
    baseurls = list() #list of URLs
    for date in dates: #iterate through every date in the dates list
        baseurl = 'https://www.nytimes.com/{}/fashion/weddings/this-weeks-wedding-announcements.html'.format(date)
        baseurls.append(baseurl) #add new URL to list of URLS
    return baseurls

def get_announcement_URL(baseurls): #function returns a list of every URL that includes a marriage announcement
    announcement_URLs = list() #list of URLs for announcements
    for base in baseurls:
        try: #to prevent error from URL for a Sunday in the year that has not passed
            req = requests.get(base) #get the base URL
            req_soup = BeautifulSoup(req.text, 'html.parser')
            soup_div = req_soup.find('div',{'id':'app'})
            soup_contents = soup_div.find('article',{'id':'story'})
            soup_urls = soup_contents.findAll('h2') #part of the webpage which includes all the URLs for the marriage announcements released that week
            for url in soup_urls:
                announcement_URL = url.find('a').get('href') #get the link for the announcement
                announcement_URLs.append(announcement_URL) #add to list of URLs for the marriage announcements
        except:
            continue
    return announcement_URLs

def articleParser2018(test): #parsing through each marriage announcement URL
    stories = list() #initializing a list for all the couple love stories
    for link in test: #iterating through each announcement URL
        try:
            req_link = requests.get(link)
            link_soup = BeautifulSoup(req_link.text, 'html.parser')
            link_div = link_soup.find('div',{'id':'app'})
            link_contents = link_div.find('article',{'id':'story'}) #finding the text for the article
            couple_name = link_contents.find('h1').text #retrieving the name of each individual in the couple
            link_main_section = link_contents.find('section',{'name': 'articleBody'}) #finding the body for the article
            link_main_text = link_main_section.findAll('p')
            story = list() #list of all the dictionary items for one couple
            for p in link_main_text:
                link_body = p.text #main body text
                link_lines = link_body.split('\n') #split the main body by new line
                story_dict = dict() #initializing dictionary for couple
                for line in link_lines: #iterating through each line of the article
                    if 'met' in line: #identifying statement about how the couple met
                        story_dict['Name'] = couple_name #store name of each individual in the couple
                        story_dict['Married in'] = '2018' #store the year they got married, 2018 for all couples
                        story_dict['How They Met'] = line #store line that indicates how they met
                        for word in line.split(): #split this line by word
                            word = word.translate(word.maketrans('','',string.punctuation)) #remove punctuation from each word
                            if word.isdigit(): #identify numbers in the line
                                word = str(word) #convert number to string in order to store in the dictionary
                                story_dict['When They Met'] = word #store when the couple met
                        story.append(story_dict) #append the dictionary to a list of all the dictionary values for the couple
                    else:
                        continue
            stories.append(story) #append the couple's story to all the couple stories
        except:
            continue
    return stories

def NYT_writer(final,file_output): #function writes out the CSV for the NYT announcements, takes in the name for the file_output and list of couple stories
    with open(file_output, 'w') as outputfile:
        writer = csv.writer(outputfile)
        fileEmpty = os.stat(file_output).st_size == 0 #variable to describe what an emptyfile is
        column_names = final[1][0].keys() #headers for the CSV
        if fileEmpty: #only write headers if the file is empty
            writer.writerow(column_names)
        for story in final: #iterate through every couple story in the list
            if len(story) > 0: #ensuring list item is not empty
                if len(story) > 1: #if the list item has more than one list of dictionary items - this occurs if 'met' was found in two sentences
                    values = story[-1].values() #values for the row will be in the last dictionary list
                    writer.writerow(values) #write rows in the CSV
                else:
                    values = story[0].values() #values for the row will be in the first dictionary list
                    writer.writerow(values)
