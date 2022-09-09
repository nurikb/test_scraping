## test parser

this script allows you to parse data 

## Getting started

Start docker services:
    ```
    docker-compose up -d
    ```

Create dump file:
   ```bash
    docker exec db pg_dump --column-inserts --data-only  -U postgres  postgres > dumps/FILE_NAME.sql
  ```
