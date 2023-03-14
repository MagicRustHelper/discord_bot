from dotenv import load_dotenv

from app.bot import MRHelperBot
from app.core import logs

logs.add_debug_file_log()
logs.add_info_file_log()

load_dotenv('.env')


bot = MRHelperBot()
bot.run()
