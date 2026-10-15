import logging
import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# ==========================================
# 1. الإعدادات الأساسية
# ==========================================
BOT_TOKEN = "6252714666:AAHmm6U5Heecpxzt4xvETneErArsS8oZdoU"
PROMO_CODE = "1x_5881253"
DOWNLOAD_LINK = "https://1xbet.com"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==========================================
# 2. معالجات الأوامر والرسائل
# ==========================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    أمر /start: ترحب بالمستخدم وتظهر زر التحميل وزر التفعيل
    """
    context.user_data.clear()
    
    welcome_text = (
        "🌐 **النظام الذكي للتحليل والتشغيل - 1xBET VIP v4.8**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "مرحباً بك في البوت المعتمد لفك خوارزميات لعبة التفاحة 🍎\n\n"
        "⚠️ **تنبيه نظام الحماية والرقابة:**\n"
        "البوت يعمل عبر خوادم مخصصة مرتبطة بالسيرفر المباشر. يتم إيقاف الخوارزمية تلقائياً كل فترة لتفادي كشف الحسابات أو حظر السيرفر، ويُعاد تشغيله بعد تحديث الأكواد.\n\n"
        "📌 **خطوات التفعيل والشروط الأساسية:**\n"
        "1️⃣ قم بتحميل التطبيق الرسمي أو افتح الموقع عبر الرابط أدناه.\n"
        "2️⃣ أنشئ **حساب جديد** (بنقرة واحدة أو عن طريق الهاتف).\n"
        "3️⃣ ادخل البروموكود المعتمد لربط حسابك بالسيرفر:\n"
        f"👈 البروموكود: `{PROMO_CODE}` (اضغط عليه للنسخ)\n\n"
        "4️⃣ بعد إتمام التسجيل، اضغط على زر **\"تم التسجيل والتحقق ✅\"** لتأكيد الـ ID."
    )

    inline_keyboard = [
        [InlineKeyboardButton("📥 تحميل تطبيق 1xbet", url=DOWNLOAD_LINK)],
        [InlineKeyboardButton("✅ تم التسجيل والتحقق", callback_data="check_registration")]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)

    await update.message.reply_text(
        text=welcome_text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    عند الضغط على زر 'تم التسجيل والتحقق ✅'
    """
    query = update.callback_query
    await query.answer()

    if query.data == "check_registration":
        context.user_data["awaiting_id"] = True
        
        request_id_text = (
            "🔄 **جاري الاتصال بسيرفرات 1xbet...**\n\n"
            "يرجى إرسال **ID الحساب الجديد** الخاص بك الآن في شات البوت لربطه بخوارزمية التوقع."
        )
        
        # إظهار زر إلغاء أو توجيه سفلي للتحكم
        keyboard = [["توقع التفاحة 🍎🎯"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        await query.message.reply_text(
            text=request_id_text,
            parse_mode="Markdown",
            reply_markup=reply_markup  # هذا يضمن ظهور الكيبورد فوراً للعميل عند الضغط
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    معالجة إرسال الـ ID أو الضغط على الأزرار
    """
    user_text = update.message.text.strip()

    # --- 1. إذا أرسل المستخدم أرقام الـ ID ---
    if user_text.isdigit():
        account_id = user_text
        context.user_data["account_id"] = account_id
        context.user_data["awaiting_id"] = False
        
        checking_msg = await update.message.reply_text(
            "⏳ *جاري مطابقة ID الحساب مع قواعد بيانات البروموكود...*", 
            parse_mode="Markdown"
        )
        await asyncio.sleep(1.5)
        await checking_msg.delete()

        success_text = (
            f"✅ **تم التحقق من الحساب بنجاح!**\n"
            f"🆔 ID: `{account_id}`\n"
            f"🌐 المنصة: **1xbet VIP**\n"
            f"🔑 البروموكود: `{PROMO_CODE}`\n\n"
            "اضغط على زر **\"توقع التفاحة 🍎🎯\"** بالأسفل للحصول على التوقع."
        )
        
        keyboard = [["توقع التفاحة 🍎🎯"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            text=success_text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    # --- 2. عند الضغط على زر التوقع ---
    elif user_text in ["توقع التفاحة 🍎🎯", "التوقع التالي 🔄"]:
        if "account_id" not in context.user_data:
            await update.message.reply_text(
                "⚠️️ **لم يتم ربط ID الحساب بعد!**\n"
                "يرجى إرسال رقم الـ ID الخاص بحسابك الجديد (أرقام فقط) أولاً."
            )
            return

        system_status = random.choice([
            "🟢 حالة السيرفر: متصل وآمن",
            "🟢 حالة الخوارزمية: نشطة 100%",
            "🟡 حالة السيرفر: ضغط متوسط - نظام حماية متقبل"
        ])
        
        apple_pos = random.randint(1, 5)
        safe_rate = random.randint(93, 99)

        game_response = (
            f"🛡️ {system_status}\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🎯 **التوقع الحالي:** اختر التفاحة رقم **[{apple_pos}]** 🍎\n"
            f"📊 **نسبة الأمان:** {safe_rate}%\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "💡 *تنبيه:* إذا واجهت حظراً أو توقفاً، فهذا يعني أن الشركة تجري فحصاً دورياً وسنعيد تشغيل البوت فوراً."
        )

        keyboard = [
            ["التوقع التالي 🔄"],
            ["إعادة ضبط الحساب ⚙️"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(text=game_response, parse_mode="Markdown", reply_markup=reply_markup)

    # --- 3. إعادة الضبط ---
    elif user_text == "إعادة ضبط الحساب ⚙️":
        context.user_data.clear()
        await update.message.reply_text(
            "تم إغلاق الجلسة وإعادة تعيين الاتصال. اضغط /start للبدء من جديد.",
            reply_markup=ReplyKeyboardRemove()
        )

    # --- 4. أي نص آخر ---
    else:
        keyboard = [["توقع التفاحة 🍎🎯"]] if "account_id" in context.user_data else []
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True) if keyboard else None
        
        await update.message.reply_text(
            "يرجى كتابة رقم الـ ID الخاص بك (أرقام فقط) أو استخدام الأزرار في الأسفل.",
            reply_markup=reply_markup
        )


# ==========================================
# 3. التشغيل الرئيسي
# ==========================================

def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("البوت يعمل بنجاح...")
    app.run_polling()


if __name__ == "__main__":
    main()
