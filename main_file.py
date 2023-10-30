from bestcaptchasolverapi3.bestcaptchasolverapi import BestCaptchaSolverAPI
import warnings
warnings.filterwarnings("ignore")

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time, base64
from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By

def login(driver):
    driver.get("https://voters.eci.gov.in/login")

    driver.find_element(By.NAME, "mobOrEpic").send_keys("8290979975")
    driver.find_element(By.NAME, "password").send_keys("Saini@2022")

    time.sleep(3)
    captcha = driver.find_element(By.CLASS_NAME, 'col-md-auto.mr-0.p-0').find_element(By.TAG_NAME, 'img')
    img_captcha_base64 = driver.execute_script("""
                                                var ele = arguments[0];
                                                var cnv = document.createElement('canvas');
                                                cnv.width = ele.width; cnv.height = ele.height;
                                                cnv.getContext('2d').drawImage(ele, 0, 0);
                                                return cnv.toDataURL('image/png').substring(22);    
                                                """, captcha)
    with open(r"captcha.png", 'wb') as f:
        f.write(base64.b64decode(img_captcha_base64))

    data = {}
    data['image'] = 'captcha.png'
    access_token = 'AB79DD39EC38466DBFB1B982FCA92840'
    # get your access token from https://bestcaptchasolver.com/account
    bcs = BestCaptchaSolverAPI(access_token)
    captcha_id = bcs.submit_image_captcha(data)

    image_text = bcs.retrieve(captcha_id)['text']

    driver.find_element(By.NAME, "captcha").send_keys(image_text)
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, "btn.library-btn.btn-block.submit").click()
    otp = input("Enter OTP : ")
    driver.find_element(By.NAME, "otp1").send_keys(otp.strip())

    driver.find_element(By.CLASS_NAME, "btn.library-btn.btn-block.submit.mt-4").click()

def download(driver):
    WebDriverWait(driver, 6).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "e-epic-download-box.card-zoom.e-epic-download-card-height"))
    )

    driver.find_element(By.CLASS_NAME, "e-epic-download-box.card-zoom.e-epic-download-card-height").click()
    
    #driver.get("https://voters.eci.gov.in/home/e-epic-download")
    epic = input("Enter EpicNO : ")
    driver.find_element(By.NAME, "epicNo").send_keys(epic.strip())
    select = Select(driver.find_element(By.NAME, "stateValue"));
    options = select.options

    optext = [i.text for i in options[1:]]

    for i,pt in enumerate(optext):
        print(i+1,pt)
    ind = input(f"Enter option number between 1 - {len(optext)} : ")
    select.select_by_index(int(ind.strip()))

    driver.find_element(By.CLASS_NAME, "btn.btn-primary.btn-sm.searchbuttonreport").click()
    time.sleep(5)
    WebDriverWait(driver, 4).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'btn.btn-primary.btn-sm')))
    driver.find_elements(By.CLASS_NAME,"btn.btn-primary.btn-sm")[-1].click()

    otp = input("Enter OTP : ")
    driver.find_element(By.NAME,"otpValue").send_keys(otp.strip())
    time.sleep(4)
    driver.find_elements(By.CLASS_NAME,"btn.btn-primary")[-1].click()
    time.sleep(10)

    driver.find_elements(By.CLASS_NAME,"btn.btn-primary.mx-3")[-1].click()

def correction(driver):
    driver.get("https://voters.eci.gov.in/form8")
    time.sleep(10)
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.NAME, 'applicationFor'))
    )
    elements[-1].click()

    WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.NAME, 'popupEpic'))
    )
    epic = input("Enter EpicNO : ")
    driver.find_elements(By.NAME, "popupEpic")[-1].send_keys(epic.strip())

    driver.find_elements(By.CLASS_NAME, "btn.btn-primary.mr-0")[-1].click()

    time.sleep(15)
    try:
        driver.find_elements(By.CLASS_NAME, "buttonVisible.preview-btn")[-1].click()
    except:
        time.sleep(15)
        driver.find_elements(By.CLASS_NAME, "buttonVisible.preview-btn")[-1].click()
    time.sleep(5)
    driver.find_elements(By.ID, "correction")[-1].click()

    driver.find_elements(By.CLASS_NAME, "btn.btn-primary.mr-0")[-1].click()
    time.sleep(4)
    driver.find_element(By.ID, "mobileno").click()
    phone = input("Enter Phone number : ")
    driver.find_element(By.NAME, "PartDmobile").send_keys(phone.strip())
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, "btn.library-btn.btn-primary.send-otp").click()
    
    otp = input("Enter OTP : ")
    driver.find_element(By.NAME, "enterOTP").send_keys(otp.strip())

    driver.find_elements(By.CLASS_NAME, "btn.library-btn.btn-primary.send-otp")[-1].click()
    time.sleep(3)
    driver.find_elements(By.CLASS_NAME, "btn.library-btn.buttonVisible.next-btn")[5].click()

    place = input("Enter Place")
    driver.find_element(By.NAME, "place").send_keys(place.strip())

    driver.find_elements(By.CLASS_NAME, "btn.library-btn.buttonVisible.next-btn")[-1].click()
    time.sleep(2)
    captcha = driver.find_element(By.CLASS_NAME, 'col-md-auto.mr-0.p-0').find_element(By.TAG_NAME, 'img')
    img_captcha_base64 = driver.execute_script("""
                                                var ele = arguments[0];
                                                var cnv = document.createElement('canvas');
                                                cnv.width = ele.width; cnv.height = ele.height;
                                                cnv.getContext('2d').drawImage(ele, 0, 0);
                                                return cnv.toDataURL('image/png').substring(22);    
                                                """, captcha)
    with open(r"captcha.png", 'wb') as f:
        f.write(base64.b64decode(img_captcha_base64))
    data = {}
    data['image'] = 'captcha.png'
    access_token = 'AB79DD39EC38466DBFB1B982FCA92840'
    bcs = BestCaptchaSolverAPI(access_token)

    captcha_id = bcs.submit_image_captcha(data)

    image_text = bcs.retrieve(captcha_id)['text']

    driver.find_element(By.NAME,"captcha").send_keys(image_text)

    driver.find_elements(By.CLASS_NAME, "btn.library-btn.buttonVisible.preview-btn")[-1].click()
    time.sleep(3)

    driver.find_element(By.CLASS_NAME, "btn.library-btn.buttonVisible.btn_form6A").click()
    time.sleep(3)
    driver.find_element(By.CLASS_NAME, "btn.btn-primary").click()
    time.sleep(3)
    driver.find_elements(By.CLASS_NAME, "btn.library-btn.btn-ok")[1].click()
    time.sleep(3)

if __name__ =="__main__":
    driver = webdriver.Chrome()
    login(driver)
    time.sleep(5)
    print("login")
    
    #correction(driver)
    time.sleep(5)
    download(driver)
