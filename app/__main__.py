from dotenv import load_dotenv

from app.bot import MRHelperBot

load_dotenv('.env')


bot = MRHelperBot()
bot.run()
