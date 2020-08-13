import time
import pandas as pd

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("Search For Jobs\n")
search_job_value = input("With all of these words: ")
search_word_value = input("With at least one of these words: ")
print("\n")

DRIVER_PATH = './chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

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

titles = []
companies = []
locations = []
links = []
reviews = [] 
salaries = []
descriptions = []

for i in range(0, 20):
    job_card = driver.find_elements_by_xpath('//div[contains(@class,"clickcard")]')

    for job in job_card:
        #not all companies have reviews, salaries and a location posted
        try: 
            review = job.find_element_by_xpath('.//span[@class="ratingsContent"]').text
        except:
            review = "None" 
        reviews.append(review)

        try: 
            salary = job.find_element_by_xpath('.//span[@class="salaryText"]').text
        except:
            salary = "None" 
        salaries.append(salary)

        try: 
            location = job.find_element_by_xpath('.//span[@class="location"]').text
        except:
            location = "None" 
        locations.append(location)

        #get the title of the job 
        try:
            title = job.find_element_by_xpath('.//h2[@class="title"]//a').text
        except:
            title = job.find_element_by_xpath('.//h2[@class="title"]//a').get_attribute(name="title")
        print(title)
        titles.append(title)

        link = job.find_element_by_xpath('.//h2[@class="title"]//a').get_attribute(name="href")
        links.append(link)

        company = job.find_element_by_xpath('.//span[@class="company"]').text
        companies.append(company)

    #move to another page
    try:
        next_page = driver.find_element_by_xpath('//a[@aria-label="Next"]//span[@class="np"]')
        next_page.click()
    except:
        print("\nFinished Scraping Jobs")
        break
    #print the page you're on 
    print("Page: {}".format(str(i+2)))

print("Scraping Job Descriptions...")
descriptions = []
for link in links:
    driver.get(link)
    job_description = driver.find_element_by_xpath('//div[@id="jobDescriptionText"]').text

    descriptions.append(job_description)

dataframe_da = pd.DataFrame()
dataframe_da['Title'] = titles
dataframe_da['Company'] = companies
dataframe_da['Location'] = "Toronto, Ontario"
dataframe_da['Link'] = links
dataframe_da['Review'] = reviews
dataframe_da['Salary'] = salaries
dataframe_da['Description'] = descriptions

#write data to an excel spreadsheet
writer = pd.ExcelWriter('output.xlsx')
dataframe_da.to_excel(writer, 'Jobs')

writer.save()
print("\nData written to an Excel Sheet")