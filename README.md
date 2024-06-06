# StackExchange Scifi Tags Classifier
Classify relevant tags from StackExchange Scifi questions.

## Build from Source
1. Clone the repo
```bash
git clone https://github.com/zzarif/Industry-Market-Cap-Analysis.git
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
This will generate [question_urls.csv](data/question_urls.csv) file. This file has 30,000 StackExchange Scifi question URLs.

## Fetch Question Details via [Stack API](https://api.stackexchange.com/)
Now that we have 30K Scifi questions, we need to fetch the details (description, tags, etc.) for each of the questions. For that, we will request REST APIs provided by StackExchange for this purpose. To do so:
1. Register your v2.0 application at [Stackapps](https://stackapps.com/apps/oauth/register) to get an API key.
2. Now, `deactivate` your active virtual environment.
3. Open your `venv/Scripts/activate` file and add this line at the end of file:
```bash
export STACK_API_KEY="<your_api_key>"
```
*Copy the API key from Stackapps and paste it in this line.*
4. Activate the virtual environment again:
```bash
source venv/Scripts/activate
```
5. Now, run the question detail scraper:
```bash
python scraper/question_detail_scraper.py
```
This will generate [question_details.csv](data/question_details.csv) file. It has the details (title, url, description, tags) of 30,000 scifi and fantasy questions from StackExchange.
*Registering an app gives us an API key which allows us to make 10,000 requests per day to Stack API. Here, we added this API key as an environment variable.*