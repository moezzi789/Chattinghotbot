import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# لیست کاربران در انتظار
waiting_users = {}
active_chats = {}

# تنظیمات لاگ‌گیری
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

# فرمان شروع
def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلام! برای شروع چت ناشناس، دستور /find رو بزن.")

# جستجوی چت ناشناس
def find(update: Update, context: CallbackContext):
    user_id = update.message.chat_id

    if user_id in active_chats:
        update.message.reply_text("شما قبلاً در یک چت هستید! برای خروج از چت، /end رو بزن.")
        return

    if waiting_users:
        partner_id, _ = waiting_users.popitem()
        active_chats[user_id] = partner_id
        active_chats[partner_id] = user_id

        context.bot.send_message(partner_id, "یک نفر پیدا شد! حالا می‌تونید چت کنید.")
        update.message.reply_text("یک نفر پیدا شد! حالا می‌تونید چت کنید.")
    else:
        waiting_users[user_id] = update.message
        update.message.reply_text("منتظر پیدا شدن یک نفر باشید...")

# مدیریت پیام‌ها بین کاربران
def message_handler(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    partner_id = active_chats.get(user_id)

    if partner_id:
        context.bot.send_message(partner_id, update.message.text)
    else:
        update.message.reply_text("شما در چت نیستید! از /find استفاده کنید.")

# پایان چت
def end(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    partner_id = active_chats.pop(user_id, None)

    if partner_id:
        del active_chats[partner_id]
        context.bot.send_message(partner_id, "چت پایان یافت.")
        update.message.reply_text("چت پایان یافت.")
    else:
        update.message.reply_text("شما در چت نیستید!")

# اجرای ربات
def main():
    TOKEN = "YOUR_BOT_TOKEN"  # توکن رباتت رو اینجا بذار
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("find", find))
    dp.add_handler(CommandHandler("end", end))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
