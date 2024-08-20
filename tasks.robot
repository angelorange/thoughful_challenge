*** Settings ***
Library     OperatingSystem
Library     Process


*** Variables ***
${OUTPUT_DIR}       output
${ARTIFACTS_DIR}    /path/to/artifacts


*** Tasks ***
Search and Save News
    Run Process    python    news_search.py
    # Ensure that the output directory is copied to the artifacts directory
    Copy Directory    ${OUTPUT_DIR}    ${ARTIFACTS_DIR}
