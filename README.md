Scrapers for collecting content on different social media platforms! Please ensure you download all the packages listed at the top of the files. 

# Running IG
- Ensure that you have quit all chrome on your computer
- Update your computer's username (eg. when i open my terminal i see belle@Belles-Laptop-3 and my username is belle)
- Update the length of scroll
- run ig.py to get posts from searches
- run igHomePage.py to get posts from your homepage

# Youtube
- Ensure that you have quit all chrome on your computer
- How to run: put your queries in the queries.csv file
- Run `pytest -s --uc scraper.py`
- After youtube page loads, log in manually. After 60 seconds, page would automatically run your queries.
- You can find the scraped html pages inside `results`.
- If this doesn't work, update queries in and run using_api.py (this will use PyTube API instead of scraping)
