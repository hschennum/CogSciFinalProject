# Hayden Schennum
# 2025-11-16

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import traceback


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


# Match str -> bool
# given contestant's regex match and target for this round;
# returns True iff contestant matched tgt
def contestant_solved(match, target):
    if not match:
        return False
    amount = match.group(2)
    solution = match.group(3)
    if "mistake" in solution.lower():
        return False
    return amount.isdigit() and int(amount) == int(target)



if __name__ == "__main__":
    index_url = "https://cdb.apterous.org/index.php"
    index_html = get_page_content(index_url)
    index_soup = BeautifulSoup(index_html, "html.parser")

    fh_out = open("output.txt","w",encoding='utf-8',buffering=1)
    # records = []

    for a in index_soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("series.php?series="):
            series_url = "https://cdb.apterous.org/" + href
            series_match = re.search(r"series=(-?\d+)", series_url)
            series_num = series_match.group(1) if series_match else ""
            if int(series_num) != 31:
                print("SKIPPING parse for series", series_num)
                continue
            print("Starting parse for series", series_num)
            series_html = get_page_content(series_url)
            if series_html is None:
                continue
            series_soup = BeautifulSoup(series_html, "html.parser")
            for a in series_soup.find_all("a", href=True):
                href = a["href"]
                if href.startswith("game.php?game="):
                    game_url = "https://cdb.apterous.org/" + href
                    game_html = get_page_content(game_url)
                    if game_html is None:
                        continue
                    game_soup = BeautifulSoup(game_html, "html.parser")
                    try:
                        
                        text = game_soup.find("div", class_="content").get_text()
                        lines = [line.strip() for line in text.split("\n") if line.strip()]


                        title = game_soup.find("title").get_text()
                        date_match = re.search(r"(\d{1,2}(?:st|nd|rd|th)?\s+\w+\s+\d{4})", title)
                        if date_match:
                            date_str = date_match.group(1)
                            date_str_clean = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)
                            date_obj = datetime.strptime(date_str_clean, "%d %B %Y")
                            date = date_obj.strftime("%Y-%m-%d") # convert to YYYY-MM-DD
                        else:
                            date = ""
                        
                        current_record = [] # header, C1, C2, RR (optional)
                        recording = False
                        # regex tip: things enclosed in parens are groups; they can be referenced later e.g. match.group(1)
                        header_pattern = re.compile(r"Round\s+(\d+):\s+([\d, ]+)\. Target: (\d+)\.")
                        contestant_pattern = re.compile(r"^([^:]+):\s*([\d\-]+)\.?\s*(.*?)\s*(?:\((\d+)\))?$") # thank you GPT for the regexs

                        for line in lines:
                            header_match = header_pattern.search(line)
                            if header_match:
                                round_num = header_match.group(1)
                                numbers_set = header_match.group(2).replace(" ", "")
                                target = header_match.group(3)                            
                                current_record.append(line)
                                recording = True
                                continue

                            if recording:
                                current_record.append(line)
                                if line.strip().startswith("Score:"): # end pattern
                                    header = current_record[0]
                                    C1_line = current_record[1]
                                    C2_line = current_record[2]
                                    RR_line = current_record[3] if len(current_record) > 4 else ""
                                    OT_line = current_record[4] if len(current_record) > 5 else ""

                                    current_record = []
                                    recording = False         

                                    C1_match = re.search(contestant_pattern, C1_line)
                                    C2_match = re.search(contestant_pattern, C2_line)
                                    RR_match = re.search(contestant_pattern, RR_line)
                                    OT_match = re.search(contestant_pattern, OT_line)

                                    if contestant_solved(C1_match, target):
                                        solved = "T"
                                        solution = C1_match.group(3)
                                    elif contestant_solved(C2_match, target):
                                        solved = "T"
                                        solution = C2_match.group(3)
                                    elif contestant_solved(RR_match, target):
                                        solved = "F"
                                        solution = RR_match.group(3)
                                    elif contestant_solved(OT_match, target):
                                        solved = "F"
                                        solution = OT_match.group(3)
                                    else: # do not keep this record
                                        continue

                                    fh_out.write(f"Series{series_num};{date};Round{round_num};{numbers_set};{target};{solved};{solution}\n")
                    except Exception as e:
                        print(f"Error processing game {game_url}: {e}")
                        # traceback.print_exc()

    # for r in records:
    #     print(r)
    #     print()

    fh_out.close()