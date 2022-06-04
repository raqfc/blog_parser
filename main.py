# This is a sample Python script.
import json
import os
import re
import shutil
import time
import traceback

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

category1Titles = [
    "Como otimizar o registro de atendimento ao paciente? Confira 4 dicas!",
    "Qual é a importância e como fazer a avaliação de atendimento em anestesia?",
    "5 passos para otimizar o uso de indicadores na gestão de um centro cirúrgico",
    "Controle de produção em empresas de anestesia: entenda o que é e como otimizar",
    "5 erros comuns ao acompanhar indicadores em serviços de anestesiologia",
    "Como fazer uma boa gestão de dados e informações na saúde?",
    "Sistema de gerenciamento de processos: por que adotar um na sua unidade?",
    "Empresa de anestesia: como tornar a troca de plantão mais eficiente?",
    "Você sabe como colocar em prática o controle de processos na sua empresa de anestesia?",
    "Rotinas em anestesiologia: principais problemas e como evitá-los",
    "Como aumentar a produtividade da equipe de anestesistas",
]
category1 = "Controle de processos"

category2Titles = [
    "5 desafios da adoção de um aplicativo de escalas de trabalho e como superá-los",
    "Como o aplicativo de escala de plantão acelera a transformação digital na saúde?",
    "Como fazer uma escala de trabalho adequada à legislação na sua empresa de anestesia?",
    "5 erros que afetam a gestão de escalas de anestesistas",
    "7 razões para contar com um aplicativo de escalas de trabalho para anestesistas",
    "5 dicas de como montar escalas de trabalho produtivas",
]

category2 = "Gestão de Escalas"

category3Titles = [
    "Gestão financeira para médicos: 5 dicas para otimizar",
    "Principais indicadores de desempenho financeiro para a área da saúde",
    "3 dicas de como fazer uma redução de custos operacionais na saúde",
    "Principais técnicas de faturamento e auditoria de contas médicas para aplicar na sua instituição",
    "Como aumentar o faturamento da empresa de anestesia?",
    "Planilha financeira empresarial: como fazer o acompanhamento com o apoio da tecnologia?",
    "Gestão administrativa e financeira: 7 passos para otimizar esse processo em instituições de saúde",
    "Como o sistema de gestão para médico ajuda a reduzir custos em sua empresa de anestesia?",
    "Por que otimizar o controle de faturamento médico?",
    "Como o sistema de faturamento facilita o controle de empresas de anestesia?",
    "Erros na gestão de faturamento em empresas de anestesia que você deve evitar",
    "Como fazer o faturamento de contas médicas?",
    "Planilha de controle financeiro empresarial: por que não usar",
    "Gestão de dados e informação na saúde: tudo o que você precisa saber!",
    "Como melhorar os processos de faturamento no setor da saúde",
]

category3 = "Gestão Administrativa e Financeira"

category4Titles = [
    "Sistema de gestão ou planilha de controle de glosas: qual escolher?",
    "Indicadores de glosas hospitalares: veja quais são e como acompanhar",
    "5 dicas para melhorar a gestão de glosas",
]

category4 = "Gestão de glosas"

category5Titles = [
    "Por que a gestão de qualidade aumenta a eficiência da equipe de anestesia?",
    "Gestão inteligente: 4 vantagens de adotar este sistema",
    "Principais indicadores de qualidade hospitalar que você precisa conhecer",
    "Quais são os impactos da gestão de produtividade em instituições de saúde?",
    "5 erros que atrapalham a gestão de desempenho de grupos e empresas de anestesia",
    "Quais são os pilares da gestão de qualidade em saúde e como otimizar?",
    "Atendimento humanizado: Importância e como adotar no seu grupo de anestesia?",
    "O que é a gestão de atendimento e como implementar na saúde?",
    "Empresas de anestesia: principais impactos da transformação digital na saúde",
    "Tudo o que você precisa saber sobre o sistema de gestão da qualidade (SGQ)",
    "Como realizar a gestão do tempo e produtividade em instituições da saúde?",
    "Gestão inteligente na saúde: como realizar um gerenciamento baseado em dados?",
    "Qual o papel da tecnologia na área da saúde e como adotar?",
    "Importância da gestão de desempenho nas instituições de saúde",
    "Passo a passo para atingir eficiência operacional em empresas de anestesia",
    "Como garantir a gestão de qualidade nas empresas de anestesiologia?",
    "Experiência do paciente: entenda a importância e como garantir uma vivência positiva",
    "6 benefícios de adotar novas tecnologias na área da saúde para anestesiologistas",
]

category5 = "Gestão de qualidade"

category6Titles = [
    "Indicadores de segurança do paciente: o que são e importância para empresas de anestesia?",
    "6 Impactos da transformação digital na área da saúde",
    "O que é inteligência de dados e como implementar esse processo na saúde?",
    "Entenda o que é saúde 4.0 e por que adotar na sua empresa de anestesia",
    "Saúde baseada em valor: o que é e por que valorizar na sua empresa de anestesia?",
    "Modelo de troca de plantão: como automatizar esse processo?",
    "Qual é a importância da avaliação pré-anestésica e como otimizar com tecnologia?",
    "5 razões para implementar um software de gestão para médicos",
    "O que é gestão da informação em uma instituição de saúde?",
    "5 erros comuns ao acompanhar indicadores em serviços de anestesiologia",
    "Qual é a importância da avaliação pré-anestésica e como otimizar com tecnologia?",
    "5 razões para implementar um software de gestão para médicos",
    "O que é gestão da informação em uma instituição de saúde?",
    "5 erros comuns ao acompanhar indicadores em serviços de anestesiologia",
    "Qual a importância da eficiência operacional na saúde?",
    "Jornada do paciente: tudo sobre este conceito",
    "Entenda porque uma cooperativa de anestesista é importante",
    "3 dicas de como melhorar a sua produtividade em anestesiologia",
    "Benefícios do atendimento humanizado em seu grupo de anestesia",
    "Como o índice de eficiência operacional pode ajudar na área da saúde?",
    "Empresa e grupo de anestesia: como cuidar da saúde mental dos médicos?",
    "Entenda o que são as cooperativas médicas e como otimizá-las com tecnologia",
    "7 dicas para otimizar as rotinas em anestesiologia",
    "4 passos para fazer a gestão de ficha anestésica",
    "6 benefícios da gestão de dados e informação para empresas de anestesia",
    "Gestão de equipes de anestesia: 5 desafios e como superá-los",
    "LGPD na saúde: impactos e como se adequar à nova lei de proteção de dados?",
    "4 mitos da gestão de tempo e produtividade de empresas de anestesia",
    "5 segredos de como aumentar a produtividade das equipes de anestesia",
    "Pilares da experiência do paciente: o que considerar na sua empresa de anestesia?",
    "5 desafios na adoção de um sistema de gestão em empresas de anestesia",
    "Transformação digital no seu grupo de anestesia: 7 dicas para implementar",
    "Como escolher um sistema de gestão para empresas de anestesia?",
    "6 indicadores que todo médico anestesista deveria acompanhar",
    "Como otimizar a gestão de ficha de anestesia eletrônica",
    "10 vantagens de um sistema de gestão empresarial específico para grupo de anestesia",
]

category6 = "Gestão de empresas médicas"

def parseFile(path, blogId):
    s = Service(cromeDriverPath)
    driver = webdriver.Chrome(service=s)

    driver.get('https://www.prowaretech.com/articles/current/tools/convert-html-to-json')
    time.sleep(1)
    driver.execute_script("closeCookies()")
    time.sleep(2)

    search_box = driver.find_element(by=By.NAME, value='html')
    btn_submit = driver.find_element(by=By.NAME, value='submit')
    pretty_json_box = driver.find_element(by=By.ID, value='pretty')

    search_box.clear()

    htmlFile = ""
    htmlFileName = ""
    for file_name in os.listdir(path):
        # construct full file path
        source = path + file_name
        # copy only files
        file_extension = os.path.splitext(source)[1]
        if file_extension == ".html":
            htmlFileName = file_name
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
        "id": str(blogId),
        "active": True,
        "publishable": True,
        "createdBy": "Volan",
        "createdEnv": "WEB",
        "relatedPosts": [],
        "links": [],
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

    for aTag in htmlContent.find_all("a"):
        if re.search("https://volan.app.br/.+", aTag.attrs["href"]):
            data["links"].append({
                "link": aTag.attrs["href"],
                "label": aTag.findChildren()[0].text if aTag.findChildren() else ""
            })

    relatedPostsDiv = soup.find_all("div", {"class": "related-posts"})[0]

    search_box.clear()
    oldImgPath = None
    metasString = ""

    prefixYear = '2021'
    prefixMonth = '0'

    for meta in soup("meta"):
        if meta.attrs.get('property') is not None:
            if meta.attrs['property'] == 'og:description':
                data["abstract"] = meta.attrs['content']
            elif meta.attrs['property'] == 'og:title':
                data["title"] = meta.attrs['content']
            elif meta.attrs['property'] == "og:url":
                splittedBlogUrl = list(filter(None, meta.attrs['content'].split("/")))
                isMonth = False
                for part in splittedBlogUrl:
                    if part == prefixYear:
                        isMonth = True
                    elif isMonth:
                        prefixMonth = part
                        break
                data["slug"] = splittedBlogUrl[-1]
            elif meta.attrs['property'] == 'og:type':
                data["category"] = meta.attrs['content']
            elif meta.attrs['property'] == 'article:published_time':
                data["createdAt"] = meta.attrs['content']
            elif meta.attrs['property'] == 'article:modified_time':
                data["updatedAt"] = meta.attrs['content']
            elif meta.attrs['property'] == 'og:image':
                oldImgPath = meta.attrs['content']

        metasString = metasString + str(meta)
        meta.decompose()

    search_box.send_keys(str(metasString))
    time.sleep(1)
    btn_submit.click()
    time.sleep(1)
    metasJson = json.loads(pretty_json_box.get_attribute("value"))

    imageFileName = ""
    if oldImgPath is not None:
        splitted = oldImgPath.split("/")

        year = '2021'
        month = '01'

        isMonth = False
        for part in splitted:
            if part == '2021':
                isMonth = True
            elif isMonth:
                month = part
                break

        fileName = splitted[-1]

        imgExtention = fileName.split(".")[-1]
        imageFileName = fileName
        img = soup.find_all("span", {"class": "post-featured-img"})[0].findChildren("img")[0]
        data["image"] = {
            "src": "blogs/" + year + "/" + month + "/" + fileName,
            "alt": img["alt"],
            "format": imgExtention
        }

    splittedCreatedAt = data["createdAt"].split('-')
    data["createdPrefix"] = str(splittedCreatedAt[0] + "/" + splittedCreatedAt[1])

    # trying to find blog category
    if data["title"] in category1Titles:
        data["category"] = category1
    elif data["title"] in category2Titles:
        data["category"] = category2
    elif data["title"] in category3Titles:
        data["category"] = category3
    elif data["title"] in category4Titles:
        data["category"] = category4
    elif data["title"] in category5Titles:
        data["category"] = category5
    elif data["title"] in category6Titles:
        data["category"] = category6

    # relatedPosts
    for div in relatedPostsDiv.findChildren("div", {"class": "post"}):
        a = div.findChildren("a", {"class": "img-link"})[0]
        h3 = div.findChildren("h3", {"class": "title"})[0]
        # img = a.findChildren("img")[0]

        data["relatedPosts"].append({
            "title": h3.text,
            "link": a.attrs["href"],
            # "image": {
            #     "src": "blogs/" + year + "/" + month + "/" + fileName + "/realatedImages/" + imageFileName,
            #     "alt": img["alt"],
            #     "prefix": "images",
            #     "format": "png"
            # },
        })

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

    os.makedirs(os.path.dirname(savePath), exist_ok=True)
    with open(savePath + data["slug"] + '.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False)

    for fileName in os.listdir(path):
        source = path + fileName
        if os.path.isdir(source):
            shutil.copytree(source, savePath + "files")

            for innerFileName in os.listdir(source):
                if innerFileName == imageFileName:
                    shutil.copy(source + "/" + innerFileName, savePath)
                    break
            break

    with open(savePath + '/files/' + htmlFileName, 'w') as f:
        f.write(htmlFile)
        # json.dump(replacedHtmlContentString, f, ensure_ascii=False)

    driver.quit()


def getHtmlFile(path):
    f = open(path, "r")
    read = f.read()
    f.close()
    return read


baseSourcePath = "/Users/raquelfreire/Documents/landingpage_blogs/v2/allBlogs/"
baseSavePath = "/Users/raquelfreire/Documents/landingpage_blogs/v3/parsedBlogs/"
# baseSourcePath = "/Users/raquelfreire/Desktop/blogs2/"
# baseSavePath = "/Users/raquelfreire/Desktop/parsedBlogs/"
cromeDriverPath = "/Users/raquelfreire/Documents/chromedriver"

if __name__ == '__main__':
    blogId = 1
    # andar por todas as pastas do baseSourcePath
    for file_name in reversed(os.listdir(baseSourcePath)):
        if os.path.isdir(baseSourcePath + file_name):
            dirPath = baseSourcePath + file_name + "/"
            try:
                print("parsing " + dirPath + " blogId = " + blogId)
                parseFile(dirPath, blogId)
                blogId = blogId + 1
            except Exception as e:
                print("error parsing " + dirPath)
                print(e)
                traceback.print_exc()
