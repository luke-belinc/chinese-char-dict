from configparser import ConfigParser


def config(filename="/media/luke/Things/OneDrive\ -\ Wayne\ State\ University/python-project/database.ini", section="psql"):
    # create a parser
    parser = ConfigParser()
    #read config file
    parser.read(filename)

    # get section, default to psql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for p in params:
            db[p[0]] = p[1]

    else:
        raise Exception("Section {0} not found in the {1} file.".format(section, filename))

    return db
