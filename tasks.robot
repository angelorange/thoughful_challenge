*** Settings ***
Library     OperatingSystem
Library     Process


*** Variables ***
${OUTPUT_DIR}       output


*** Tasks ***
Search and Save News
    Run Process    python    news_search.py
    Copy Files    ${OUTPUT_DIR}    ${OUTPUT_DIR}
