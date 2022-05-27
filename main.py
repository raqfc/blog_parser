# This is a sample Python script.
import json
import os
import re
import shutil
import time

import unidecode
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def parseFile(path):
    s = Service(cromeDriverPath)
    driver = webdriver.Chrome(service=s)

    driver.get('https://www.prowaretech.com/articles/current/tools/convert-html-to-json')
    time.sleep(1)
    driver.execute_script("closeCookies()")
    time.sleep(1)

    search_box = driver.find_element(by=By.NAME, value='html')
    btn_submit = driver.find_element(by=By.NAME, value='submit')
    pretty_json_box = driver.find_element(by=By.ID, value='pretty')

    search_box.clear()

    htmlFile = ""
    for file_name in os.listdir(path):
        # construct full file path
        source = path + file_name
        # copy only files
        filename, file_extension = os.path.splitext(source)
        if file_extension == ".html":
            htmlFile = getHtmlFile(source)
            break



    soup = BeautifulSoup(htmlFile, 'html.parser')
    htmlContent = soup.find_all("div", {"class": "content-inner"})[0]
    htmlContent.attrs['class'] = "post-content"
    replacedHtmlContentString = str(htmlContent)

    search_box.send_keys(replacedHtmlContentString)
    time.sleep(1)
    btn_submit.click()
    time.sleep(1)
    jsonContent = json.loads(pretty_json_box.get_attribute("value"))

    data = {
        "id": "1",
        "active": True,
        "publishable": True,
        "createdBy": "Volan",
        "createdEnv": "WEB",
        "authors": [{
            "name": "Volan",
            "image": {
                "src": "/brand/volan-logo-dark.png",
                "alt": "volan logo avatar",
                "prefix": "images",
                "format": "png"
            }
        }],
    }

    search_box.clear()
    oldImgPath = None
    for meta in soup("meta"):
        if meta.attrs.get('property') is not None:
            if meta.attrs['property'] == 'og:description':
                data["abstract"] = meta.attrs['content']
            elif meta.attrs['property'] == 'og:title':
                data["title"] = meta.attrs['content']
                data["slug"] = unidecode.unidecode(re.sub("(\s)", "-", meta.attrs['content']).lower())
            elif meta.attrs['property'] == 'og:type':
                data["category"] = meta.attrs['content']
            elif meta.attrs['property'] == 'article:published_time':
                data["createdAt"] = meta.attrs['content']
            elif meta.attrs['property'] == 'article:modified_time':
                data["updatedAt"] = meta.attrs['content']
            elif meta.attrs['property'] == 'og:image':
                oldImgPath = meta.attrs['content']

        search_box.send_keys(str(meta))
        meta.decompose()
        time.sleep(1)
        btn_submit.click()
        time.sleep(1)

    metasJson = json.loads(pretty_json_box.get_attribute("value"))

    prefixYear = '0'
    prefixMonth = '0'
    if data.get("slug") is not None and oldImgPath is not None:
        splitted = oldImgPath.split("/")
        year = splitted[5]
        month = splitted[6]
        imgExtention = splitted[7].split(".")[-1]
        img = soup.find_all("span", {"class": "post-featured-img"})[0].findChildren("img")[0]
        data["image"] = {
                            "src": "blogs/" + year + "/" + month + "/" + data["slug"] + "." + imgExtention,
                            "alt": img.alt,
                            "format": imgExtention
                        },
        prefixYear = year
        prefixMonth = month
        data["prefix"] = str(year + "/" + month),

    toc = []

    titleIndex = 0
    subtitleIndex = 1
    for child in htmlContent.findChildren():
        if child.name == "h2":
            titleIndex += 1
            subtitleIndex = 1
            toc.append(
                {
                    "id": "title#" + str(titleIndex),
                    "label": child.text
                }
            )
        elif child.name == "h3":
            toc.append(
                {
                    "id": "subtitle#" + str(titleIndex) + "." + str(subtitleIndex),
                    "label": child.text,
                    "depth": 3
                }
            )
            subtitleIndex += 1

    data["seo"] = {
        "meta": metasJson
    }

    data["toc"] = toc
    data["document"] = replacedHtmlContentString
    data["body"] = jsonContent

    # escrevendo resultado
    savePath = baseSavePath + prefixYear + "/" + prefixMonth + "/" + data["slug"] + "/"

    for file_name in os.listdir(path):
        source = path + file_name
        if os.path.isdir(source):
            shutil.copytree(source, savePath + "files")
            break

    os.makedirs(os.path.dirname(savePath), exist_ok=True)
    with open(savePath + 'seo.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False)
    with open(savePath + 'post_content.html', 'w') as f:
        json.dump(replacedHtmlContentString, f, ensure_ascii=False)

    driver.quit()


def getHtmlFile(path):
    f = open(path, "r")
    read = f.read()
    f.close()
    return read


baseSourcePath = "/Users/raquelfreire/Desktop/blogs2/"
baseSavePath = "/Users/raquelfreire/Desktop/parsedBlogs/"
cromeDriverPath = "/Users/raquelfreire/Documents/chromedriver"

if __name__ == '__main__':
    # andar por todas as pastas do baseSourcePath
    for file_name in os.listdir(baseSourcePath):
        if os.path.isdir(baseSourcePath + file_name):
            dirPath = baseSourcePath + file_name + "/"
            try:
                print("parsing" + dirPath)
                parseFile(dirPath)
            except Exception as e:
                print("error parsing " + dirPath)
                print(e)
