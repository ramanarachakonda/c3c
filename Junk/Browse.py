import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())


url = 'https://maps.arcgis.com/apps/MapSeries/index.html?appid=c2efd1898e48452e83d7218329e953d7'
#'https://www.nj.gov/health/cd/topics/covid2019_dashboard.shtml'
clicable = '/html/body/div[3]/div/div[1]/ul/li[3]/button'
#'//*[@id="nav-bar"]/div/div[1]/ul/li[3]/button'
div = '/html/body/div/div/div[2]/div/div'

def grab_html(url, clicable, div):
    driver.get(url)
    print(12)
    time.sleep(12)
    print('try')
    driver.execute_script("""document.querySelector("#nav-bar > div > div.entries > ul > li:nth-child(3) > button")""")
    print(2)
    time.sleep(2)
    print('try')
    driver.execute_script("""document.querySelector("#nav-bar > div > div.entries > ul > li:nth-child(3) > button")""")
    print(2)
    time.sleep(2)
    print('now')
    driver.execute_script('''document.body.querySelector("#nav-bar > div > div.entries > ul > li:nth-child(3) > button").click()''')
    time.sleep(10)
    driver.get_screenshot_as_file('screen.png')
    

grab_html(url, clicable, div)
    
