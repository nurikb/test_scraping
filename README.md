## test parser

this script allows you to parse data 

## Getting started

Start docker services:
    ```bash
    docker-compose up -d
    ```

Create dump file:
   ```bash
    docker exec db pg_dump --column-inserts --data-only  -U postgres  postgres > FILE_NAME.sql
  ```
