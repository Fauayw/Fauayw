import os
import re
import yt_dlp
import asyncio
import httpx
import shutil
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime

# --- التوكن ---
TOKEN = "8561488420:AAGr8c0oPWEcWoT9kvHBOpBEsBWfD2p6zKA"

def get_detailed_era(u_id):
    try:
        u_id = int(u_id)
        if u_id < 10**10: return "💎 الأساطير (2016-2017)"
        elif u_id < 6500000000000000000: return "🎖️ قديم (2018-2019)"
        else: return "🛰️ حديث (2020-2026)"
    except: return "Unknown"

async def titan_elite_engine(username):
    work_dir = f"elite_cache_{username}"
    if not os.path.exists(work_dir): os.makedirs(work_dir)

    # 1. جلب البيانات العميقة (Web Scraping)
    async with httpx.AsyncClient(timeout=20.0) as client:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        resp = await client.get(f"https://www.tiktok.com/@{username}", headers=headers)
        
        sec_uid = re.search(r'"secUid":"(.*?)"', resp.text).group(1) if '"secUid":"' in resp.text else "N/A"
        bio = re.search(r'"signature":"(.*?)"', resp.text).group(1) if '"signature":"' in resp.text else "N/A"
        verified = "✅ Verified" if '"verified":true' in resp.text else "❌ Unverified"
        followers = re.search(r'"followerCount":(\d+)', resp.text).group(1) if '"followerCount":' in resp.text else "0"
        hearts = re.search(r'"heartCount":(\d+)', resp.text).group(1) if '"heartCount":' in resp.text else "0"

    # 2. تحليل الميتا داتا والفيديوهات
    ydl_opts = {
        'quiet': True, 'getcomments': True, 'playlist_items': '1', 
        'outtmpl': f'{work_dir}/%(id)s.%(ext)s'
    }
    
    intel_leads = []
    video_path = None
    music_info = "Unknown"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(None, lambda: ydl.extract_info(f"https://www.tiktok.com/@{username}", download=True))
        
        u_id = info.get('uploader_id', '0')
        age = get_detailed_era(u_id)
        
        if 'entries' in info and len(info['entries']) > 0:
            video_entry = info['entries'][0]
            video_path = ydl.prepare_filename(video_entry)
            music_info = video_entry.get('track', 'Original Sound')
            
            # رادار التسريبات المطور
            comments = video_entry.get('comments', [])
            raw_text = bio + " " + " ".join([c.get('text', '') for c in comments])
            intel_leads = re.findall(r'(\+?\d{9,15}|snap:|insta:|@\w+|سناب:|انستا:|بالرياض|بجدة|بالشرقية|بالكويت)', raw_text, re.IGNORECASE)

    # حساب معدل التفاعل التقديري
    try: engagement = round((int(hearts) / int(followers)) * 10, 1) if int(followers) > 0 else 0
    except: engagement = "Normal"

    return {
        "user": username, "sec": sec_uid, "id": u_id, "bio": bio, "age": age,
        "verified": verified, "followers": followers, "hearts": hearts,
        "eng": engagement, "music": music_info, "leads": list(set(intel_leads))
    }, video_path, work_dir

async def handle_titan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.text.replace("@", "").strip()
    # رسالة فخمة أثناء المعالجة
    status = await update.message.reply_text(
        f"☣️ **[ SYSTEM BREACH IN PROGRESS ]**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📡 Target: `@{user}`\n"
        f"📡 Status: `Injecting API Tracer...`"
    )

    try:
        data, video, w_dir = await titan_elite_engine(user)
        
        # قالب التقرير الأفخم (بدون ملفات)
        final_msg = (
            f"```\n"
            f"⚡ TITAN ELITE RECON v10.0 ACTIVE ⚡\n"
            f"════════════════════════════════════\n"
            f"```\n"
            f"👤 **Target:** `@{data['user']}` | {data['verified']}\n"
            f"📊 **Followers:** `{data['followers']}` | **Likes:** `{data['hearts']}`\n"
            f"📈 **Engage Rate:** `{data['eng']}%` (تقديري)\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 **UID:** `{data['id']}`\n"
            f"⏳ **Era:** `{data['age']}`\n"
            f"🔒 **SecUID:** `{data['sec']}`\n"
            f"🎵 **Fav Music:** `{data['music']}`\n"
            f"📝 **Bio:** `{data['bio']}`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🔍 **Detected Leads (الارتباطات):**\n"
            f"`{', '.join(data['leads']) if data['leads'] else '❌ No Leaks Found'}`\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🛰️ **Forensic Tools:**\n"
            f"• [Deep Search](https://www.google.com/search?q=%22{user}%22)\n"
            f"• [UID Tracker](https://www.google.com/search?q=%22{data['id']}%22)\n\n"
            f"🗑️ _System: Local memory wiped. Cloud active._"
        )

        if video and os.path.exists(video):
            await update.message.reply_video(video=open(video, 'rb'), caption=f"🎬 Media Capture: @{user}")

        await status.edit_text(final_msg, parse_mode='Markdown', disable_web_page_preview=True)
        shutil.rmtree(w_dir)

    except Exception as e:
        await status.edit_text(f"🛑 **[ SCAN HALTED ]**\nخطأ: الحساب قد يكون خاصاً أو محظوراً.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", lambda u,c: u.message.reply_text("💀 TITAN ELITE v10.0 READY.")))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_titan))
    app.run_polling()

if __name__ == '__main__': main()
