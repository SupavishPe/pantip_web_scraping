import pandas as pd
import numpy as np
import time as time
import pickle
import re
import string
import codecs
import os 
from selenium import webdriver
from tqdm import tqdm
import logging
import config 

logging.getLogger().setLevel(logging.INFO)



def open_and_scroll_webpage(website, pause_time, n_scroll, config=config): 
    driver = webdriver.Chrome(executable_path= config.DRIVER_PATH)
    driver.get(website)
    if n_scroll > 0 :
        for _ in range(n_scroll):
            # Scroll down 
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(pause_time)
    else: 
        time.sleep(pause_time)
    return driver

def get_topic_link(driver, classname='pt-list-item__title'):
    topic_lst = driver.find_elements_by_class_name(classname)

    link_lst = []
    for t in topic_lst:
        link = t.find_element_by_css_selector('a').get_attribute("href")
        if len(re.findall(r'https://pantip.com/topic/(\d+)', link)) != 0 : 
            link_lst.append(link)

    link_lst = list(set(link_lst))
    n_link = len(link_lst)    
    logging.info(f'Found {n_link} topics')
    return link_lst

def get_title(driver, classname='display-post-title'):  
    title = driver.find_element_by_class_name(classname)
    title = title.text
    return title

def get_story_comment(driver, sep, classname='display-post-story'):    
    content = driver.find_elements_by_class_name(classname)
    story = content[0].text
    comment = [post.text for post in content[1:] if post.text != '']
    if comment == []: 
        comment = ''
    else: 
        comment = f'{sep}'.join(comment)
    return story, comment

def scrap_title_story(link_lst, pause_time, config=config): 
    driver = webdriver.Chrome(config.DRIVER_PATH)
    titles = []
    stories = []
    comments = []
    for url in tqdm(link_lst):
        driver.get(url)
        title = get_title(driver)
        story, comment = get_story_comment(driver, sep=config.SEPERATE_COMMENT)

        titles.append(title)
        stories.append(story)
        comments.append(comment)
        time.sleep(pause_time)
    driver.quit()
    return titles, stories, comments


if __name__ == '__main__': 
    driver = open_and_scroll_webpage(
        website=config.WEBSITE,
        pause_time=config.PAUSE_TIME_FOR_SCROLLING,
        n_scroll=config.N_SCROLL
        )
    link_lst = get_topic_link(driver)
    driver.quit()

    titles, stories, comments = scrap_title_story(
        link_lst=link_lst,
        pause_time=config.PAUSE_TIME_BTW_TOPIC
    )

    d = {'link': link_lst, 'title': titles, 'story':stories, 'comment':comments}
    df = pd.DataFrame(data=d)
    df.to_csv(f'{config.SAVED_CSV}', index=False, encoding='utf-8-sig')
