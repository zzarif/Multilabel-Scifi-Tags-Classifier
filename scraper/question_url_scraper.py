from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
import pandas as pd


if __name__ == "__main__":
    question_urls = []
    chrome_options = webdriver.ChromeOptions() # chrome options
    chrome_options.add_argument("--headless") # run in background
    chrome_options.add_argument("--window-size=1920,1080") # render full screen
    chrome_options.add_argument('log-level=3') # suppress verbose log messages

    base_url = "https://scifi.stackexchange.com/questions?tab=votes&pagesize=50"

    # each page has max 50 urls
    # to fetch total 30K urls
    # iterate page by page from page 1 to 600
    for page_id in tqdm(range(1, 601)):
        driver = webdriver.Chrome(options=chrome_options) # initialize driver
        driver.get(f"{base_url}&page={page_id}")

        questions_container = driver.find_element(By.ID, "questions")
        rows = questions_container.find_elements(By.TAG_NAME, "h3")
        print(len(rows))
        for row in rows:
            url_tag = row.find_element(By.TAG_NAME,"a")
            question_title = url_tag.text
            question_url = url_tag.get_attribute("href")
            question_urls.append({
                "title": question_title,
                "url": question_url
            })
        # exit the driver
        driver.quit()
        # save the dataframe to csv
        df = pd.DataFrame(data=question_urls, columns=question_urls[0].keys())
        df.to_csv("data/question_urls.csv", index=False)