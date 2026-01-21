import asyncio
import random
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError
import aiohttp
import os

# إعدادات البوت
BOT_TOKEN = "8475807409:AAHNj5nCT4BnwOrMSHoviStSUDgRwn_QO4g"
CHANNEL_USERNAME = "@MobWallpaper4k"

# مفاتيح API المجانية (لا تحتاج تسجيل)
UNSPLASH_ACCESS_KEY = "your_unsplash_key_here"  # احصل عليه من unsplash.com/developers (مجاني)
PEXELS_API_KEY = "your_pexels_key_here"  # احصل عليه من pexels.com/api (مجاني)

# فئات الخلفيات
WALLPAPER_CATEGORIES = [
    "nature", "abstract", "minimal", "dark", "space", "ocean", 
    "mountains", "sunset", "city", "technology", "animals", "flowers"
]

class WallpaperBot:
    def __init__(self):
        self.bot = Bot(token=BOT_TOKEN)
        
    async def get_unsplash_wallpaper(self):
        """جلب خلفية من Unsplash"""
        try:
            category = random.choice(WALLPAPER_CATEGORIES)
            # استخدام API بدون مفتاح (محدود لكن يعمل للتجربة)
            url = f"https://source.unsplash.com/1080x1920/?{category},wallpaper"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        image_data = await response.read()
                        return image_data, category
        except Exception as e:
            print(f"خطأ في جلب من Unsplash: {e}")
        return None, None
    
    async def get_pexels_wallpaper(self):
        """جلب خلفية من Pexels (بدون API key - طريقة بديلة)"""
        try:
            category = random.choice(WALLPAPER_CATEGORIES)
            # استخدام Picsum للحصول على صور عشوائية عالية الجودة
            url = f"https://picsum.photos/1080/1920?random={random.randint(1, 10000)}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        image_data = await response.read()
                        return image_data, category
        except Exception as e:
            print(f"خطأ في جلب الصورة: {e}")
        return None, None
    
    def generate_caption(self, category):
        """إنشاء وصف للمنشور"""
        emojis = {
            "nature": "🌿🌲",
            "abstract": "🎨✨",
            "minimal": "⚪️⚫️",
            "dark": "🌑🖤",
            "space": "🌌🚀",
            "ocean": "🌊🐚",
            "mountains": "🏔️⛰️",
            "sunset": "🌅🌇",
            "city": "🌃🏙️",
            "technology": "💻🔮",
            "animals": "🦁🐾",
            "flowers": "🌸🌺"
        }
        
        emoji = emojis.get(category, "📱")
        
        captions = [
            f"{emoji} خلفية {category} جديدة لهاتفك",
            f"{emoji} استمتع بهذه الخلفية الرائعة",
            f"{emoji} خلفية اليوم - {category}",
            f"{emoji} أضف لمسة جمالية لشاشتك"
        ]
        
        caption = random.choice(captions)
        caption += "\n\n🔥 @MobWallpaper4k\n📥 حمّل الآن!"
        
        return caption
    
    async def post_wallpaper(self):
        """نشر خلفية في القناة"""
        try:
            # محاولة جلب من مصادر مختلفة
            image_data, category = await self.get_unsplash_wallpaper()
            
            if not image_data:
                image_data, category = await self.get_pexels_wallpaper()
            
            if image_data:
                caption = self.generate_caption(category or "mobile")
                
                # حفظ الصورة مؤقتاً
                temp_file = f"temp_wallpaper_{datetime.now().timestamp()}.jpg"
                with open(temp_file, 'wb') as f:
                    f.write(image_data)
                
                # نشر في القناة
                with open(temp_file, 'rb') as photo:
                    await self.bot.send_photo(
                        chat_id=CHANNEL_USERNAME,
                        photo=photo,
                        caption=caption
                    )
                
                # حذف الملف المؤقت
                os.remove(temp_file)
                
                print(f"✅ تم نشر خلفية بنجاح - {datetime.now()}")
                return True
            else:
                print("❌ فشل جلب الخلفية")
                return False
                
        except TelegramError as e:
            print(f"❌ خطأ في التيليغرام: {e}")
            return False
        except Exception as e:
            print(f"❌ خطأ عام: {e}")
            return False
    
    async def run(self):
        """تشغيل البوت"""
        print("🤖 بوت الخلفيات يعمل الآن!")
        print(f"📢 القناة: {CHANNEL_USERNAME}")
        print(f"⏰ النشر كل 3 ساعات")
        print("-" * 50)
        
        while True:
            try:
                await self.post_wallpaper()
                # الانتظار 3 ساعات (10800 ثانية)
                print(f"⏳ الانتظار 3 ساعات حتى المنشور التالي...")
                await asyncio.sleep(10800)
            except Exception as e:
                print(f"❌ خطأ في الحلقة الرئيسية: {e}")
                # في حالة الخطأ، انتظر 10 دقائق ثم حاول مجدداً
                await asyncio.sleep(600)

async def main():
    bot = WallpaperBot()
    await bot.run()

if __name__ == "__main__":
    print("🚀 بدء تشغيل بوت خلفيات الموبايل...")
    asyncio.run(main())
