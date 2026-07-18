# This file is part of the materials accompanying the book
# "Mathematical Logic through Python" by Gonczarowski and Nisan,
# Cambridge University Press. Book site: www.LogicThruPython.org
# (c) Yannai A. Gonczarowski and Noam Nisan, 2017-2022
# File name: test_chapter01.py

"""Tests all Chapter 1 tasks."""

from propositions.syntax_test import *

def test_task1(debug=False):
    test_repr(debug)

def test_task2(debug=False):
    test_variables(debug)

def test_task3(debug=False):
    test_operators(debug)

def test_task4(debug=False):
    test_parse_prefix(debug)

def test_task5(debug=False):
    test_is_formula(debug)

def test_task6(debug=False):
    test_parse(debug)

def test_task7(debug=False):
    test_polish(debug)

def test_task8(debug=False):
    test_parse_polish(debug)

test_task1(True)
print('Task 1.1 complete! 🎉')
test_task2(True)
print('Task 1.2 complete! 🎉')
test_task3(True)
print('Task 1.3 complete! 🎉')
test_task4(True)
print('Task 1.4 complete! 🎉')
test_task5(True)
print('Task 1.5 complete! 🎉')
test_task6(True)
print('Task 1.6 complete! 🎉')
test_task7(True) # Optional
print('Task 1.7 complete! 🎉')
test_task8(True) # Optional
print('Task 1.8 complete! 🎉')
