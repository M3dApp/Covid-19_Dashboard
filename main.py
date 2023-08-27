from flask import Flask, request, render_template, redirect, request
from sys import path
import logging
import sched
import time
import json

path.append("modules")
logging.basicConfig(filename="sys.log", encoding="utf-8")

import covid_data_handler
import covid_news_handling
CDH = covid_data_handler
CNH = covid_news_handling

app = Flask(__name__)
config = json.load(open("config.json", 'r'))
scheduler = sched.scheduler(time.time, time.sleep)
CDH.scheduler = scheduler
CNH.scheduler = scheduler

scheduled_updates = []
reload_data = True
first_time = True

def calculate_time_diff(HHMM):
    """
    Calculates the difference in seconds between the current time and a set time.

    Args:
        HHMM (str): 24-hour clock time in HH:MM format (e.g. 21:00, 02:30, etc).
    
    Returns:
        None
    """
    local_time = time.localtime()
    time_set = (int(HHMM.split(':')[0]) * 3600) + (int(HHMM.split(':')[1]) * 60)
    time_now = (local_time.tm_hour * 3600) + (local_time.tm_min * 60) + local_time.tm_sec
    diff = time_set - time_now
    if diff <= 0:
        diff = (86400 - time_now) + time_set
    return diff

def update_schedule_ui(covid_sched, news_sched):
    """
    Updates the interface for the schedule list and enters new schedules into the scheduler if needed.

    Args:
        covid_sched (list): A list containing the titles of covid data updates that need to be removed/updated.
        news_sched (list): A list containing the titles of news data updates that need to be removed/updated.
    
    Returns:
        None
    """
    global scheduled_updates
    if len(covid_sched) > 0 or len(news_sched) > 0:
        new_sched_upds = []
        for upd in scheduled_updates:
            if upd["title"] in covid_sched or upd["title"] in news_sched:
                if "True" in upd["content"].split(" | ")[0]:
                    new_sched_upds.append(upd)
                    delay = calculate_time_diff(upd["title"].split(" @ ")[1])
                    if upd["title"] in covid_sched:
                        CDH.schedule_covid_updates(delay, upd["title"])
                    if upd["title"] in news_sched:
                        CNH.schedule_news_updates(delay, upd["title"])
            else:
                new_sched_upds.append(upd)
        scheduled_updates = new_sched_upds

@app.route('/')
def primary():
    global reload_data, first_time
    if reload_data or first_time:
        first_time = False
        CDH.update_covid_data()
        CNH.update_news()
    reload_data = True
    return index()

@app.route('/index')
def index():
    global reload_data
    scheduler.run(False)
    update_schedule_ui(CDH.del_sched, CNH.del_sched)
    CDH.del_sched = []
    CNH.del_sched = []
    if request.path == "/index":
        upd_time = request.args.get("update")
        upd_name = request.args.get("two")
        upd_rep = (request.args.get("repeat") and True) or False
        upd_covid = (request.args.get("covid-data") and True) or False
        upd_news = (request.args.get("news") and True) or False
        if upd_name:
            if upd_time and (upd_covid or upd_news):
                full_name = str(upd_name)+" @ "+str(upd_time)
                for upd in scheduled_updates:
                    if upd["title"] == full_name:
                        scheduled_updates.remove(upd)
                        break
                scheduled_updates.append({
                    "title": full_name,
                    "content": "Repeat: "+str(upd_rep)+" | Covid: "+str(upd_covid)+" | News: "+str(upd_news)
                })
                delay = calculate_time_diff(upd_time)
                if upd_covid:
                    CDH.schedule_covid_updates(delay, full_name)
                if upd_news:
                    CNH.schedule_news_updates(delay, full_name)
        del_upd = request.args.get("update_item")
        del_art = request.args.get("notif")
        if del_upd:
            for upd in scheduled_updates:
                if upd["title"] == del_upd:
                    scheduled_updates.remove(upd)
                    for s in scheduler.queue:
                        if s.argument[0] == upd["title"]:
                            scheduler.cancel(s)
                            break
                    break
        if del_art:
            for art in CNH.shown_articles:
                if art["title"] == del_art:
                    CNH.shown_articles.remove(art)
                    CNH.article_blacklist.append(del_art)
                    break
        reload_data = False
        return redirect('/')
    return render_template("index.html",
        favicon = f"\static\images\{config['favicon']}",
        title = config["title"],
        image = config["image"],
        location = config["local_location"],
        nation_location = config["national_location"],
        local_7day_infections = f"{CDH.local_last7days_cases:,}",
        national_7day_infections = f"{CDH.nation_last7days_cases:,}",
        hospital_cases = f"Hospital cases: {CDH.nation_hosp_cases:,}",
        deaths_total = f"Total deaths: {CDH.nation_deaths:,}",
        updates = scheduled_updates,
        news_articles = CNH.shown_articles,
    )

if __name__ == "__main__":
    app.run()
