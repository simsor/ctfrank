#!/usr/bin/env python3

from flask import Flask, render_template
from ctfrank import CTF
import json

app = Flask(__name__)

ctfs_list = [
    ["AlexCTF", "https://ctf.oddcoder.com/"],
    ["BITSCTF", "https://bitsctf.bits-quark.org"]
]

@app.route("/")
def index():
    ctfs = []
    for ctf in ctfs_list:
        ctfs.append(ctf[0])

    return render_template("index.html", ctfs=ctfs, round=round)


@app.route("/getctf/<ctfname>")
def getctf(ctfname):
    ctf = None
    team = None
    for c in ctfs_list:
        if c[0] == ctfname:
            ctf = CTF(c[1])
            team = ctf.get_team("Cryptis")
            break
    if not ctf:
        return "no ctf by that name"
    
    return json.dumps({
        "title": ctf.title,
        "team": {
            "url": team.url,
            "points": team.points,
            "rank": team.rank,
            "total": team.total,
            "percentile": round(team.percentile, 1)
        }
    })

if __name__ == "__main__":
    app.run()
