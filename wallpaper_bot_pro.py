import asyncio
import random
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError
import aiohttp
import os

# ========== الإعدادات ==========
BOT_TOKEN = "8475807409:AAHNj5nCT4BnwOrMSHoviStSUDgRwn_QO4g"
CHANNEL_USERNAME = "@MobWallpaper4k"

# فئات الخلفيات
CATEGORIES = [
    "nature", "abstract", "minimal", "dark", "space", "ocean", 
    "mountains", "sunset", "city", "technology", "cars", "architecture",
    "animals", "flowers", "forest", "beach", "night", "art"
]

# مصادر الخلفيات المجانية
WALLPAPER_SOURCES = [
    "https://source.unsplash.com/1080x1920/?{category},wallpaper",
    "https://picsum.photos/1080/1920?random={random}",
    "https://source.unsplash.com/random/1080x1920/?{category}",
]

class WallpaperBot:
    def __init__(self):
        self.bot = Bot(token=BOT_TOKEN)
        self.post_count = 0
        
    async def download_wallpaper(self):
        """تحميل خلفية من مصدر عشوائي"""
        category = random.choice(CATEGORIES)
        
        # تجربة مصادر مختلفة
        for attempt in range(3):
            try:
                source = random.choice(WALLPAPER_SOURCES)
                url = source.format(
                    category=category,
                    random=random.randint(1, 100000)
                )
                
                print(f"🔍 محاولة التحميل من: {url[:50]}...")
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=30) as response:
                        if response.status == 200:
                            image_data = await response.read()
                            
                            # التحقق من حجم الصورة
                            if len(image_data) > 10000:  # أكبر من 10KB
                                print(f"✅ تم التحميل بنجاح - الحجم: {len(image_data)/1024:.1f}KB")
                                return image_data, category
                            
                print(f"⚠️ المحاولة {attempt + 1} فشلت، إعادة المحاولة...")
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"❌ خطأ في المحاولة {attempt + 1}: {e}")
                await asyncio.sleep(2)
        
        return None, None
    
    def create_caption(self, category):
        """إنشاء وصف جذاب للمنشور"""
        
        emojis_map = {
            "nature": ["🌿", "🌲", "🍃", "🌱"],
            "abstract": ["🎨", "✨", "🌈", "💫"],
            "minimal": ["⚪", "⚫", "🔲", "▫️"],
            "dark": ["🌑", "🖤", "⬛", "🌚"],
            "space": ["🌌", "🚀", "🪐", "⭐"],
            "ocean": ["🌊", "🐚", "🌴", "🏝️"],
            "mountains": ["🏔️", "⛰️", "🗻", "🏕️"],
            "sunset": ["🌅", "🌇", "🌄", "🌆"],
            "city": ["🌃", "🏙️", "🌆", "🏗️"],
            "technology": ["💻", "🔮", "⚡", "🤖"],
            "cars": ["🚗", "🏎️", "🚙", "🏁"],
            "architecture": ["🏛️", "🏰", "🕌", "🏢"],
            "animals": ["🦁", "🐾", "🦅", "🐺"],
            "flowers": ["🌸", "🌺", "🌻", "🌷"],
            "forest": ["🌲", "🦌", "🍄", "🌳"],
            "beach": ["🏖️", "🌊", "☀️", "🐚"],
            "night": ["🌙", "⭐", "🌃", "✨"],
            "art": ["🎨", "🖼️", "🎭", "✨"]
        }
        
        emoji = random.choice(emojis_map.get(category, ["📱", "🖼️"]))
        
        templates = [
            f"{emoji} خلفية {category} خرافية",
            f"{emoji} اجمل خلفيات {category}",
            f"{emoji} خلفية اليوم - {category}",
            f"{emoji} حمّل هذه الروعة الآن",
            f"{emoji} خلفية {category} حصرية",
            f"{emoji} جدد شكل هاتفك",
        ]
        
        caption = random.choice(templates)
        caption += "\n\n"
        caption += random.choice([
            "🔥 جودة عالية HD\n",
            "⚡ دقة فائقة\n",
            "✨ تصميم احترافي\n",
            "💎 خلفية مميزة\n"
        ])
        caption += f"📥 حمّل الآن | @MobWallpaper4k\n"
        caption += f"🎯 خلفية #{self.post_count + 1}"
        
        return caption
    
    async def post_wallpaper(self):
        """نشر الخلفية في القناة"""
        try:
            print("\n" + "="*60)
            print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*60)
            
            # تحميل الخلفية
            image_data, category = await self.download_wallpaper()
            
            if not image_data:
                print("❌ فشل تحميل الخلفية من جميع المصادر")
                return False
            
            # حفظ مؤقت
            temp_file = f"wallpaper_{datetime.now().timestamp()}.jpg"
            with open(temp_file, 'wb') as f:
                f.write(image_data)
            
            # إنشاء الوصف
            caption = self.create_caption(category)
            
            # النشر
            print(f"📤 نشر في القناة...")
            with open(temp_file, 'rb') as photo:
                await self.bot.send_photo(
                    chat_id=CHANNEL_USERNAME,
                    photo=photo,
                    caption=caption,
                    read_timeout=30,
                    write_timeout=30
                )
            
            # حذف الملف المؤقت
            os.remove(temp_file)
            
            self.post_count += 1
            print(f"✅ نجح النشر! إجمالي المنشورات: {self.post_count}")
            print(f"📊 الفئة: {category}")
            print("="*60)
            
            return True
            
        except TelegramError as e:
            print(f"❌ خطأ تيليغرام: {e}")
            return False
        except Exception as e:
            print(f"❌ خطأ عام: {e}")
            return False
    
    async def run(self):
        """تشغيل البوت"""
        print("╔" + "="*58 + "╗")
        print("║" + " "*15 + "🤖 بوت خلفيات الموبايل" + " "*15 + "║")
        print("╚" + "="*58 + "╝")
        print(f"\n📢 القناة: {CHANNEL_USERNAME}")
        print(f"⏰ معدل النشر: كل 3 ساعات")
        print(f"🎨 عدد الفئات: {len(CATEGORIES)}")
        print(f"🚀 البوت جاهز للعمل!\n")
        print("-"*60)
        
        # نشر أول خلفية فوراً
        print("🎬 نشر أول خلفية...")
        await self.post_wallpaper()
        
        while True:
            try:
                # الانتظار 3 ساعات
                next_post = datetime.now().timestamp() + 10800
                next_post_time = datetime.fromtimestamp(next_post).strftime('%H:%M:%S')
                
                print(f"\n⏳ المنشور التالي في الساعة: {next_post_time}")
                print(f"💤 وضع السكون لمدة 3 ساعات...\n")
                
                await asyncio.sleep(10800)  # 3 ساعات
                
                # نشر خلفية جديدة
                success = await self.post_wallpaper()
                
                if not success:
                    print("⚠️ فشل النشر، إعادة المحاولة بعد 5 دقائق...")
                    await asyncio.sleep(300)
                    
            except KeyboardInterrupt:
                print("\n\n⛔ تم إيقاف البوت بواسطة المستخدم")
                break
            except Exception as e:
                print(f"\n❌ خطأ في الحلقة الرئيسية: {e}")
                print("🔄 إعادة المحاولة بعد دقيقة...")
                await asyncio.sleep(60)

async def test_bot():
    """اختبار سريع للبوت"""
    print("🧪 وضع الاختبار - نشر خلفية واحدة فقط\n")
    bot = WallpaperBot()
    success = await bot.post_wallpaper()
    if success:
        print("\n✅ الاختبار نجح! البوت يعمل بشكل صحيح")
    else:
        print("\n❌ الاختبار فشل! تحقق من الإعدادات")

async def main():
    """النقطة الرئيسية لتشغيل البوت"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        await test_bot()
    else:
        bot = WallpaperBot()
        await bot.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 وداعاً!")
