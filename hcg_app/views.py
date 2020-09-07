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

def index(request):
    args= HCGArgumentHandler()
    default_fmin= 3
    default_fmax= 5
    hydra=CodeGenerator(ignoredList=[], exclusiveSourceList=[], exclusiveFunctionList=[])
    if request.method == 'GET':
        if('webdriver' in request.session):
            #driver=ctypes.cast(request.session['webdriver'], ctypes.py_object).value
            #if isinstance(driver, selenium.webdriver.chrome.webdriver.WebDriver):
               # driver.quit()
            del request.session['webdriver']
            for filename in glob.glob("hcg_app/__pycache__/*cpython*"):
                os.remove(filename) 
        args.set_fmin( default_fmin )
        args.set_fmax( default_fmax )
        args.set_amin( hydra.getMinValue() )
        args.set_amax( hydra.getMaxValue() )
        args.set_arrow_prob( hydra.getArrowFunctionProb() )
        args.set_mouse_prob( hydra.getMouseFunctionProb() )
        args.set_modulate_itself_prob( hydra.getModulateItselfProb() )
        args.set_ignore_list( hydra.getIgnoredList() )
        args.set_exclusive_source_list( hydra.getExclusiveSourceList() )
        args.set_exclusive_function_list( hydra.getExclusiveFunctionListt() )

    elif(request.method == 'POST'): # AJAX REQUESTS FROM HERE
        data=request.POST
        return_data= { }
        #print(data)
        #args.set_arrow_prob(request.POST.get('arrow_prob'))
        #args.set_mouse_prob(request.POST.get('mouse_prob'))
        #args.set_modulate_itself_prob(request.POST.get('modulate_itself_prob'))
        #args.set_ignore_list(request.POST.get('ignore_list')) #.split(",")
        #args.set_exclusive_source_list(request.POST.get('exclusive_source_list'))
        #args.set_exclusive_function_list(request.POST.get('exclusive_function_list'))


        if ('live_switch' in data): # START OR END LIVE SESSION MODE
            print("-------------")
            print("live switch")
            print("-------------")
            if not ('webdriver' in request.session): # STARTS LIVE SESSION MODE
                url= "https://hydra.ojack.xyz/?code=" + hydra.encodeText(data['code'])
                driver = webdriver.Chrome(executable_path= "/home/ale/scripts/hydracodegenerator_terminal/resources/webdrivers/linux/chromedriver")
                driver.get(url)
                request.session['webdriver'] = id(driver)
                print(request.session['webdriver'])
            else: # ENDS LIVE SESSION MODE
               # driver=ctypes.cast(request.session['webdriver'], ctypes.py_object).value
               # if isinstance(driver, selenium.webdriver.chrome.webdriver.WebDriver):
               #     driver.quit()
                del request.session['webdriver']
                for filename in glob.glob("hcg_app/__pycache__/*cpython*"):
                    os.remove(filename) 
        else:
            #Code generation for AJAX requests
            args.set_fmin(int(data['fmin']))
            args.set_fmax(int(data['fmax']))
            args.set_amin(int(data['amin']))
            args.set_amax(int(data['amax']))
            hydra = CodeGenerator(args.get_amin(), args.get_amax(), args.get_arrow_prob(), args.get_mouse_prob(), args.get_modulate_itself_prob(), args.get_ignore_list(), args.get_exclusive_source_list(), args.get_exclusive_function_list())
            hydraCode= hydra.generateCode(args.get_fmin(), args.get_fmax())   
            #encodedCode= hydra.encodeText(hydraCode)
            return_data['code'] = hydraCode

            if(data['live_session_mode']=="1"): #writes to an already open live session
                driver = ctypes.cast(request.session['webdriver'], ctypes.py_object).value
                textarea = driver.find_elements(By.CSS_SELECTOR, '.CodeMirror textarea')[0]
                #area = driver.find_elements(By.ID, 'editor-container')[0]
                area = driver.find_elements(By.CLASS_NAME, 'CodeMirror')[0]
                action = ActionChains(driver)
                area.click() #Click on browser screen
                textarea.send_keys(Keys.CONTROL + "a") #Ctrl+a to select all code
                textarea.send_keys(data['code']) #writes new code overwriting old one
                action.key_down(Keys.CONTROL)
                action.key_down(Keys.SHIFT)
                action.key_down(Keys.ENTER)
                action.perform()
                action.key_up(Keys.ENTER)
                action.key_up(Keys.SHIFT)
                action.key_up(Keys.CONTROL)                   
                action.perform()

     
        return_data = json.dumps(return_data)
        return HttpResponse(return_data, content_type="application/json") #return for AJAX requests only

    #Context for GET requests:
    hydraCode= hydra.generateCode(args.get_fmin(), args.get_fmax())   
    #encodedCode= hydra.encodeText(hydraCode)        
    context = {
        'code': hydraCode,
    }
    template = "hcg_app/content.html"

    return render(request, template, context) #return for GET requests only


def asd(request):
    args= HCGArgumentHandler()
    args.set_fmin(int(request.POST.get('fmin')))
    args.set_fmax(int(request.POST.get('fmax')))
    args.set_amin(int(request.POST.get('amin')))
    args.set_amax(int(request.POST.get('amax')))
    #args.set_arrow_prob(request.POST.get('arrow_prob'))
    #args.set_mouse_prob(request.POST.get('mouse_prob'))
    #args.set_modulate_itself_prob(request.POST.get('modulate_itself_prob'))
    #args.set_ignore_list(request.POST.get('ignore_list')) #.split(",")
    #args.set_exclusive_source_list(request.POST.get('exclusive_source_list'))
    #args.set_exclusive_function_list(request.POST.get('exclusive_function_list'))
    hydra = CodeGenerator(args.get_amin(), args.get_amax(), args.get_arrow_prob(), args.get_mouse_prob(), args.get_modulate_itself_prob(), args.get_ignore_list(), args.get_exclusive_source_list(), args.get_exclusive_function_list())
    request.session['code'] = hydra.generateCode(args.get_fmin(), args.get_fmax())   
    index(request)
    return HttpResponse(json.dumps(request.session['code']))


def notFound(request):
    return HttpResponse("wat")

