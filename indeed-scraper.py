import time
import pandas as pd
import re

from job import Job
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("Search For Jobs\n")
search_job_value = input("With all of these words: ")
search_word_value = input("With at least one of these words: ")
file_name = input("Save file with name: ")
print("\n")

DRIVER_PATH = './chromedriver'
# hide the chrome window using options 
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)

driver.get('https://ca.indeed.com')

initial_search_button = driver.find_element_by_xpath('//*[@id="whatWhereFormId"]/div[3]/button')
initial_search_button.click()

advanced_search = driver.find_element_by_xpath("//a[contains(text(), 'Advanced Job Search')]")
advanced_search.click()

#search values
search_job = driver.find_element_by_xpath('//input[@id="as_and"]')
search_job.send_keys([search_job_value])

search_word = driver.find_element_by_xpath('//input[@id="as_any"]')
search_word.send_keys([search_word_value])

#sort by last 15
sort_option = driver.find_element_by_xpath('//select[@id="fromage"]//option[@value="15"]')
sort_option.click()

#limit search results to 30 results per page
display_limit = driver.find_element_by_xpath('//select[@id="limit"]//option[@value="30"]')
display_limit.click()

#click the search button
search_button = driver.find_element_by_xpath('//*[@id="fj"]')
search_button.click()

#close pop-up
time.sleep(0.5) #wait for the popup to appear
close_popup = driver.find_element_by_xpath('//*[@id="popover-x"]')
close_popup.click()

#go through job cards
driver.implicitly_wait(3)

jobs = []

links = []
descriptions = []

print ("Scraping the following jobs: \n")
for i in range(0, 20):
    job_card = driver.find_elements_by_xpath('//div[contains(@class,"clickcard")]')

    for job in job_card:
        #not all companies have reviews, salaries and a location posted
        try: 
            review = job.find_element_by_xpath('.//span[@class="ratingsContent"]').text
        except:
            review = "None" 

        try: 
            salary = job.find_element_by_xpath('.//span[@class="salaryText"]').text
        except:
            salary = "None" 

        try: 
            location = job.find_element_by_xpath('.//span[@class="location"]').text
        except:
            location = "None" 

        #get the title of the job 
        try:
            title = job.find_element_by_xpath('.//h2[@class="title"]//a').text
        except:
            title = job.find_element_by_xpath('.//h2[@class="title"]//a').get_attribute(name="title")
        print(title)

        link = job.find_element_by_xpath('.//h2[@class="title"]//a').get_attribute(name="href")
        links.append(link)

        company = job.find_element_by_xpath('.//span[@class="company"]').text

        job = Job(title, company, location, link, review, salary)
        jobs.append(job)

    #move to another page
    try:
        next_page = driver.find_element_by_xpath('//a[@aria-label="Next"]//span[@class="np"]')
        next_page.click()
    except:
        print("\nFinished Scraping Jobs")
        break
    #print the page you're on 
    print("\nPage: {}".format(str(i+2)))

print("Scraping Job Descriptions...\n")

count = 0
for link in links:
    driver.get(link)
    job_description = driver.find_element_by_xpath('//div[@id="jobDescriptionText"]').text
    jobs[count].add_description(job_description)
    count = count + 1

#create an HTML file to view the data nicely
html = ""

htmlBeginning = '''\
<html>
  <head></head>
  <h1>Jobs:</h1>
  <body>
'''

htmlMiddle = ""
for job in jobs:
    title = job.get_title()
    company = job.get_company()
    review = job.get_review()
    location = job.get_location()
    salary = job.get_salary()
    description = job.get_description()
    link = job.get_link()

    if review == "None":
        review = "No posted company review"
    if salary == "None": 
        salary = "No posted job salary"
    if location == "None": 
        location = "No posted location"

    #replace new line characters with a break to make it display nicer on the html
    description = re.sub(r'(\n)', r'\1<br>', description)

    htmlMiddle += '''\
        <p>----------------------------------------------------------------------------------------------</p>
        <h2>{title} - {salary}</h2>
        <h3>Company: {company} - {review}</h3>
        <h4>Location: {location}</h4>
        <p>{description}</p>
        <a href="{link}">Link</a><br><br>
        <p>----------------------------------------------------------------------------------------------</p>
    '''.format(title = title, company = company, review = review, location = location,
               salary = salary, description = description, link = link)

htmlEnding = '''\
  </body>
</html>
'''

html = htmlBeginning + htmlMiddle + htmlEnding

with open(file_name + ".html", "w") as html_file: 
    html_file.write(html)

print("Jobs written to HTML file: " + file_name + ".html")

driver.quit()