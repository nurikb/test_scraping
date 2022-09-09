## test parser

this script allows you to parse data 

## Getting started

Start docker services:
   ```bash
    docker-compose up --exit-code-from main
  ```

Create dump file:
   ```bash
    docker exec db pg_dump --column-inserts --data-only  -U postgres  postgres > dumps/FILE_NAME.sql
  ```

## Note:
ignore the message:

   ```bash
       Error occurred during loading data. Trying to use cache server https://fake-useragent.herokuapp.com/browsers/0.1.11
        Traceback (most recent call last):
        File "/opt/venv/lib/python3.8/site-packages/fake_useragent/utils.py", line 154, in load
        for item in get_browsers(verify_ssl=verify_ssl):
        File "/opt/venv/lib/python3.8/site-packages/fake_useragent/utils.py", line 99, in get_browsers
        html = html.split('<table class="w3-table-all notranslate">')[1]
        IndexError: list index out of range
  ```