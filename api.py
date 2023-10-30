from flask import Flask, request, jsonify,send_file
import re
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
app = Flask(__name__)
otpvar = {}


import os
download_dir = os.getcwd()

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True
})

# Create a Chrome driver with the configured options
driver = webdriver.Chrome(options=chrome_options)








@app.route('/signup', methods=['POST'])
def signup():
    global driver,otpvar
    try:

        data = request.get_json()
        number = data.get('mobile_number')
        firstName = data.get('firstname')
        password = data.get('password')
        driver.get("https://voters.eci.gov.in/signup")
        time.sleep(5)
        driver.find_element(By.NAME, 'mobile_number').send_keys(number)
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

        driver.find_element(By.NAME, "captcha").send_keys(image_text)

        driver.find_element(By.CLASS_NAME, "btn.library-btn.btn-block.submit").click()

        time.sleep(1)
        er = driver.find_element(By.CLASS_NAME, "alert_global").text.strip()
        print(er)
        if er:
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

            driver.find_element(By.NAME, "captcha").send_keys(image_text)

            driver.find_element(By.CLASS_NAME, "btn.library-btn.btn-block.submit").click()

        time.sleep(5)
        driver.find_element(By.NAME, "firstName").send_keys(firstName)

        driver.find_element(By.NAME, "password").send_keys(password)

        driver.find_element(By.NAME, "confirmpassword").send_keys(password)

        driver.find_element(By.CLASS_NAME, "btn.library-btn.btn-block.submit1").click()
        time.sleep(40)

        while otpvar.get(number,None) is None:
            time.sleep(2)
        otp = otpvar.get(number)
        driver.find_element(By.NAME, "otp1").send_keys(otp)
        otpvar[number]=None
        driver.find_element(By.CLASS_NAME, "btn.library-btn.btn-block.submit.mt-4").click()
        return {"signup" : "success"}
    except:
        return {"signup": "failed"}

@app.route('/login', methods=['POST'])
def login():
    global driver, otpvar
    try:
        # Get input data from query parameters in the URL
        mobile_number = request.args.get('mobile_number')
        password = request.args.get('password')

        driver.get("https://voters.eci.gov.in/login")
        time.sleep(3)
        driver.find_element(By.NAME, "mobOrEpic").send_keys(mobile_number)
        driver.find_element(By.NAME, "password").send_keys(password)
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
        time.sleep(1)
        er = driver.find_element(By.CLASS_NAME, "alert_global").text.strip()
        print(er)
        if er:
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

            driver.find_element(By.NAME, "captcha").send_keys(image_text)

            driver.find_element(By.CLASS_NAME, "btn.library-btn.btn-block.submit").click()

        time.sleep(40)
        while otpvar.get(mobile_number, None) is None:
            time.sleep(2)
        otp = otpvar.get(mobile_number)

        otpvar[mobile_number] = None
        driver.find_element(By.NAME, "otp1").send_keys(otp.strip())

        driver.find_element(By.CLASS_NAME, "btn.library-btn.btn-block.submit.mt-4").click()
        return {"login":"success"}
    except:
        return {"login": "failed"}

@app.route('/download', methods=['POST'])
def download():
    try:
        global driver,otpvar
        data = request.get_json()
        epic_number = data.get('epic_number')
        state_option = data.get('state_option')

        driver.get("https://voters.eci.gov.in/Homepage")
        time.sleep(2)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "e-epic-download-box.card-zoom.e-epic-download-card-height"))
        )

        driver.find_element(By.CLASS_NAME, "e-epic-download-box.card-zoom.e-epic-download-card-height").click()
        time.sleep(7)
        # driver.get("https://voters.eci.gov.in/home/e-epic-download")
        epic = epic_number
        driver.find_element(By.NAME, "epicNo").send_keys(epic.strip())
        select = Select(driver.find_element(By.NAME, "stateValue"));
        options = select.options

        optext = [i.text for i in options[1:]]

        for i, pt in enumerate(optext):
            print(i + 1, pt)

        select.select_by_index(int(state_option))

        driver.find_element(By.CLASS_NAME, "btn.btn-primary.btn-sm.searchbuttonreport").click()
        time.sleep(5)
        WebDriverWait(driver, 7).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'btn.btn-primary.btn-sm')))
        driver.find_elements(By.CLASS_NAME, "btn.btn-primary.btn-sm")[-1].click()
        time.sleep(40)
        while otpvar.get(epic_number, None) is None:
            time.sleep(2)
        otp = otpvar.get(epic_number)

        otpvar['epic_number']=None

        driver.find_element(By.NAME, "otpValue").send_keys(otp.strip())
        time.sleep(4)
        driver.find_elements(By.CLASS_NAME, "btn.btn-primary")[-1].click()
        time.sleep(10)

        driver.find_elements(By.CLASS_NAME, "btn.btn-primary.mx-3")[-1].click()
        time.sleep(5)
        epic_pattern = re.compile(r'e-EPIC_WPN(\d+)(?: \((\d+)\))?.pdf')
        epic_files = [f for f in os.listdir(download_dir) if epic_pattern.match(f)]
        epic_files = [f for f in epic_files if re.search(epic_number, f)]
        latest_epic_pdf = None
        latest_epic_version = -1

        for file in epic_files:
            match = epic_pattern.match(file)
            epic_version = int(match.group(2)) if match.group(2) else 0
            if epic_version > latest_epic_version:
                latest_epic_version = epic_version
                latest_epic_pdf = file

        return send_file(
            latest_epic_pdf,
            as_attachment=True,
            download_name=latest_epic_pdf
        )
    except:
        return {"download":'failed'}

@app.route('/correction', methods=['POST'])
def correction():
    global driver,otpvar
    try:
        data = request.get_json()
        epic_number = data.get('epic_number')
        phone_number = data.get('phone_number')
        place = data.get('place')
        driver.get("https://voters.eci.gov.in/form8")
        time.sleep(10)
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.NAME, 'applicationFor'))
        )
        elements[-1].click()

        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.NAME, 'popupEpic'))
        )
        epic = epic_number
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
        phone = phone_number
        driver.find_element(By.NAME, "PartDmobile").send_keys(phone.strip())
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, "btn.library-btn.btn-primary.send-otp").click()
        time.sleep(40)
        while otpvar.get(phone_number,None) is None:
            time.sleep(2)
        otp = otpvar.get(phone_number)

        otpvar[phone_number]=None
        driver.find_element(By.NAME, "enterOTP").send_keys(otp.strip())

        driver.find_elements(By.CLASS_NAME, "btn.library-btn.btn-primary.send-otp")[-1].click()
        time.sleep(3)
        driver.find_elements(By.CLASS_NAME, "btn.library-btn.buttonVisible.next-btn")[5].click()

        place = place
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

        driver.find_element(By.NAME, "captcha").send_keys(image_text)

        driver.find_elements(By.CLASS_NAME, "btn.library-btn.buttonVisible.preview-btn")[-1].click()
        time.sleep(1)
        er = driver.find_element(By.CLASS_NAME, "alert_global").text.strip()
        print(er)
        if er:
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

            driver.find_element(By.NAME, "captcha").send_keys(image_text)

            driver.find_elements(By.CLASS_NAME, "btn.library-btn.buttonVisible.preview-btn")[-1].click()

        time.sleep(3)

        driver.find_element(By.CLASS_NAME, "btn.library-btn.buttonVisible.btn_form6A").click()
        time.sleep(3)
        driver.find_element(By.CLASS_NAME, "btn.btn-primary").click()
        time.sleep(3)
        driver.find_elements(By.CLASS_NAME, "btn.library-btn.btn-ok")[1].click()
        time.sleep(3)
        return {'correction':"success"}
    except:
        return {'correction': "failed"}

@app.route('/otp', methods=['POST'])
def otp():
    global otpvar

    data = request.get_json()
    mobile_number = data.get('number')
    otp = data.get('otp')
    otpvar[mobile_number] = otp
    return {"message": "OTP set successfully",
            mobile_number:otp}

@app.route('/refresh')
def refresh():
    global driver
    driver.refresh()
    return {'refresh':"Done"}

if __name__ == "__main__":
    app.run()
