from newspaper import Article
import bs4
from bs4 import BeautifulSoup
from urlextract import URLExtract
import requests
import re 
from autolink import linkify
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

vaccine_terms = ["smallpox", "pertussis", "infect", "heart attack", "cancer", "diabetes", "shingles", "paralysis", "cervical cancer", 
"neurogenesis", "infectious disease", "brain", "asthma", "bowel disease", "kidney",
"encephalitis", "HOMEOPATHY", "parapertussis", "seizure", "allergies", "SIDS", "placebo", "Fatigue", "shingles", "lizard morphing", "behavior change",
"strains", "hippocampal neurogenesis", "antibiotics", "uillainBarreSyndrome", "pneumonia", "HPV", "shedding", "vaccin", "pertussis", 
"hepatitis", "polio","chickenpox", "measles", "HPV", "rotavirus", "flu", "DPT",
"MMR", "Tdap", "Hep B", "DTap", "NMDA", "HBV", "Krabbe", "Gardisil", "dog kidney cells", "chicken", "fetal", "babies",
"cancer", "tumor", "monkey", "rubella", "mumps", "MMR", "measles", "pentavalent", "live virus", "virus","infected", "exposure",
"aluminum", "mercury", "thimerosal", "fetal", "babies", "Autism", "Infant mortality", "bacteria"]

vaccine_terms = [item.casefold() for item in vaccine_terms]


def URL_rep(text): 
	url_info = dict()
	extractor = URLExtract()
	urls = extractor.find_urls(text)
	if not urls:
		return url_info
	count = 0
	for url in urls:
		url_org = url
		try:
			article = Article(url)
			response = requests.get(url, verify=False,timeout=20)
			if response.status_code != 200:
				raise Exception('---------')
		    
		except:
			temp_url = re.search('"(.*)"',linkify(url)).group(1)
			url = temp_url
			response = requests.get(url, verify=False,timeout=20)
			if response.status_code != 200:
				count += 1
				url_info[url_org] = "NA"
				continue

		try:
			article = Article(url)
			article.download()
			article.parse()
			title = "\n" + article.title + "\n" + article.text
			if not any(item for item in vaccine_terms if item in title.casefold()):
				title = 'NA'
			url_info[url_org] = title

		except Exception as e:
			html = response.content
			soup = BeautifulSoup(html, "html.parser") #features="lxml"
			matches = soup.findAll(['p','title'],text = True,limit=None)  #text = re.compile('vaccin')
			linkcontent = []
			for node in matches:
				if type(node) is bs4.element.Tag:
					linkcontent.append(node.get_text())
				else:
					linkcontent.append(node)
			if not linkcontent:
				title = 'NA'
			elif not any(item for item in vaccine_terms if item in " ".join(linkcontent).casefold()):
				title = 'NA'
			else:
				title = "\n" + " ".join(linkcontent)
			
			url_info[url_org] = title

	return url_info
