#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup


class CTFTeam:

    def __init__(self, name, url, points, rank, total):
        self.name = name
        self.url = url
        self.points = points
        self.rank = rank
        self.total = total

        self.percentile = (rank / total) * 100

    def __str__(self):
        return "CTFTeam<%s, %d points, %d/%d>" % (self.name, self.points, self.rank, self.total)


class CTF:
    """
    A CTF website

    You just have to pass the base url to the constructor and it will retrieve all the teams and their rank
    It only works for CTFd-based websites
    """

    def __init__(self, base_url):
        self.base_url = base_url
        self.title = "N/A"
        self.teams = []
        self._load()

    def _load(self):
        r = requests.get(self.base_url + "/scoreboard")
        html = r.text
        soup = BeautifulSoup(html, "html.parser")

        self.title = soup.title.string

        teams_table = soup.table
        rows = teams_table.find_all("tr")[1:]

        for row in rows:
            name = row.find("a").string
            url = self.base_url + row.find("a")["href"]
            points = int(row.find_all("td")[2].string)
            rank = int(row.find_all("td")[0].string)
            self.teams.append(CTFTeam(name, url, points, rank, len(rows)))

    def get_team(self, name):
        for t in self.teams:
            if t.name == name:
                return t
        return None


if __name__ == "__main__":
    bitctf = CTF("https://ctf.oddcoder.com/")

    team = bitctf.get_team("Cryptis")

    print("Top %.2f percent" % (team.percentile))
