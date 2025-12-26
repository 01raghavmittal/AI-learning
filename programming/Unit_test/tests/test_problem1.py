import pytest
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from problem1 import word_count, unique_words

def test_wordcount():
    assert word_count(text="I am learning about unit test in python")==8

def test_wordcount():
    assert word_count(text="I am learning about unit test in python. I am a python programmer")==13