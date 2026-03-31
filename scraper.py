#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
from bs4 import BeautifulSoup
from db import supabase


def scrape_toto_latest():

    url = "https://en.lottolyzer.com/history/singapore/toto?page=1"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.select("table tbody tr")

    draws = []

    for row in rows:
        cols = row.find_all("td")

        if len(cols) >= 4:
            draw_no = int(cols[0].text.strip())
            draw_date = cols[1].text.strip()
            winning_no = cols[2].text.strip()
            additional_no = cols[3].text.strip()

            draws.append({
                "draw_no": draw_no,
                "draw_date": draw_date,
                "winning_no": winning_no,
                "additional_no": int(additional_no)
            })

    return draws


def update_supabase(draws):

    for draw in draws:
        supabase.table("toto_results").upsert(draw, on_conflict="draw_no").execute()

