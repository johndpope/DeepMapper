import requests
from db import *
from bs4 import BeautifulSoup
import re

### CONFIG ###
site_base = "https://www.findchatfriends.com/find/snapchat-usernames"
site = "https://www.findchatfriends.com"
starting_page = 1
##############


def fetchPage(page):
    html_data = requests.get(site_base, params={"page": page}).text

    soup = BeautifulSoup(html_data, features="lxml")

    profiles = soup.find_all("div", class_="post")

    return profiles


def parsePage(page):
    output = []

    for profile in page:
        pf = {}
        profile = str(profile)
        soup = BeautifulSoup(profile, features="lxml")

        pf["gender"] = re.findall('data-gender="([f,m])"', profile)[0]
        photos = re.findall('url\((.*)\)"', profile)
        pf["profile_url"] = site + (photos[0] if len(photos) > 0 else "")
        # This ugly line deals with cross-encoding issues
        pf["age"] = int("0" + str(soup.find_all("div", class_="age")[0].encode_contents()).replace("\\n", "").strip().replace(" ", "").replace("yo", "").replace(
            "b", "").replace("'", "").split("<")[0])
        loc = re.findall('<div class="location">(.*)<\/div>', profile)
        pf["location"] = loc[0] if len(loc) > 0 else ""
        pf["username"] = re.findall(
            '<div class="username">(.*)<\/div>', profile)[0]
        bio = re.findall('<p class="about">(.*)<\/p>', profile)
        pf["bio"] = bio[0] if len(bio) > 0 else ""

        output.append(pf)

    return output


# page = fetchPage(200000000)
# print(parsePage(page))

successfull = True
curpage = starting_page
while successfull:
    page = fetchPage(curpage)

    # Check for invalid page
    try:
        users = parsePage(page)
    except Exception as e:
        successfull = False
        print(e)
        continue
    
    

    print(f"Parsed page: {curpage}")

    for user in users:
        print(f"Adding {user['username']} to DB")
        con.execute(tbl_users.insert().values(
            username=user["username"],
            age=user["age"],
            location=user["location"],
            sfw=False,
            bio=user["bio"],
            profile_url=user["profile_url"],
            gender=user["gender"]
        ))

    curpage += 1