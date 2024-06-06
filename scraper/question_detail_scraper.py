import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import os


## stack API Creds
STACK_API_ENDPOINT = "https://api.stackexchange.com/2.3/questions"
API_KEY = os.environ['STACK_API_KEY']
SITE = "scifi"


if __name__ == "__main__":
    qdf = pd.read_csv("data/question_urls.csv")
    question_urls = qdf["url"].to_list()  # convert urls to iterable list

    # Load existing data from the CSV file
    if os.path.exists("data/question_details.csv"):
        df = pd.read_csv("data/question_details.csv")
        question_data = df.to_dict(orient="records")
        last_processed_index = len(question_data)
    else:
        question_data = []
        last_processed_index = 0

    for i in tqdm(range(last_processed_index, len(question_urls))):
        question_url = question_urls[i]

        # Extract the question ID from the URL
        question_id = question_url.split("/")[-2]

        api_endpoint = f"{STACK_API_ENDPOINT}/{question_id}"
        params = {
            "filter": "withbody",
            "key": API_KEY,
            "site": SITE,
        }

        # Make a GET request to the API
        response = requests.get(api_endpoint, params=params)
        data = response.json()

        if "items" in data:
            item = data["items"][0]
            title = item["title"]
            body = BeautifulSoup(item["body"], "html.parser").get_text()
            tags = item["tags"]

            # Append to data list
            question_data.append({
                "title": title,
                "url": question_url,
                "description": body,
                "tags": tags
            })

            # Save the dataframe to CSV
            df = pd.DataFrame(data=question_data, columns=question_data[0].keys())
            df.to_csv("data/question_details.csv", index=False)
            time.sleep(1)

        # Check remaining quota of the day
        if "quota_remaining" in data and data["quota_remaining"] == 0:
            print(f"Quota limit reached. Processed {i+1} out of {len(question_urls)} URLs.")
            break  # max API request limit (10K) reached