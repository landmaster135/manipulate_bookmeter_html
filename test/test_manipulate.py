# coding: UTF-8

# Library by third party
import pytest
from bs4 import BeautifulSoup
# Library by manipulate_bookmeter_html
from src.manipulate_bookmeter_html.manipulate import *

FOLDER_TEST_DATA = get_config("general_path", "folder_test_data")

def test_manipulate_bookmeter_html_1_1():
    html_1 = "1_1_before.html"
    html_2 = "1_1_after.html"
    bookmeter_html = open(f"{FOLDER_TEST_DATA}/{html_1}", 'r')
    actual = manipulate_bookmeter_html(bookmeter_html)
    expected_html = open(f"{FOLDER_TEST_DATA}/{html_2}", 'r')
    expected = BeautifulSoup(expected_html, "html.parser")
    assert str(actual) == str(expected)
