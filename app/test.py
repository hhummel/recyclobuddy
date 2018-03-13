import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from mysite import passwords

print(passwords.EMAIL_PASSWORD)
