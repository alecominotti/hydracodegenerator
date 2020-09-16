from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import CodeGenerator, HCGArgumentHandler
import selenium
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import ctypes
import json
import os, glob
import platform
import random

def index(request):
    version="v1.0"
    txtpath="generatedCodeHistory.txt"
    default_url = "https://hydra.ojack.xyz"
    args = HCGArgumentHandler()
    default_fmin = 5
    default_fmax = 10
    hydra = CodeGenerator(ignoredList=[], exclusiveSourceList=[], exclusiveFunctionList=[])
    allSources = hydra.getSourcesList()
    allFunctions = hydra.getAllFunctions()
    defaultIgnoredList = hydra.getIgnoredList()
    defaultExclusiveSources = hydra.getExclusiveSourceList()
    defaultExclusiveFunctions = hydra.getExclusiveFunctionList()

    if request.method == 'GET': # First time on site
        global driver
        request.session['runningOnLinux'] = platform.system()=='Linux'
        request.session['runningOnMac'] = platform.system()=='Darwin'
        request.session['runningOnWindows']  = platform.system()=='Windows'
        if(request.session['runningOnMac']):
            request.session['control_key'] = Keys.COMMAND
        else:
            request.session['control_key'] = Keys.CONTROL
        if('webdriver' in request.session):
            driver = get_object_by_id(request.session['webdriver'])
            #if isinstance(driver, selenium.webdriver.chrome.webdriver.WebDriver):
                #driver.quit()
            del request.session['webdriver']
            #for filename in glob.glob("hcg_app/__pycache__/*cpython*"):
            #    os.remove(filename) 
        args.set_fmin( default_fmin )
        args.set_fmax( default_fmax )
        args.set_amin( hydra.getMinValue() )
        args.set_amax( hydra.getMaxValue() )
        args.set_arrow_prob( hydra.getArrowFunctionProb() )
        args.set_mouse_prob( hydra.getMouseFunctionProb() )
        args.set_modulate_itself_prob( hydra.getModulateItselfProb() )
        args.set_ignore_list( hydra.getIgnoredList() )
        args.set_exclusive_source_list( hydra.getExclusiveSourceList() )
        args.set_exclusive_function_list( hydra.getExclusiveFunctionList() )

    elif(request.method == 'POST'): # AJAX REQUESTS FROM HERE
        data=request.POST
        return_data= { }
        hidecodestatus = data['hidecodestatus']
        if ('live_switch' in data): # START OR END LIVE SESSION MODE
            if not ('webdriver' in request.session): # STARTS LIVE SESSION MODE
                driverpath = setWebDriverPath(request)
                print("Opening Web driver: '" + driverpath + "'...")
                url = data['hydraurl'] + "/?code=" + hydra.encodeText(data['code'])
                caps = webdriver.DesiredCapabilities.CHROME.copy()
                caps['acceptInsecureCerts'] = True
                driver = webdriver.Chrome(executable_path=driverpath, desired_capabilities=caps)
                driver.get(url)
                request.session['webdriver'] = id(driver)

                if(hidecodestatus=="1"):
                    hideCodeKeys(request)
                print("Live Session Started")
            else: # ENDS LIVE SESSION MODE
                driver = get_object_by_id(request.session['webdriver'])
                if isinstance(driver, selenium.webdriver.chrome.webdriver.WebDriver):
                    driver.quit()
                del request.session['webdriver']
                print("Live Session Finished")
        elif('send_code' in data) and (data['live_session_mode']=="1"): # just run textarea code to hydra
            print("Executing code in Hydra...")
            if hidecodestatus=="1": # To show it
                hideCodeKeys(request)
            driver = get_object_by_id(request.session['webdriver'])
            executeCodeKeys(request, driver, data['code'])
            if hidecodestatus=="1": # To hide it
                hideCodeKeys(request)
        elif not ('send_code' in data):
            print("Generating new code...")
            #Code generation for AJAX requests
            if(data['fmin']):
                args.set_fmin(int(data['fmin']))
                if not data['fmax']:
                    args.set_fmax(int(data['fmin']))
                elif int(data['fmin']) > int(data['fmax']):
                    args.set_fmin(int(data['fmax']))

            if(data['fmax']):
                if(args.get_fmin() > int(data['fmax'])):
                    args.set_fmin(int(data['fmax']))
                else:
                    args.set_fmax(int(data['fmax']))

            if(data['amin']):
                args.set_amin(float(data['amin']))
                if not data['amax']:
                    args.set_amax(float(data['amin']))
                elif float(data['amin']) > float(data['amax']):
                    args.set_amin(float(data['amax']))

            if(data['amax']):
                if(args.get_amin() > float(data['amax'])):
                    args.set_amin(float(data['amax']))
                else:
                    args.set_amax(float(data['amax']))

            if(data['arrowprob']):
                if int(data['arrowprob']) < 0:
                    args.set_arrow_prob(0)
                elif int(data['arrowprob']) > 100:
                    args.set_arrow_prob(100)
                else:
                    args.set_arrow_prob(int(data['arrowprob']))
            
            if(data['mouseprob']):
                if int(data['mouseprob']) < 0:
                    args.set_mouse_prob(0)
                elif int(data['mouseprob']) > 100:
                    args.set_mouse_prob(100)
                else:
                    args.set_mouse_prob(int(data['mouseprob']))
            
            if(data['modulateitselfprob']):
                if int(data['modulateitselfprob']) < 0:
                    args.set_modulate_itself_prob(0)
                elif int(data['modulateitselfprob']) > 100:
                    args.set_modulate_itself_prob(100)
                else:
                    args.set_modulate_itself_prob(int(data['modulateitselfprob']))

            if('ignored' in data):
                args.set_ignore_list(data['ignored'].split(","))
            if('exclusivesources' in data):
                args.set_exclusive_source_list(data['exclusivesources'].split(","))
            if('exclusivefunctions' in data):
                args.set_exclusive_function_list(data['exclusivefunctions'].split(","))

            hydra = CodeGenerator(args.get_amin(), args.get_amax(), args.get_arrow_prob(), args.get_mouse_prob(), args.get_modulate_itself_prob(), args.get_ignore_list(), args.get_exclusive_source_list(), args.get_exclusive_function_list())
            hydraCode= hydra.generateCode(args.get_fmin(), args.get_fmax())   
            save_code_to_history(txtpath, hydra.getInfo(), hydraCode)
            return_data['code'] = hydraCode

            if(data['live_session_mode']=="1") and (data['auto_send_status']=="1"): #writes to an already open live session
                print("Executing code in Hydra...")
                if hidecodestatus=="1": # To show it
                    hideCodeKeys(request)
                driver = get_object_by_id(request.session['webdriver'])
                executeCodeKeys(request, driver, hydraCode)
                if hidecodestatus=="1": # To hide it
                    hideCodeKeys(request)
        print("Done")
        return_data = json.dumps(return_data)
        return HttpResponse(return_data, content_type="application/json") #return for AJAX requests only

    #Context for GET requests:
    hydraCode= hydra.generateCode(args.get_fmin(), args.get_fmax())
    save_code_to_history(txtpath, hydra.getInfo(), hydraCode)  
    context = {
        'code': hydraCode,
        'fmin': args.get_fmin(),
        'fmax': args.get_fmax(),
        'amin': args.get_amin(),
        'amax': args.get_amax(),
        'arrowprob' : args.get_arrow_prob(),
        'mouseprob' : args.get_mouse_prob(),
        'modulateitselfprob': args.get_modulate_itself_prob(),
        'ignoreList' : args.get_ignore_list(),
        'defaultignorelist' : defaultIgnoredList,
        'defaultexclusivesources' : defaultExclusiveSources,
        'defaultexclusivefunctions' : defaultExclusiveFunctions,
        'exclusiveSourcesList' : args.get_exclusive_source_list(),
        'exclusiveFunctionsList' : args.get_exclusive_function_list(),
        'allsources' : allSources,
        'allfunctions' : allFunctions,
        'sourcesandfunctions' : allSources + allFunctions,
        'defaulturl' : default_url,
        'version' : version,
        'random' : random.randint(0, 999999999)
    }

    template = "hcg_app/content.html"
    print("Done")
    return render(request, template, context) #return for GET requests only


def setWebDriverPath(request):
    webDriversRootFolder = "webdrivers/"
    if request.session['runningOnLinux']:
        driverpath = webDriversRootFolder + "linux/chromedriver"
        os.system("chmod +rwx " + driverpath)
    elif request.session['runningOnMac']:
        driverpath = webDriversRootFolder + "mac/chromedriver"
    elif request.session['runningOnWindows']:
        driverpath = webDriversRootFolder + "windows/chromedriver"
    return driverpath


def executeCodeKeys(request, driver, hydraCode):
    textarea = driver.find_elements(By.CSS_SELECTOR, '.CodeMirror textarea')[0]
    #area = driver.find_elements(By.ID, 'editor-container')[0]
    area = driver.find_elements(By.CLASS_NAME, 'CodeMirror')[0]
    action = ActionChains(driver)
    area.click() #Click on browser screen
    textarea.send_keys(Keys.CONTROL + "a") #Ctrl+a to select all code
    textarea.send_keys(hydraCode) #writes new code overwriting old one
    action.key_down(Keys.CONTROL)
    action.key_down(Keys.SHIFT)
    action.key_down(Keys.ENTER)
    action.perform()
    action.key_up(Keys.ENTER)
    action.key_up(Keys.SHIFT)
    action.key_up(Keys.CONTROL)                   
    action.perform()

def hideCodeKeys(request): # presses Ctrl + Shift + H
    #It appears to be a bug in some computers when doing a key up of "h" key. This was the workaround:
    driver = get_object_by_id(request.session['webdriver'])
    action = ActionChains(driver)

    action.key_down(request.session['control_key'])
    action.key_down(Keys.SHIFT)
    action.perform()
    action.send_keys("h")
    action.key_up(Keys.SHIFT)
    action.key_up(request.session['control_key'])
    action.perform()
    return HttpResponse(status=204)

def get_object_by_id(id_):
    return ctypes.cast(id_, ctypes.py_object).value
    #for obj in gc.get_objects():
        #if id(obj) == id_:
            #return obj
    #raise Exception("No found")

def save_code_to_history(txtpath, info, hydra_code):
    hydra_code_no_header = hydra_code[len(info):] 
    extra_info = "// All generated codes are stored here. You can delete this file if you want.\n"
    separator = "----------------------------------------------------------------------------------------------"
    if not os.path.exists(txtpath): # writes header if not exists
        with open(txtpath, 'w') as txt: 
            txt.write(info)
            txt.write(extra_info)
            txt.write(separator + "\n\n")
    elif os.stat(txtpath).st_size == 0:  # writes header if content was emptied
        with open(txtpath, 'w') as txt:
            txt.write(info)
            txt.write(extra_info)
            txt.write(separator + "\n\n")
    with open(txtpath, 'a') as txt:
        txt.write("//" + time.strftime('%H:%M:%S%p - %d %b. %Y' + "\n\n"))
        txt.write(hydra_code_no_header)
        txt.write("\n\n" + separator + "\n\n")