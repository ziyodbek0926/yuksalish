from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
import sqlite3
import pandas as pd

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT
)''')
conn.commit()

ADMIN_ID = 6389876397  


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    if user.id == ADMIN_ID:  
        await update.message.reply_text(
            f"Salom, {user.first_name}! Bu yerdan foydalanuvchilar ma'lumotlarini olishingiz mumkin.",
            reply_markup=ReplyKeyboardMarkup([
                ["Ma'lumotlarni olish"]
            ], resize_keyboard=True)
        )
    else:  
        await update.message.reply_text(
            f"Salom, {user.first_name}!\nKontakt ma'lumotlaringizni yuboring.",
            reply_markup=ReplyKeyboardMarkup([
                [KeyboardButton("Kontakt yuborish", request_contact=True)]
            ], resize_keyboard=True)
        )


async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    name = contact.first_name
    phone = contact.phone_number

    cursor.execute("INSERT INTO users (name, phone) VALUES (?, ?)", (name, phone))
    conn.commit()

    await update.message.reply_text(
       """🎉 Tabriklaymiz! 🎉

Sizga do‘konimiz tomonidan 3% chegirma tasdiqlandi! ✅
Chegirmadan foydalanish uchun do‘konimizga tashrif buyuring va mahsulotlaringizni yanada arzonroq narxlarda oling! 🛍️

📍 Manzil: Uchqo'rg'on Xalq Banki binosi ro'parasida, Yuksalish Kredit Do‘koni
☎️ Aloqa uchun: +998 97 778 87 73
📲 Bizning Telegram kanalimiz
@uchqorgon_muddatli8888

🎁 Do‘konimizga tashrifingizdan xursand bo‘lamiz!."""
    )


async def send_database(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()

    if not data: 
        await update.message.reply_text("Ma'lumotlar bazasi bo'sh.")
        return

    df = pd.DataFrame(data, columns=["ID", "Ism", "Telefon"])
    file_path = "users_data.xlsx"
    df.to_excel(file_path, index=False)

    with open(file_path, 'rb') as file:
        await context.bot.send_document(chat_id=ADMIN_ID, document=file)

    await update.message.reply_text("Ma'lumotlar bazasi yuborildi!")


async def handle_admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Ma'lumotlarni olish" and update.effective_user.id == ADMIN_ID:
        await send_database(update, context)
    elif update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Kechirasiz, sizda bu funksiyadan foydalanish huquqi yo'q.")
