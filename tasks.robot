*** Settings ***
Library     OperatingSystem
Library     Process


*** Tasks ***
Search and Save News
    Run Process    python    news_search.py
