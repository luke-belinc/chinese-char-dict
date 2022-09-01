from connect import connect
from getEntries import getEntries

conn = connect()

if ((__name__ == '__main__') and (conn != None)):
    # success message
    print("connection succesful! (-: ")

    # initialize cursor object
    cursor = conn.cursor()

    # print version
    print("psql version: ", end='')
    cursor.execute("SELECT version()")
    print(cursor.fetchone())

    # create 'entries' table in 'dictionary'
    cursor.execute("""CREATE TABLE entries (
                    unicode		INTEGER		PRIMARY KEY,
                    charText	CHAR (1)	UNIQUE NOT NULL,
                    pinyin		TEXT [],
                    definition	TEXT,
                    etymology	JSON,
                    radical		CHAR (2)
                    )""")

    # get json objects from 'dictionaries.txt'
    entries = getEntries()

    # parse
    for e in entries:
        # primary key (unicode) and character
        char = e["character"]
        unicode = ord(char)

        # workaround, some keys are not present in all of the
        # dictionary.txt data
        defin = etym = rad = pinyin = None
        if ("pinyin" in e):
            pinyin = e["pinyin"]
        if ("definition" in e):
            defin = e["definition"]
        if ("etymology" in e):
            etym = json.dumps(e["etymology"])
        if ("radical" in e):
            rad = e["radical"]

        # insert data into 'entries' table
        sql = """INSERT INTO entries (unicode,chartext,pinyin,
            definition,etymology,radical) VALUES (%s,%s,%s,%s,%s,%s)"""

        values = (unicode, char, pinyin, defin, etym, rad)

        cursor.execute(sql, values)

    # commit changes to the table
    conn.commit()

    # close connections
    print("closing connections...")
    cursor.close()
    conn.close()

    # yay success!!!
    print("all done, bye bye!")
