import handlers as h
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes


async def receive_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word = update.message.text.strip()
    context.user_data["last_word"] = word
    await Menu(update, context, word)


async def Menu(update: Update, context: ContextTypes.DEFAULT_TYPE, word):
    keyboard = [
        [InlineKeyboardButton("🔍 Definitions", callback_data="definitions")],
        [InlineKeyboardButton("🗣 Pronunciation", callback_data="pronunciation"),
         InlineKeyboardButton("📝 Examples", callback_data="examples")],
        [InlineKeyboardButton("🧩 Phrase Containing", callback_data="phrase containing"),
         InlineKeyboardButton("🎵 Rhymes", callback_data="rhymes")],
        [InlineKeyboardButton("📚 Etymology", callback_data="etymology"),
         InlineKeyboardButton("🧒 Kids Definition", callback_data="kids Definition")],
        [InlineKeyboardButton("💡 New Word", callback_data="new word")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f'You entered: "{word}". What do you want to see?',
        reply_markup=reply_markup
    )



async def Menu_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🖥 Menu", callback_data="menu"),
         InlineKeyboardButton("💡 New word", callback_data="new word")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "What next? : ",
        reply_markup=reply_markup
    )


async def New_Word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Enter your word :"
    )




async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query  # extracts the CallbackQuery object from the update
    await query.answer()  # acknowledge button press and inform Telegram about it

    data = query.data.lower()  # the callback_data from buttons in Menu() & Menu_2() function
    word = context.user_data.get("last_word")  # we'll store last word user typed

    if not word:
        await query.edit_message_text("Please send a word first!")
        return

    # Dispatch based on button
    if data == "definitions":
        await h.Definitions(query, context, word)
    elif data == "pronunciation":
        await h.Pronunciation(query, context, word)
    elif data == "kids definition":
        await h.Kids_Definition(query, context, word)
    elif data == "rhymes":
        await h.Rhymes(query, context, word)
    elif data == "examples":
        await h.Examples(query, context, word)
    elif data == "phrase containing":
        await h.Phrase_Containing(query, context, word)
    elif data == "etymology":
        await h.Etymology(query, context, word)
    elif data == "new word":
        await New_Word(query, context)
    elif data == "menu":
        await Menu(query, context, word)


