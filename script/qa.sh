ALLURE_REPORT_FOLDER=./allure-report

poetry run pytest \
  --cov-report html --cov=test_cl \
  --alluredir=${ALLURE_REPORT_FOLDER} \
  tests/
firefox htmlcov/index.html
# allure serve ${ALLURE_REPORT_FOLDER}
