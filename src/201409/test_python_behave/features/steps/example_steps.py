#coding=utf-8
# -- FILE: features/steps/example_steps.py
from behave import given, when, then, step
from test01 import TextEditor
# @given('Given we have some text {text1}')
@given('we have some text {text}')#"aaa bbb ccc         "')
def step_impl(context,text):
    context.editor=TextEditor(text)
    assert True  

@given('we have a file "{filename}"')#"aaa bbb ccc         "')
def step_impl(context,filename):
    file = open(filename, "r")
    text = file.read()
    context.editor=TextEditor(text)
    assert True  

@given('we have some long text')
def step_impl(context):
    context.editor=TextEditor(context.text)
    assert True  

@when('we implement prev word func with pointer at {pos:d}')
def step_impl(context, pos):  # -- NOTE: number is converted into integer
    print('000000000000')
    assert pos == 12
    assert pos > 0
    context.ret=context.editor.prev_word(pos)
    print(context.ret)
   
@then('behave will return {text}')              
def step_impl(context,text):
    assert context.ret == 'ccc'
# #@given('we have some text "aaa bbb ccc         "')
# @given('we have some text {a}')#"aaa bbb ccc         "')
# def step_impl(context,a):
#     assert True
# @when('we implement prev word func with pointer at 12')
# def step_impl(context):
#     assert True
# 
# @then('behave will return \'ccc\'')
# def step_impl(context):
#     assert True