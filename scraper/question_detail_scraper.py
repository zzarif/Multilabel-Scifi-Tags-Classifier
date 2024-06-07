import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import pandas as pd
from tqdm import tqdm
import time

def scrape_question(question_url):
    chrome_options = webdriver.ChromeOptions()  # chrome options
    chrome_options.add_argument("--headless")  # run in background
    chrome_options.add_argument("--window-size=1920,1080")  # render full screen
    chrome_options.add_argument('log-level=3')  # suppress verbose log messages

    driver = webdriver.Chrome(options=chrome_options)  # initialize driver
    driver.get(question_url)

    try:
        # scrape elements
        title = driver.find_element(By.ID, "question-header").text.split('\n')[0]
        description = driver.find_element(By.CLASS_NAME, "s-prose.js-post-body").text
        tags = [tag.text for tag in driver.find_element(By.CLASS_NAME, "post-taglist").find_elements(By.TAG_NAME, "li")]

        # return the scraped data
        return {
            "title": title,
            "url": question_url,
            "description": description,
            "tags": tags
        }

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error occurred while scraping {question_url}: {str(e)}")
        return None

    finally:
        # exit the driver
        driver.quit()
        time.sleep(5)

def scrape_chunk(chunk, chunk_id):
    question_data = []
    for question_url in tqdm(chunk, desc=f"Chunk {chunk_id}"):
        data = scrape_question(question_url)
        if data:
            question_data.append(data)

    # save the dataframe to csv for the current chunk
    df = pd.DataFrame(data=question_data, columns=question_data[0].keys())
    df.to_csv(f"data/question_details_chunk{chunk_id}.csv", index=False)

if __name__ == "__main__":
    df = pd.read_csv("data/question_urls.csv")
    question_urls = df["url"].to_list()  # convert urls to iterable list

    num_processes = multiprocessing.cpu_count()  # get the number of CPU cores
    chunk_size = len(question_urls) // num_processes  # calculate the chunk size

    # divide the question_urls into chunks
    chunks = [question_urls[i:i + chunk_size] for i in range(0, len(question_urls), chunk_size)]

    # create a process for each chunk
    processes = []
    for i, chunk in enumerate(chunks):
        process = multiprocessing.Process(target=scrape_chunk, args=(chunk, i))
        processes.append(process)
        process.start()

    # wait for all processes to finish
    for process in processes:
        process.join()