from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "YOUR_BOT_TOKEN"

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_user.id] = {"score": 0}

    keyboard = [["صد"], ["هشتاد"], ["شصت"], ["زیر شصت"]]

    await update.message.reply_text(
        "سوال اول:\nاز یک تا صد به ماینکرفت بازی کردن امیرقلی چند میدهید؟",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text

    if uid not in user_data:
        await start(update, context)
        return

    state = user_data[uid].get("state", 1)

    # سوال 1
    if state == 1:
        if text == "صد":
            user_data[uid]["score"] += 5
            user_data[uid]["good_path"] = True
        elif text == "هشتاد":
            user_data[uid]["score"] += 4
            user_data[uid]["good_path"] = True
        elif text == "شصت":
            user_data[uid]["score"] += 2
            user_data[uid]["good_path"] = False
        else:
            user_data[uid]["good_path"] = False

        user_data[uid]["state"] = 2

        if user_data[uid]["good_path"]:
            keyboard = [["همبرگر"], ["پاستا"], ["پیتزا"], ["لازانیا"]]
            await update.message.reply_text(
                "آفرین آفرین حالا بگو فست فود مورد علاقه امیرقلی چیه ؟",
                reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
            )
        else:
            keyboard = [["میخارم"], ["هیتر هستم"], ["از نیگرا خوشم نمیاد"], ["همه گزینه ها"]]
            await update.message.reply_text(
                "خاک بر سرت چرا نمره کم میدی ؟",
                reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
            )
        return

    # سوال 2
    if state == 2:
        if user_data[uid]["good_path"]:
            if text == "پیتزا":
                user_data[uid]["score"] += 5
        else:
            if text == "میخارم":
                user_data[uid]["score"] += 5

        user_data[uid]["state"] = 3

        keyboard = [["آب پرتقال"], ["آب هویج"], ["نوشابه"], ["شیرکاکائو"]]

        await update.message.reply_text(
            "سوال سوم: نوشیدنی مورد علاقه امیرقلی چیه؟",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        )
        return

    # سوال 3
    if state == 3:
        if text == "شیرکاکائو":
            user_data[uid]["score"] += 5

        user_data[uid]["state"] = 4

        keyboard = [["آره"], ["هرچی بگم کار خودتو میکنی"], ["نه لازم نیست"], ["نظری ندارم"]]

        await update.message.reply_text(
            "سوال چهارم: یه چنل به عشق خودت بزنم؟",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        )
        return

    # سوال 4
    if state == 4:
        if text == "آره":
            user_data[uid]["score"] += 5

        score = user_data[uid]["score"]

        await update.message.reply_text(
            f"🎉 آزمون تمام شد!\n\nنمره نهایی شما: {score} از 20"
        )

        del user_data[uid]

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    app.run_polling()

if __name__ == "__main__":
    main()
