# Hayden Schennum
# 2025-11-16

import requests
from bs4 import BeautifulSoup
import re



# str -> str | None
# given URL, sends HTTP GET request to URL and returns the text response
def get_page_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error: Unable to retrieve content. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None



if __name__ == "__main__":
    index_url = "https://cdb.apterous.org/index.php"
    index_html = get_page_content(index_url)
    index_soup = BeautifulSoup(index_html, "html.parser")

    fh_out = open("output.txt","w",encoding='utf-8')
    records = []

    for a in index_soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("series.php?series="):
            series_url = "https://cdb.apterous.org/" + href
            series_html = get_page_content(series_url)
            series_soup = BeautifulSoup(series_html, "html.parser")
            for a in series_soup.find_all("a", href=True):
                href = a["href"]
                if href.startswith("game.php?game="):
                    game_url = "https://cdb.apterous.org/" + href
                    game_html = get_page_content(game_url)
                    game_soup = BeautifulSoup(game_html, "html.parser")

                    content_div = game_soup.find("div", class_="content")
                    text = content_div.get_text()
                    lines = text.split("\n")


                    
                    current_record = []
                    recording = False

                    start_pattern = re.compile(r"Round\s+\d+:\s+[\d, ]+\. Target: \d+\.")

                    for line in lines:
                        if start_pattern.search(line):
                            recording = True
                            current_record.append(line)
                            continue

                        if recording:
                            current_record.append(line)
                            if line.strip().startswith("Score:"): # end pattern
                                records.append("\n".join(current_record))
                                current_record = []
                                recording = False


    for r in records:
        print(r)
        print()

    # fh_out.close()