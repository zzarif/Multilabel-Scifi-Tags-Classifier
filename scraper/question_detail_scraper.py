from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm
import pandas as pd


if __name__ == "__main__":
    question_data = []
    chrome_options = webdriver.ChromeOptions() # chrome options
    chrome_options.add_argument("--headless") # run in background
    chrome_options.add_argument("--window-size=1920,1080") # render full screen
    chrome_options.add_argument('log-level=3') # suppress verbose log messages

    df = pd.read_csv("data/question_urls.csv")
    question_urls = df["url"].to_list() # convert urls to iterable list
    
    # fetch details from each url
    for question_url in tqdm(question_urls[:4]):
        print(f"Scraping -> {question_url}")
        driver = webdriver.Chrome(options=chrome_options) # initialize driver
        driver.get(question_url)

        try:
            # scrape elements
            title = driver.find_element(By.ID, "question-header").text.split('\n')[0]
            description = driver.find_element(By.CLASS_NAME, "s-prose.js-post-body").text
            tags = [tag.text for tag in driver.find_element(By.CLASS_NAME, "post-taglist").find_elements(By.TAG_NAME, "li")]

            # append to data list
            question_data.append({
                "title": title,
                "url": question_url,
                "description": description,
                "tags": tags
            })

            # save the dataframe to csv
            df = pd.DataFrame(data=question_data, columns=question_data[0].keys())
            df.to_csv("data/question_details.csv", index=False)

        except NoSuchElementException:
            continue

        finally:
            # exit the driver
            driver.quit()
    