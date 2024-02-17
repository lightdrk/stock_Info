import time
from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.chrome.service import Service

class Scrap:
    ''' scraps data (like charts screenshot etc ) from trading view '''
    def __init__(self):
        chrome_options = Options()
        chrome_options.headless = False
        self.driver = webdriver.Chrome(options=chrome_options)

    def retrive(self, url):
        ''' retrives data from tranding view '''
        if url.find('.com') == -1:
            name = url
            url = f'https://in.tradingview.com/chart/?symbol={url}'
        else:
            print(url)

        try:
            self.driver.get(url)
        except Exception as err:
            print(f'Issue Opening {err}')

        wait = WebDriverWait(self.driver,100)
        time.sleep(3)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.container-hw_3o_pb')))
        script ='''
        function data(){
            let x = document.getElementsByClassName('buttonText-hw_3o_pb');
            return [x[0].innerText, x[1].innerText];
        }

        return data()'''

        try:
            output = self.driver.execute_script(script)
        except Exception as err:
            print(f'1st script Excecution error :{err}')

        script_button ='''
        function data(){{
            let button = document.getElementsByClassName("item-SqYYy1zF button-GwQQdU8S apply-common-tooltip isInteractive-GwQQdU8S accessible-GwQQdU8S")
            button[{val}].click();
            return 1
        }}

        return data()'''

        for val in [0,1,2]:
            try:
                self.driver.execute_script(script_button.format(val=val))
            except Exception as err:
                print(f'x- ++__++ {val} ++__++ -x-script-x Excecution error :{err}')

            time.sleep(2)
            try:
                print(name)
                self.driver.save_screenshot(f'./image_output/{name}{val}.png')
            except Exception as err:
                print(f'error while taking screeshot :{err}')

        return output

    def exit(self):
        ''' exit the browser safely '''
        self.driver.quit()

'''
x = Scrap()

print(x.retrive('https://in.tradingview.com/chart/?symbol=NSE%3AHDFCBANK'))
time.sleep(10)
print(x.retrive('https://in.tradingview.com/chart/?symbol=NSE%3ATECHNOE'))
'''
