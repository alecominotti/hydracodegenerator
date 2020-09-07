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
    elif(request.method == 'POST') and ('osb' in request.POST):
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

    hydraCode= hydra.generateCode(args.get_fmin(), args.get_fmax())   
    encodedCode= hydra.encodeText(hydraCode)

    if (request.method == 'POST') and ('csb' in request.POST): #close webdriver
      #  driver=ctypes.cast(request.session['webdriver'], ctypes.py_object).value
       # driver.quit()
        if('webdriver' in request.session):
            del request.session['webdriver']
            for filename in glob.glob("hcg_app/__pycache__/*cpython*"):
                os.remove(filename) 
    if (request.method == 'POST') and ('osb' in request.POST): #open webdriver
        if not ('webdriver' in request.session):
            url= "https://hydra.ojack.xyz/?code=" + encodedCode
            driver = webdriver.Chrome(executable_path= "/home/ale/scripts/hydracodegenerator_terminal/resources/webdrivers/linux/chromedriver")
            driver.get(url)
            request.session['webdriver'] = id(driver)
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
        
    context = {
        'code': hydraCode,
    } 
    
    template = "hcg_app/content.html"
    return render(request, template, context)


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

