from requests import get
import pathlib
import logging
import json

config_path = str(pathlib.Path(__file__).parent.parent.resolve())+"\\config.json"
config = json.load(open(config_path, 'r'))

scheduler = None
del_sched = []
shown_articles = []
article_blacklist = []
articles_page = 1

def news_API_request(covid_terms = "Covid COVID-19 coronavirus"):
    """
    Sends a request to the news API to get the relevant articles relating to covid.

    Args:
        covid_terms (str): The search terms to use.
    
    Returns:
        json (json): Relevant articles.
    """
    response = get("https://newsapi.org/v2/everything?pageSize=100&page="+str(articles_page)+"&sortBy="+config["articles_sort"]+"&language="+config["articles_language"]+"&qInTitle="+covid_terms.replace(' ', " OR ")+"&apiKey="+config["api_key"])
    if response.status_code == 200:
        return response.json()
    else:
        logging.warning(f" newsapi.org [{response.status_code}] - {response.reason}")

def update_news(upd_name = None):
    """
    Updates the articles section of the interface.

    Args:
        upd_name (str): Title of update that triggered this function.
    
    Returns:
        None.
    """
    global del_sched, shown_articles, articles_page
    if upd_name != None:
        del_sched.append(upd_name)
    articles = news_API_request(config["search_terms"])
    if articles:
        shown_articles = []
        count = 0
        for art in articles["articles"]:
            full_title = f"[{art['source']['name']}] {art['title']} ({art['publishedAt'][:10]})"
            if not (full_title in article_blacklist):
                shown_articles.append({
                    "title": full_title,
                    "content": f"{art['description']} [{art['url']}]"
                })
                count += 1
            if count == config["max_articles"]:
                break
        if count == 0:
            articles_page += 1
            update_news()

def schedule_news_updates(update_interval, update_name):
    """
    Enters a schedule into the scheduler to update news data.

    Args:
        update_interval (int): Delay of when to trigger update.
        update_name (str): Title of update that will trigger the news data update.
    
    Returns:
        None.
    """
    if scheduler:
        scheduler.enter(update_interval, 1, update_news, (update_name,))
