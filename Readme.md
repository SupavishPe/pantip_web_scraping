# Scrap data from pantip.com using Selenium

Scrap {title, story, comment} searched by tag at pantip.com

How to run: 
1. download selenium driver at https://chromedriver.chromium.org/downloads and move into this working directory.
2. create new environment
3. pip install -r -requirements.txt
4. if you would like to get new tag, you can change 'TAG_NAME' value in config.py (default='ความรักวัยรุ่น')
5. run python web_scraping.py

Output: .csv file with 4 columns; link, title, story and comment.

