import menu as m
import requests
from bs4 import BeautifulSoup
from telegram import Update, InputFile
from telegram.ext import ContextTypes

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Merriam-Webster Dictionary.\n\n"
        "Enter your word :"
    )

# send a Pronunciation guide pdf to the user(pronunciation command)
async def send_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_path = ("Pronunciation_Guide.pdf")
    await update.message.reply_text(
        "✅ Here's a six page guide to understand the pronunciation symbols."
        " You can see a concise table of pronunciation symbols on the last page."
    )
    with open(file_path, "rb") as file:
        await update.message.reply_document(document=InputFile(file, filename="Pronunciation_Guide.pdf"))



async def Definitions(update: Update, context: ContextTypes.DEFAULT_TYPE, word):
    url = f"https://www.merriam-webster.com/dictionary/{word}"
    response = requests.get(url)

    if response.status_code != 200:
        await update.message.reply_text("❗️ Error!\n"
                                        "An error occurred while trying to process your request")
        await m.Menu_2(update, context)
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    parts1 = soup.find_all("h2", class_="parts-of-speech")
    parts2 = []
    for i in parts1:
        parts2.append(i.get_text().strip())

    definitions_N0 = []
    definitions_N = []
    definitions_V = []
    definitions_Adj = []
    definitions_Adv = []
    definitions_Pre = []
    definitions_Pro = []
    definitions_Abb = []
    definitions_Con = []

    for i,j in enumerate(parts2):
        soup = BeautifulSoup(response.text, 'html.parser')
        if 'noun' in j:
            definitions_N = ['As Noun :']
            soup = soup.find("div", id =f"dictionary-entry-{i+1}")
            definitions_N0 += soup.find_all("div", class_="vg-sseq-entry-item")
            for d in definitions_N0:
                definitions_N += [d.find("span", class_="dtText")] + d.find_all("span", class_="unText")[:2]
            definitions_N = definitions_N[:6]
            if len(definitions_N) == 1:
                definitions_N = []

        elif 'verb' in j:
            definitions_V = definitions_V + ['As Verb :']
            verbs = soup.find_all("div", class_="vg")
            verbs = verbs[i:i+3]
            soup = soup.find("div", id=f"dictionary-entry-{i+1}")

            definitions_Vt = ['--Transitive,']
            definitions_Vi = ['--inTransitive,']
            definitions_Va = ['--Auxiliary,']
            for x in verbs:
                try:
                    if x.find("p", class_="vd").get_text() == "transitive verb":
                        definitions_Vt += x.find_all("span", class_="dtText")[:3]
                        definitions_Vt += x.find_all("span", class_="unText")[:2]
                        if len(definitions_Vt) == 1:
                            definitions_Vt = []
                except AttributeError:
                    pass
                try:
                    if x.find("p", class_="vd").get_text() == "intransitive verb":
                        definitions_Vi += x.find_all("span", class_="dtText")[:3]
                        definitions_Vi += x.find_all("span", class_="unText")[:2]
                        if len(definitions_Vi) == 1:
                            definitions_Vi = []
                except AttributeError:
                    pass
                try:
                    if x.find("p", class_="vd").get_text() == "auxiliary verb":
                        definitions_Va += x.find_all("span", class_="dtText")[:3]
                        definitions_Va += x.find_all("span", class_="unText")[:2]
                        if len(definitions_Va) == 1:
                            definitions_Va = []
                except AttributeError:
                    pass

            definitions_V += definitions_Vt + definitions_Vi + definitions_Va

        elif 'adjective' in j:
            definitions_Adj = definitions_Adj + ['As Adjective :']
            soup = soup.find("div", id=f"dictionary-entry-{i+1}")
            definitions_Adj += soup.find_all("span", class_="dtText")[:3]
            definitions_Adj += soup.find_all("span", class_="unText")[:2]
            if len(definitions_Adj) == 1:
                definitions_Adj = []

        elif 'adverb' in j:
            definitions_Adv = definitions_Adv + ['As Adverb :']
            soup = soup.find("div", id=f"dictionary-entry-{i+1}")
            definitions_Adv += soup.find_all("span", class_="dtText")[:3]
            definitions_Adv += soup.find_all("span", class_="unText")[:2]
            if len(definitions_Adv) == 1:
                definitions_Adv = []


        elif 'preposition' in j:
            definitions_Pre = definitions_Pre + ['As Preposition :']
            soup = soup.find("div", id=f"dictionary-entry-{i+1}")
            definitions_Pre += soup.find_all("span", class_="dtText")[:3]
            definitions_Pre += soup.find_all("span", class_="unText")[:3]
            if len(definitions_Pre) == 1:
                definitions_Pre = []

        elif 'pronoun' in j:
            definitions_Pro = definitions_Pro + ['As Preposition :']
            soup = soup.find("div", id=f"dictionary-entry-{i+1}")
            definitions_Pro += soup.find_all("span", class_="dtText")[:3]
            definitions_Pro += soup.find_all("span", class_="unText")[:2]
            if len(definitions_Pro) == 1:
                definitions_Pro = []


        elif 'abbreviation' in j:
            definitions_Abb = definitions_Abb + ['As Abbreviation :']
            soup = soup.find("div", id=f"dictionary-entry-{i+1}")
            definitions_Abb += soup.find_all("span", class_="dtText")[:3]
            definitions_Abb += soup.find_all("span", class_="unText")[:2]
            if len(definitions_Abb) == 1:
                definitions_Abb = []

        elif 'conjunction' in j:
            definitions_Con = definitions_Con + ['As Conjunction :']
            soup = soup.find("div", id=f"dictionary-entry-{i+1}")
            definitions_Con += soup.find_all("span", class_="dtText")[:3]
            definitions_Con += soup.find_all("span", class_="unText")[:2]
            if len(definitions_Con) == 1:
                definitions_Con = []


    definitions = (definitions_N + definitions_V + definitions_Adj + definitions_Adv+
                   definitions_Pre + definitions_Pro + definitions_Abb + definitions_Con)

    if definitions == []:
        await update.message.reply_text(f'There are no definitions for "{word}".')
        return

    result = "Definitions :  \n\n\n"
    for i, d in enumerate(definitions):
        if not isinstance(d, str):
            text = d.get_text().strip().lstrip(":")
            result += f"  • {text}\n"
        else :
            if d in ['--Transitive,', '--inTransitive,', '--Auxiliary,']:
                result += '\n' + d + '\n'
            else:
                result += '\n\n' + d + '\n'

    await update.message.reply_text(result)
    await m.Menu_2(update, context)


async def Pronunciation(update: Update, context: ContextTypes.DEFAULT_TYPE, word):
    url = f"https://www.merriam-webster.com/dictionary/{word}"
    response = requests.get(url)

    if response.status_code != 200:
        await update.message.reply_text("❗️ Error!\n"
                                        "An error occurred while trying to process your request")
        await m.Menu_2(update, context)
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    pronunciation = soup.find("a", class_="play-pron-v2")

    if not pronunciation:
        await update.message.reply_text(f'There is no pronunciation for "{word}".')
        return

    result = "Pronunciation:  \n\n"
    text = pronunciation.get_text().strip()
    result += f" {text}\n\n"

    await update.message.reply_text(result)
    await m.Menu_2(update, context)


async def Examples(update: Update, context: ContextTypes.DEFAULT_TYPE, word):
    url = f"https://www.merriam-webster.com/sentences/{word}"
    response = requests.get(url)

    if response.status_code != 200:
        await update.message.reply_text("❗️ Error!\n"
                                        "An error occurred while trying to process your request")
        await m.Menu_2(update, context)
        return



    soup = BeautifulSoup(response.text, 'html.parser')
    examples = soup.find_all("span", class_="t")

    if not examples:
        await update.message.reply_text(f'There are no examples for "{word}".')
        return

    result = "Examples:  \n\n"
    for i, d in enumerate(examples[:5], 1):
        text = d.get_text().strip()
        text = text.replace(f"{word}", f"<b>{word}</b>")
        result += f"{i}. {text}\n\n"

    await update.message.reply_text(result, parse_mode="HTML")
    await m.Menu_2(update, context)


async def Etymology(update: Update, context: ContextTypes.DEFAULT_TYPE, word):
    url = f"https://www.merriam-webster.com/dictionary/{word}"
    response = requests.get(url)

    if response.status_code != 200:
        await update.message.reply_text("❗️ Error!\n"
                                        "An error occurred while trying to process your request")
        await m.Menu_2(update, context)
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    etymology = soup.find("p", class_="et")

    if not etymology:
        await update.message.reply_text(f'There is no etymology for "{word}".')
        return

    result = "Etymology:  \n\n"
    text = etymology.get_text().strip()
    result += f" {text}\n\n"

    await update.message.reply_text(result)
    await m.Menu_2(update, context)


async def Phrase_Containing(update: Update, context: ContextTypes.DEFAULT_TYPE, word):
    url = f"https://www.merriam-webster.com/dictionary/{word}"
    response = requests.get(url)

    if response.status_code != 200:
        await update.message.reply_text("❗️ Error!\n"
                                        "An error occurred while trying to process your request")
        await m.Menu_2(update, context)
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    phrases = soup.find_all("li", class_="related-phrases-list-item col-6 col-lg-4")

    if not phrases:
        await update.message.reply_text(f'There are no phrases for "{word}".')
        return

    result = "Phrases:  \n\n"
    for d in phrases[:6]:
        text = d.get_text().strip()
        result += f' "{text}", '

    await update.message.reply_text(result)
    await m.Menu_2(update, context)


async def Rhymes(update: Update, context: ContextTypes.DEFAULT_TYPE, word):
    url = f"https://www.merriam-webster.com/dictionary/{word}"
    response = requests.get(url)

    if response.status_code != 200:
        await update.message.reply_text("❗️ Error!\n"
                                        "An error occurred while trying to process your request")
        await m.Menu_2(update, context)
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    rhymes = soup.find_all("li", class_="mw-grid-table-list-item")

    if not rhymes:
        await update.message.reply_text(f'There are no rhymes for "{word}".')
        return

    result = "Rhymes:  \n\n"
    for d in rhymes[:6]:
        text = d.get_text().strip()
        result += f' "{text}", '

    await update.message.reply_text(result)
    await m.Menu_2(update, context)


async def Kids_Definition(update: Update, context: ContextTypes.DEFAULT_TYPE, word):
    url = f"https://www.merriam-webster.com/dictionary/{word}"
    response = requests.get(url)

    if response.status_code != 200:
        await update.message.reply_text("❗️ Error!\n"
                                        "An error occurred while trying to process your request")
        await m.Menu_2(update, context)
        return
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        soup = soup.find("div", id="kidsdictionary")
        soup = soup.find("div", class_="content-section-body")
        soup = soup.find("div", id="elementary-entry-1")
        soup = soup.find("div", class_="vg")
        kidsdef = soup.find_all("span", class_="dtText")
    except AttributeError:
        await update.message.reply_text(f'There are no kids definition for "{word}".')
        return

    if not kidsdef:
        await update.message.reply_text(f'There are no kids definition for "{word}".')
        return

    result = "Kids Definition:  \n\n"
    for i, d in enumerate(kidsdef[:2], 1):
        text = d.get_text().strip().lstrip(":")
        result += f"{i}. {text}\n\n"

    await update.message.reply_text(result)
    await m.Menu_2(update, context)