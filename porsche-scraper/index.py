import requests
from bs4 import BeautifulSoup

def remove_umlaut(string):
    umlaut_mapping = {
        'ü': 'ue', 'Ü': 'Ue', 'ä': 'ae', 'Ä': 'Ae',
        'ö': 'oe', 'Ö': 'Oe', 'ß': 'ss'
    }
    for umlaut, replacement in umlaut_mapping.items():
        string = string.replace(umlaut, replacement)
    return string

url_paths = {
    "connect": "connect",
    "e-mobility": "e-mobility",
    "my-porsche": "my-porsche"
}

def question_and_links(url):
    resp = requests.get(url)
    resp.encoding = resp.apparent_encoding
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    questions = []
    for link in soup.find_all('a', href=True):
        text = link.text.strip()
        href = link['href']
        if text and "Mehr erfahren" in text:
            questions.append((text.replace("Mehr erfahren", "").strip(), href))
    
    return questions

def get_full_answer(url):
    resp = requests.get(url)
    resp.encoding = resp.apparent_encoding
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    article = soup.find('main', {'class': 'pcom-main'})
    if article:
        return article.get_text(separator=' ', strip=True)
    return "Keine Antwort gefunden"

def scrapeData(url, output_file):
    questions_and_links = question_and_links(url)
    QUESTION_URL = "https://ask.porsche.com"
    
    with open(output_file, "w", encoding="utf-8") as file:
        for question, link in questions_and_links:
            full_url = QUESTION_URL + link
            answer = get_full_answer(full_url)
            
            question = remove_umlaut(question)
            answer = remove_umlaut(answer)
            
            file.write(f"Frage: {question}\n")
            file.write(f"Antwort: {answer}\n")
            file.write("----------\n")

def main():
    base_url = "https://ask.porsche.com/de/de-DE/"
    
    for category, path in url_paths.items():
        print(f"Scraping {category}...")
        url = base_url + path + "/"
        output_file = f"{category}_output.txt"
        scrapeData(url, output_file)
        print(f"Finished scraping {category}. Results saved in {output_file}")

if __name__ == "__main__":
    main()