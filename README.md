# StackExchange Scifi Tags Classifier
Classify relevant tags from StackExchange Scifi questions.

## Build from Source
1. Clone the repo
```bash
git clone https://github.com/zzarif/StackExchange-Scifi-Tags-Classifier.git
```
2. Initialize and activate virtual environment
```bash
virtualenv --no-site-packages venv
source venv/Scripts/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
*Note: Select virtual environment interpreter from* `Ctrl`+`Shift`+`P`

## Run the Selenium Scraper
```bash
python scraper/question_url_scraper.py
```
Wait for the script to finish (might take a few hours depending on your network bandwidth). When complete, this will generate [question_urls.csv](data/question_urls.csv) file. This file has **30,000** StackExchange Scifi question titles and URLs. Now, we need to fetch the question details (description, tags, etc.) for each of these question URLs.

## Fetch Question Details
Fetching details from **30,000** question URLs is a rather resource intensive task. To efficiently fetch the details we can either request the question details via Stack API (recommended) or we can scrape the details with selenium scraper. (There are other ways too as mentioned [here](https://stackoverflow.com/a/40017359/23817375).)

### Method 1: Request question details via [Stack API](https://api.stackexchange.com/)
This method explains Now that we have **30,000** Scifi question URLs, we need to fetch the details (description, tags, etc.) for each of the questions. For that, we will utilize StackExchange REST APIs for this purpose. To do so:
1. Register your v2.0 application at [Stackapps](https://stackapps.com/apps/oauth/register) to get an API key.
2. `deactivate` your active virtual environment.
3. Open your `venv/Scripts/activate` file and add this line at the end of file (replace `<your_api_key>` with the API key from Stackapps):
```bash
export STACK_API_KEY="<your_api_key>"
```

4. Activate the virtual environment again:
```bash
source venv/Scripts/activate
```
5. Now, run the question detail scraper:
```bash
python scraper/question_detail_scraper.py
```
Wait for the script to finish (might take a few hours depending on your network bandwidth). The script might get interrupted because the Stack API is [throttled](https://api.stackexchange.com/docs/throttle) to max 10,000 calls per day for registered apps and it only allows for only a limited number of calls within a timeframe. In that case, simply wait and re-run the script the next day and it will resume from where it got interrupted. When complete, this will generate [question_details.csv](data/question_details.csv) file. It has the details (title, url, description, tags) of **30,000** scifi and fantasy questions from StackExchange.

### Method 2: Fetch question details via Selenium Scraper
