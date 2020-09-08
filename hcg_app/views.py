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
    args = HCGArgumentHandler()
    default_fmin = 3
    default_fmax = 5
    hydra = CodeGenerator(ignoredList=[], exclusiveSourceList=[], exclusiveFunctionList=[])
    allSources = hydra.getSourcesList()
    allFunctions = hydra.getAllFunctions()

    if request.method == 'GET':
        if('webdriver' in request.session):
            #driver=ctypes.cast(request.session['webdriver'], ctypes.py_object).value
            #if isinstance(driver, selenium.webdriver.chrome.webdriver.WebDriver):
                #driver.quit()
            del request.session['webdriver']
            #for filename in glob.glob("hcg_app/__pycache__/*cpython*"):
             #   os.remove(filename) 
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
        print(data)
        print("-----------------")
        print("-----------------")
        print("-----------------")
        print("-----------------")
    
        if ('live_switch' in data): # START OR END LIVE SESSION MODE
            if not ('webdriver' in request.session): # STARTS LIVE SESSION MODE
                print("Opening Web driver...")
                url= "https://hydra.ojack.xyz/?code=" + hydra.encodeText(data['code'])
                driver = webdriver.Chrome(executable_path= "/home/ale/scripts/hydracodegenerator_terminal/resources/webdrivers/linux/chromedriver")
                driver.get(url)
                request.session['webdriver'] = id(driver)
                print("Web driver opened")
            else: # ENDS LIVE SESSION MODE
                #driver=ctypes.cast(request.session['webdriver'], ctypes.py_object).value
                #if isinstance(driver, selenium.webdriver.chrome.webdriver.WebDriver):
                    #driver.quit()
                del request.session['webdriver']
                #for filename in glob.glob("hcg_app/__pycache__/*cpython*"):
                #    os.remove(filename) 
                print("Web driver closed")
        else:
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
                args.set_amin(int(data['amin']))
                if not data['amax']:
                    args.set_amax(int(data['amin']))
                elif int(data['amin']) > int(data['amax']):
                    args.set_amin(int(data['amax']))

            if(data['amax']):
                if(args.get_amin() > int(data['amax'])):
                    args.set_amin(int(data['amax']))
                else:
                    args.set_amax(int(data['amax']))

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
            #encodedCode= hydra.encodeText(hydraCode)
            return_data['code'] = hydraCode

            if(data['live_session_mode']=="1"): #writes to an already open live session
                print("Writing new code to hydra...")
                driver = ctypes.cast(request.session['webdriver'], ctypes.py_object).value
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

        return_data = json.dumps(return_data)
        return HttpResponse(return_data, content_type="application/json") #return for AJAX requests only

    #Context for GET requests:
    hydraCode= hydra.generateCode(args.get_fmin(), args.get_fmax())   
    #encodedCode= hydra.encodeText(hydraCode)     
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
        'exclusiveSourcesList' : args.get_exclusive_source_list(),
        'exclusiveFunctionsList' : args.get_exclusive_function_list(),
        'allsources' : allSources,
        'allfunctions' : allFunctions,
        'sourcesandfunctions' : allSources + allFunctions
    }

    template = "hcg_app/content.html"
    print("HCG Page loaded")   
    return render(request, template, context) #return for GET requests only


def notFound(request):
    return HttpResponse("wat")

