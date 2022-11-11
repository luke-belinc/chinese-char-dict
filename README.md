# chinese-char-dict

A simple python app to look up chinese characters and view their stroke orders!

Not possible without [Make Me A Hanzi](https://www.skishore.me/makemeahanzi/) project


![Exmaple](example.gif)

### before running: 

1. install [PostgreSQL](https://www.postgresql.org/download/)
2. create a database named 'dictionary'
3. update the database username and password at `tool\initalize.py:95` and `tool\dbtool.py:14` to match your system settings
4. install [Python 3](https://www.python.org/downloads/)
5. run `pip install psycopg2 pyside2` inside your fav shell

### to start:

1. run `python3 main.py` inside your fav shell
