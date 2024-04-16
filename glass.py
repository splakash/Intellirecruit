import requests
from bs4 import BeautifulSoup
import csv
import time
from selenium import webdriver
from selenium.webdriver import Keys
import pandas as pd
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
import requests

def scrape_glassdoor_jobs(job_title,location):
        job_data = []
        driver = webdriver.Chrome()
        driver.get("https://www.glassdoor.co.in/Job/index.htm")
        driver.maximize_window()
        get_source = driver.page_source
        soup = BeautifulSoup(get_source, "html.parser")
        search = driver.find_element(By.CSS_SELECTOR, '[class="Autocomplete_autocompleteInput__Ngcdi Autocomplete_roundLeftBorder__NBhQ9"]')
        loc=driver.find_element(By.CSS_SELECTOR,'[class="Autocomplete_autocompleteInput__Ngcdi Autocomplete_roundRightBorder__OybBh"]')
        search.send_keys(job_title)
        loc.send_keys(location)
        search.send_keys(Keys.ENTER)
        time.sleep(5)

        button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="load-more"]')))
        button.click()

        close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "CloseButton"))
        )
        close_button.click()

        time.sleep(2)

        for i in range(10):
                 WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test="load-more"]'))).click()
                 time.sleep(5)



        time.sleep(4)
        job_listings = driver.find_elements(By.CSS_SELECTOR, '[class="JobsList_jobListItem__wjTHv"]')

        for job in job_listings:
                job_title_elem = job.find_element(By.CSS_SELECTOR, '[class="JobCard_jobTitle___7I6y"]')

                company_elem = job.find_element(By.CSS_SELECTOR, '[class="EmployerProfile_compactEmployerName__LE242"]')

                location_elem = job.find_element(By.CSS_SELECTOR, '[class="JobCard_location__rCz3x"]')

                link=job.find_element(By.CSS_SELECTOR,'[class="JobCard_trackingLink__GrRYn"]')
                applly=link.get_attribute("href")

                job_title = job_title_elem.text.strip() if job_title_elem else "N/A"
                company = company_elem.text.strip() if company_elem else "N/A"
                location = location_elem.text.strip() if location_elem else "N/A"

                #job_description = job_description_elem.text.strip() if job_description_elem else "N/A"
                try:
                        salary_elem = job.find_element(By.CLASS_NAME, "JobCard_salaryEstimate__arV5J")
                        salary = salary_elem.text.strip().split(" (")[0]
                except NoSuchElementException:
                        salary = "N/A"
                job_data.append({
                        "Job Title": job_title,
                        "Company": company,
                        "Location": location,
                        "Salary": salary,
                        "Apply Link": applly,
                        #"Job Description": job_description_elem
                })
        return job_data


def save_to_csv(job_data, filename):
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["Job Title", "Company", "Location", "Salary", "Apply Link"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for job in job_data:
                        writer.writerow(job)

# Example usage:
job_title = "data analyst"
location = "india"
num_pages = 3  # Number of pages to scrape
filename = "glassdoor4_jobs.csv"

job_data = scrape_glassdoor_jobs(job_title,location)
save_to_csv(job_data, filename)


