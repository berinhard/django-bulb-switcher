#coding:utf-8

def is_on(request, flag):
    return flag in request.VALID_BULB_SWITCHER_CONDITIONALS

def is_off(request, flag):
    return not is_on(request, flag)
