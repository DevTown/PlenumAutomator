from etherpad_lite import EtherpadLiteClient
import datetime
import re
import os
import pdfkit
from mwclient import Site
import plenumconfig as cfg


def addToWiki(name, text):
    site = Site(cfg.wikiurl, path="/")
    site.login(cfg.wikiuser, cfg.wikipassword)
    page = site.pages[name]
    patternstart = r'<(a).*?>'
    result = re.sub(patternstart, "[[", text)

    patternend = r'<(/a).*?>'
    result = re.sub(patternend, "]]", result)
    page.save(text=result, summary="Neuanlage")


def makePDF(html, pdf):
    pdfkit.from_url(cfg.saveSpace + html, cfg.saveSpace + pdf)


def write_Plenum(name, html):
    with open(cfg.saveSpace + name + '.html', 'w') as f:
        f.write(html["html"])
    f.close()
    makePDF(name + ".html", name + ".pdf")


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)


def get_next_Plenum():
    today = datetime.date.today()
    first = today.replace(day=1, month=today.month + 1)
    return next_weekday(first, 2)


def get_last_Plenum():
    today = datetime.date.today()
    first = today.replace(day=1)
    return next_weekday(first, 2)


def main():
    c = EtherpadLiteClient(base_params={'apikey': cfg.myapikey}, base_url=cfg.mybaseURL)
    plenum = c.getHTML(padID=cfg.mypadID)
    filename = cfg.filePrefix + '_' + str(get_last_Plenum().strftime("%Y.%m.%d")).replace('.', '_')
    write_Plenum(filename, plenum)

    plenumwiki = str(plenum["html"]).replace("<!DOCTYPE HTML><html><body>", "").replace("</body></html>", "") + "[[Kategorie:" + cfg.wikiKategorie + "]]"
    wikiname = cfg.wikiwikiprefix + '_' + str(get_last_Plenum().strftime("%Y_%m"))
    addToWiki(wikiname, plenumwiki)

    c.setText(padID=cfg.mypadID, text='Plenum ' + str(get_next_Plenum().strftime("%Y.%m.%d")))


if __name__ == "__main__":
    main()
