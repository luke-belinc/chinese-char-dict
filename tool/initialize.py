import os, json, datetime
import psycopg2

# constant for current directory path
THIS_FOLDER = os.path.split(os.path.abspath(__file__))[0]
# log and logpath
logpath = os.path.join(THIS_FOLDER, "logs", "initialize.log")
log = open(logpath, "a+")

TOTALERRORS = 0
TOTALENTRIES = 0

def init_characters_table(curs):
    write_log("Checking if \"characters\" table exists")
    curs.execute("""SELECT EXISTS (
                        SELECT 1
                        FROM   pg_tables
                        WHERE  tablename='characters'
                    );""")

    if (curs.fetchone()[0] is False):
        write_log("no table found, initializing characters table")
        curs.execute("""CREATE TABLE characters (
                                unicode		INTEGER     PRIMARY KEY,
                                chartext	CHAR (1)	UNIQUE NOT NULL,
                                pinyin		TEXT [],
                                definition	TEXT,
                                etymology	JSON,
                                radical		CHAR (2),
                                strokedata  JSON
                            ) """)

def insert_chracters(curs):
    global TOTALENTRIES
    global TOTALERRORS
    write_log("loading characters.json from data folder and opening all.json for parsing")

    # get json objects from characters.json
    characters_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'characters.json')
    characters_file = open(characters_path, 'r', encoding='utf8')
    entries = json.loads(characters_file.read())

    strokedata_path = os.path.join(THIS_FOLDER, 'data', 'stroke-data', 'all.json')
    strokedata_file = open(strokedata_path, 'r', encoding='utf8')
    strokedata = json.loads(strokedata_file.read())

    write_log("parsing characters.json file per entry and inserting data into table...")
    for e in entries:
        # primary key (unicode) and character (chartext)
        char    = e["character"]
        unicode = ord(char)

        curs.execute("SELECT unicode FROM characters c WHERE c.unicode=" + str(unicode))

        if (curs.fetchone() is not None):
            write_log("character already in database, skipping...")
            continue

        # some keys are not present in all of the
        # dictionary.txt data, this chunk avoids errors
        # caused from missing keys
        pinyin = e["pinyin"]                  if ("pinyin" in e)      else None
        defin  = e["definition"]              if ("definition" in e)  else None
        etym   = json.dumps(e["etymology"])   if ("etymology" in e)   else None
        rad    = e["radical"]                 if ("radical" in e)     else None
        sd     = json.dumps(strokedata[char]) if (char in strokedata) else None

        try:
            # insert data into 'entries' table
            sql    = """INSERT INTO
                     characters (unicode,chartext,pinyin,definition,etymology,radical,strokedata)
                     VALUES     (%s,     %s,      %s,    %s,        %s,       %s,     %s)"""
            values =            (unicode,char,    pinyin,defin,     etym,     rad,    sd)

            curs.execute(sql, values)
            TOTALENTRIES += 1

        except Exception as err:
            TOTALERRORS += 1
            write_log("Exception raised when inserting " + char + " into the table: " + str(err))

        finally:
            strokedata_file.close()

def write_log(msg):
    time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = '[' + time_str + '] -> ' + str(msg) + '\n'
    log.write(line)

def begin():
    write_log('attemption connection to the PSQL database...')
    curs = conn = None

    try:
        conn = psycopg2.connect(
            host='localhost', 
            database='dictionary', 
            user='postgres', 
            password='password'
        )

        # success message
        write_log("Connection succesful! (-: \n")
        write_log("Getting version...\n\n")
        curs = conn.cursor()
        curs.execute("SELECT version()")
        write_log("PSQL Version: " + str(curs.fetchone()))
        write_log("Closing cursor and returning connection...")

    except (Exception, psycopg2.DatabaseError) as e:
        write_log("Exception raised while attempting connecting to database: " + str(e))
        if conn is not None:
            write_log("Closing connection...")
            conn.close()
        if curs is not None:
            write_log("Closing cursor...")
            curs.close()
        write_log("returning -1")
        return -1

    init_characters_table(curs)
    insert_chracters(curs)

    write_log("Total number of entries parsed: " + str(TOTALENTRIES))
    write_log("Total number of errors: " + str(TOTALERRORS))
    write_log("Committing changes to database...")
    conn.commit()
    write_log("Closing cursor...")
    curs.close()
    write_log("Closting connection...")
    conn.close()
    write_log("returning psycopg2.connect function...")
    log.close()

    return psycopg2.connect
