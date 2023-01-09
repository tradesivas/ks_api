import requests
import os
from dotenv import load_dotenv
load_dotenv()
fno_url = os.getenv("fno_url")
cash_url = os.getenv("cash_url")
fno_file = os.getenv("fno_file")
cash_file = os.getenv("cash_file")
fno = requests.get(fno_url, allow_redirects=True)
open(fno_file, 'wb').write(fno.content)
cash = requests.get(cash_url, allow_redirects=True)
open(cash_file, 'wb').write(cash.content)