# index.py
# Scott Metoyer, 2013
# Retrieves a list of new NZB's from the newsgroups specified in a config file
from nntplib import *
from config import config
from pymongo import MongoClient
import string
import datetime
import time

mongo_connection = MongoClient('localhost', 27017)
db = mongo_connection.nzb_database
newsgroups = db.newsgroup_collection
articles = db.article_collection

def connect():
    print('Connecting to ' + config["usenet_server"] + '...')
    server = NNTP(config["usenet_server"], config["usenet_port"], config["usenet_username"], config["usenet_password"])
    return server
    
def fetch_articles(group, start_index):
    article_count = 0
    start = time.time()
    
    server = connect()
    
    print('Reading from group ' + group + '...')
    resp, count, first, last, name = server.group(group)
  
    print('Getting a list of nzb files in ' + group + '...')

    if start_index < int(first):
        start_index = int(first)
        
    current_index = int(start_index)
    last_index = int(last)
    chunk_size = 10000

    while (current_index < last_index):
        if (current_index + chunk_size >= last_index):
            chunk_size = last_index - current_index
        
        try:
            resp, items = server.xover(str(current_index), str(current_index + chunk_size))
        except:
            print("Error grabbing articles. Attempting to reconnect...")
            server = connect()
            server.group(group)
            resp, items = server.xover(str(current_index), str(current_index + chunk_size))
            print("Reconnected.")
            
        for number, subject, poster, date, id, references, size, lines in items:
            if '.nzb' in subject.lower():
                article = {"message-id": id,
                           "group": group,
                           "article-number": number,
                           "subject": subject,
                           "date": date}
                try:
                    articles.insert(article)
                    print(number + ": " + subject)
                    article_count += 1
                except:
                    print("Error inserting article. Continuing...")
                
        current_index += chunk_size
        
    server.quit()
    end = time.time()
    elapsed = end - start
    print("Execution time: " + str(elapsed / 60) + " minutes")
    print("Total articles added: " + str(article_count))
    return current_index
    
def get_group(group_name):
    group = newsgroups.find_one({"name": group_name})
    
    if group == None:
        group = {"name": group_name,
                 "last_scan": datetime.datetime.now(),
                 "last_article": 0}
        newsgroups.insert(group)
        
    return group

def update_group(group_name, last_article):
    # Make sure the group exists
    get_group(group_name)
    
    newsgroups.update({"name": group_name}, 
                      {"$set":  {
                                    "last_scan": datetime.datetime.now(), 
                                    "last_article": last_article
                                }
                      })
    
group_name = 'alt.binaries.movies'
settings = get_group(group_name)
last_index = fetch_articles(group_name, settings["last_article"] + 1)
update_group('alt.binaries.movies',  last_index)