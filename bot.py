import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TEXTS = {
    "start": (
        "👋 Assalomu alaykum!\n\n"
        "⚡ Reaksiya xizmatiga xush kelibsiz.\n"
        "Kerakli bo‘limni tanlang:"
    ),
    "help": "ℹ️ Yordam bo‘limi.",
}

EDITING = {}


def is_admin(user_id):
    return user_id == ADMIN_ID


def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("⚡ Reaksiyalar", callback_data="reactions"),
            InlineKeyboardButton("🤖 Botlar", callback_data="bots"),
        ],
        [
            InlineKeyboardButton("📢 Kanallar", callback_data="channels"),
            InlineKeyboardButton("📨 Xabar yuborish", callback_data="send"),
        ],
        [
            InlineKeyboardButton("🕘 Eski post", callback_data="old_post"),
            InlineKeyboardButton("📊 Statistika", callback_data="stats"),
        ],
        [
            InlineKeyboardButton("⚙️ Admin panel", callback_data="admin"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def admin_menu():
    keyboard = [
        [
            InlineKeyboardButton("✏️ Matnlarni tahrirlash", callback_data="edit_text"),
        ],
        [
            InlineKeyboardButton("🎨 Tugma ranglari", callback_data="button_colors"),
        ],
        [
            InlineKeyboardButton("🤖 Reaksiya botlari", callback_data="bots"),
        ],
        [
            InlineKeyboardButton("📢 Kanallar", callback_data="channels"),
        ],
        [
            InlineKeyboardButton("📨 Xabar yuborish", callback_data="send"),
        ],
        [
            InlineKeyboardButton("🕘 Eski postga reaksiya", callback_data="old_post"),
        ],
        [
            InlineKeyboardButton("📊 Statistika", callback_data="stats"),
        ],
        [
            InlineKeyboardButton("🔙 Ortga", callback_data="back"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        TEXTS["start"],
        reply_markup=main_menu()
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    if data == "back":
        await query.edit_message_text(
            TEXTS["start"],
            reply_markup=main_menu()
        )
        return

    if data == "admin":
        if not is_admin(user_id):
            await query.answer("⛔ Faqat admin uchun!", show_alert=True)
            return

        await query.edit_message_text(
            "⚙️ ADMIN PANEL\n\nKerakli bo‘limni tanlang:",
            reply_markup=admin_menu()
        )
        return

    if data == "reactions":
        await query.edit_message_text(
            "⚡ REAKSIYALAR\n\n"
            "Bu yerda kichik botlar orqali reaksiyalar boshqariladi.\n\n"
            "🤖 8+ ta bot ulash mumkin.\n"
            "❤️ Har bir botga alohida reaksiya beriladi.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🤖 Botlarni boshqarish", callback_data="bots")],
                [InlineKeyboardButton("🔙 Ortga", callback_data="back")]
            ])
        )
        return

    if data == "bots":
        if not is_admin(user_id):
            await query.answer("⛔ Faqat admin uchun!", show_alert=True)
            return

        await query.edit_message_text(
            "🤖 REAKSIYA BOTLARI\n\n"
            "Hozircha botlar qo‘shilmagan.\n\n"
            "Keyingi bosqichda:\n"
            "➕ Bot qo‘shish\n"
            "❤️ Reaksiya tanlash\n"
            "🔄 Botni yoqish/o‘chirish\n"
            "🗑 Botni o‘chirish",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Bot qo‘shish", callback_data="add_bot")],
                [InlineKeyboardButton("🔙 Ortga", callback_data="admin")]
            ])
        )
        return

    if data == "channels":
        if not is_admin(user_id):
            await query.answer("⛔ Faqat admin uchun!", show_alert=True)
            return

        await query.edit_message_text(
            "📢 KANALLAR\n\n"
            "Bu bo‘limdan kanallarni qo‘shish va boshqarish mumkin.\n\n"
            "Bot kanalga admin qilib qo‘yilgan bo‘lishi kerak.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Kanal qo‘shish", callback_data="add_channel")],
                [InlineKeyboardButton("📋 Kanallar ro‘yxati", callback_data="channel_list")],
                [InlineKeyboardButton("🔙 Ortga", callback_data="admin")]
            ])
        )
        return

    if data == "send":
        if not is_admin(user_id):
            await query.answer("⛔ Faqat admin uchun!", show_alert=True)
            return

        await query.edit_message_text(
            "📨 KANALGA XABAR YUBORISH\n\n"
            "Keyingi bosqichda bu yerga:\n"
            "📝 Matn\n"
            "🖼 Rasm\n"
            "🎥 Video\n"
            "📢 Bir nechta kanalga yuborish\n"
            "funksiyalari qo‘shiladi.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Ortga", callback_data="admin")]
            ])
        )
        return

    if data == "old_post":
       
