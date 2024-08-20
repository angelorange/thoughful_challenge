*** Settings ***
Library     OperatingSystem
Library     Process


*** Variables ***
${OUTPUT_DIR}       /home/worker/instance/runs/2975ce28-976b-497b-8a3d-f8ac98b4b5a2/package/output
${ARTIFACTS_DIR}    ${OUTPUT_DIR}


*** Tasks ***
Search and Save News
    Run Process    python    news_search.py
    Copy Files    ${OUTPUT_DIR}/news_data.xlsx    ${ARTIFACTS_DIR}
    Copy Files    ${OUTPUT_DIR}/images    ${ARTIFACTS_DIR}/images

Log    Files in ${OUTPUT_DIR}: ${/}${"\n".join(os.listdir(${OUTPUT_DIR}))}
