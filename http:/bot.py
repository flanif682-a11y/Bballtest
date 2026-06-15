import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("TOKEN")

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {"score": 0, "step": 1}

    keyboard = [["صد"], ["هشتاد"], ["شصت"], ["زیر شصت"]]

    await update.message.reply_text(
        "سوال اول:\nاز یک تا صد به ماینکرفت بازی کردن امیرقلی چند میدهید؟",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in user_data:
        await start(update, context)
        return

    data = user_data[user_id]
    step = data["step"]

    # سوال 1
    if step == 1:
        if text == "صد":
            data["score"] += 5
            good = True
        elif text == "هشتاد":
            data["score"] += 4
            good = True
        elif text == "شصت":
            data["score"] += 2
            good = False
        else:
            good = False

        data["step"] = 2

        if good:
            keyboard = [["همبرگر"], ["پاستا"], ["پیتزا"], ["لازانیا"]]
            msg = "آفرین آفرین حالا بگو فست فود مورد علاقه امیرقلی چیه ؟"
        else:
            keyboard = [["میخارم"], ["هیتر هستم"], ["از نیگرا خوشم نمیاد"], ["همه گزینه ها"]]
            msg = "خاک بر سرت چرا نمره کم میدی ؟"

        await update.message.reply_text(msg, reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        return

    # سوال 2
    if step == 2:
        if text == "پیتزا" or text == "میخارم":
            data["score"] += 5

        data["step"] = 3

        keyboard = [["آب پرتقال"], ["آب هویج"], ["نوشابه"], ["شیرکاکائو"]]

        await update.message.reply_text(
            "سوال سوم: نوشیدنی مورد علاقه امیرقلی چیه؟",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        return

    # سوال 3
    if step == 3:
        if text == "شیرکاکائو":
            data["score"] += 5

        data["step"] = 4

        keyboard = [["آره"], ["هرچی بگم کار خودتو میکنی"], ["نه لازم نیست"], ["نظری ندارم"]]

        await update.message.reply_text(
            "سوال چهارم: یه چنل به عشق خودت بزنم؟",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        return

    # سوال 4
    if step == 4:
        if text == "آره":
            data["score"] += 5

        score = data["score"]
        await update.message.reply_text(f"نمره نهایی شما: {score} از 20")

        del user_data[user_id]

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    app.run_polling()

if __name__ == "__main__":
    main()
