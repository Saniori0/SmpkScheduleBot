import json

import re
import requests
from bs4 import BeautifulSoup

from config import redis, WEEK_DAYS_REGEXP


def getBeautifulSoupForHtml(html: str):
    return BeautifulSoup(html, features="html.parser")


def getBeautifulSoupForPage(page: str):
    request = requests.get(f"{page}")

    html = request.content

    return getBeautifulSoupForHtml(html)


def parseGroupSchedule(mainPage: str) -> dict:
    groupParsed = getBeautifulSoupForPage(f"https://rasp.mirsmpc.ru/{mainPage}")

    groupSchedule = {}

    table = groupParsed.find("table", attrs={
        "class": "inf"
    })

    rows = table.find_all("tr")

    weekDay = ""

    for rowIndex, row in enumerate(rows):

        if rowIndex < 3: continue

        columns = row.find_all("td")
        columnsLen = len(columns)

        if columnsLen < 2: continue

        if len(columns[0].text) != 1:
            weekDay = columns[0].text
            groupSchedule[weekDay] = {}
            lessonNum = int(columns[1].text) if columns[1].text.isdigit() else 0

        if len(columns[0].text) == 1:
            lessonNum = int(columns[0].text)

        groupSchedule[weekDay][lessonNum] = []

        lessons = row.find_all("td", attrs={"nowrap": True})

        for lesson in lessons:
            if lesson.text == "\xa0":
                groupSchedule[weekDay][lessonNum].append({
                    "name": "Нет пары",
                    "cab": 0,
                    "teacher": 0,
                })
                continue

            lessonOptions = lesson.find_all("a")
            groupSchedule[weekDay][lessonNum].append({
                "name": lessonOptions[0].text,
                "cab": lessonOptions[1].text,
                "teacher": lessonOptions[2].text,
            })

    return groupSchedule


def parseGroups() -> dict:
    groupsParsed = getBeautifulSoupForPage("https://rasp.mirsmpc.ru/hg.htm")

    groupsTagsA = groupsParsed.find_all("a", attrs={
        "class": "hd",
        "title": "Текущее расписание на неделю"
    })

    groups = {
        groupTagA.text: {
            "mainPage": groupTagA.attrs["href"],
            "schedule": parseGroupSchedule(groupTagA.attrs["href"])
        }
        for groupTagA in groupsTagsA
    }

    return groups


def getGroupsFromRedis() -> dict:
    groups = redis.get("groups")

    return json.loads(groups) if groups else {}


def getGroups() -> dict:
    groups = getGroupsFromRedis()

    groupsQuantity = len(groups)

    if groupsQuantity == 0:
        groups = parseGroups()

        redis.set("groups", json.dumps(groups))

        redis.expire("groups", 3600)

    return groups


def getGroup(groupName: str) -> dict:
    group = getGroups()[groupName]

    return group
