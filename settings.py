import platform
import os

OS = platform.system()
os.chmod('ChromeDrivers/chromedriver', 0o0755)
chrome_driver_dir = None	