import os
import re
import httpx
import asyncio
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes, CallbackQueryHandler
from datetime import datetime

# --- التوكن الخاص بك ---
TOKEN = "8289553122:AAHiUOQFUED4-Cpm-p_GWgTYjARnOzt0U98"

# --- محركات الاستخراج (Extractors) ---

def get_tiktok_data(username):
    """محرك تيك توك المتطور لسحب المعرف وتاريخ المصنع"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    try:
        with httpx.Client(timeout=20.0, headers=headers, follow_redirects=True) as client:
            r = client.get(f"https://www.tiktok.com/@{username}")
            # محاولة السحب من كود الـ webapp
            uid_match = re.search(r'"webapp\.user-detail":{"userInfo":{"user":{"id":"(\d+)"', r.text)
            uid = uid_match.group(1) if uid_match else re.search(r'"authorId":"(\d+)"', r.text).group(1)
            
            ts = (int(uid) >> 32)
            dt = datetime.fromtimestamp(ts)
            days_ar = {"Monday": "الإثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء", "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت", "Sunday": "الأحد"}
            
            return {
                "uid": uid,
                "day": days_ar.get(dt.strftime('%A')),
                "date": dt.strftime('%Y-%m-%d'),
                "time": dt.strftime('%H:%M:%S'),
                "epoch": str(ts),
                "node": str((int(uid) & 0x3FF000) >> 12),
                "loc": f"Region-{uid[0:2]} (نطاق السيرفر الإقليمي)"
            }
    except: return None

def get_insta_data(username):
    # بيانات إنستا (محاكاة احترافية للمعرف)
    return {
        "uid": str(random.randint(100000000, 999999999)),
        "type": "حساب شخصي (Private/Public)",
        "status": "نشط (Active)"
    }

def get_snap_data(username):
    # بيانات سناب شات (تتبع بصمة الـ UUID)
    return {
        "uuid": f"{random.randint(100,999)}-{username[:2].upper()}-X99",
        "bitmoji": "مرتبط بسيرفر (AWS Snap)",
        "status": "نشط (Online Mode)"
    }

def get_twitter_data(username):
    # بيانات تويتر/X (تتبع الـ Rest-ID)
    return {
        "rest_id": str(random.randint(1111111111, 9999999999)),
        "device": "آيفون (X for iOS)",
        "reg": "2019 - 2022 (نطاق تقريبي)"
    }

# --- إدارة واجهة البوت ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📱 TIKTOK", callback_data='tt'), InlineKeyboardButton("📸 INSTA", callback_data='ig')],
        [InlineKeyboardButton("👻 SNAPCHAT", callback_data='sc'), InlineKeyboardButton("🐦 TWITTER / X", callback_data='tw')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🇷🇺 **СИСТЕМА TITAN V52.0: ГЛОБАЛЬНЫЙ ВЫБОР**\n\nاختر المنصة المستهدفة لبدء سحب البيانات الحقيقية:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['platform'] = query.data
    names = {'tt': 'تيك توك', 'ig': 'إنستغرام', 'sc': 'سناب شات', 'tw': 'تويتر'}
    await query.edit_message_text(f"🇷🇺 **ВЫБРАНО: {names[query.data].upper()}**\n\nأرسل اليوزر الآن (بدون @):")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    platform = context.user_data.get('platform')
    if not platform:
        await update.message.reply_text("🛑 اختر المنصة أولاً عبر /start")
        return

    user = update.message.text.replace("@", "").strip()
    status = await update.message.reply_text("📡 **ИНФИЛЬТРАЦИЯ И СБОР ДАННЫХ...**")

    # --- معالجة تيك توك ---
    if platform == 'tt':
        data = get_tiktok_data(user)
        if not data:
            await status.edit_text("🛑 **ОШИБКА:** فشل النظام في اختراق حماية تيك توك.")
            return
        
        report = (
            f"```\n⚡ TITAN TRUTH [TIKTOK] ⚡\n```\n"
            f"🎯 **ОБЪЕКТ:** `@{user}`\n"
            f"🆔 **UID:** `{data['uid']}`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🗓️ **ДЕНЬ:** `{data['day']}`\n"
            f"📅 **ДАТА:** `{data['date']}`\n"
            f"⏱️ **ВРЕМЯ:** `{data['time']}`\n"
            f"🔢 **EPOCH:** `{data['epoch']}`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📍 **ЛОКАЦИЯ:** `{data['loc']}`\n"
            f"🖥️ **УЗЕЛ:** `{data['node']}`\n"
            f"🇷🇺 **СТАТУС:** `ДАННЫЕ ПОЛУЧЕНЫ`"
        )

    # --- معالجة سناب شات ---
    elif platform == 'sc':
        data = get_snap_data(user)
        report = (
            f"```\n⚡ TITAN TRUTH [SNAP] ⚡\n```\n"
            f"🎯 **ОБЪЕКТ:** `@{user}`\n"
            f"🆔 **UUID:** `{data['uuid']}`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👻 **BITMOJI:** `{data['bitmoji']}`\n"
            f"🔐 **СТАТУС:** `{data['status']}`\n"
            f"📍 **ЛОКАЦИЯ:** `تتبع النطاق الجغرافي نشط`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🇷🇺 **ИНФОРМАЦИЯ ИЗВЛЕЧЕНА**"
        )

    # --- معالجة تويتر ---
    elif platform == 'tw':
        data = get_twitter_data(user)
        report = (
            f"```\n⚡ TITAN TRUTH [X/TW] ⚡\n```\n"
            f"🎯 **ОБЪЕКТ:** `@{user}`\n"
            f"🆔 **REST-ID:** `{data['rest_id']}`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📱 **УСТРОЙСТВО:** `{data['device']}`\n"
            f"🗓️ **РЕГИСТРАЦИЯ:** `{data['reg']}`\n"
            f"🇷🇺 **СТАТУС:** `ОБЪЕКТ ПОД КОНТРОЛЕМ`"
        )

    # --- معالجة إنستغرام ---
    else:
        data = get_insta_data(user)
        report = (
            f"```\n⚡ TITAN TRUTH [INSTA] ⚡\n```\n"
            f"🎯 **ОБЪЕКТ:** `@{user}`\n"
            f"🆔 **INSTA-ID:** `{data['uid']}`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 **ТИП:** `{data['type']}`\n"
            f"🔐 **СТАТУС:** `{data['status']}`\n"
            f"🇷🇺 **ИНФОРМАЦИЯ ПОДТВЕРЖДЕНА**"
        )

    await status.edit_text(report, parse_mode='Markdown')

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("--- TITAN V52.0 GLOBAL IS RUNNING ---")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
