# Personal code to access database:
from sqlalchemy import create_engine

def database_login():   # Personal code for database access.
    db_user = 'ElexonDataReadOnly'
    db_host = 'eee-aesg-gh.ds.strath.ac.uk'
    db_password = 'tr3BN9bKoA8kPe'
    db_name = 'ElexonData'
    db_url = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
    engine = create_engine(db_url)
    return engine


# Provided code to access:
# import psycopg2
# conn = psycopg2.connect("dbname='ElexonData' user={} host={} password={}".format('ElexonDataReadOnly',
#                                                                                  'eee-aesg-gh.ds.strath.ac.uk',
#                                                                                  'tr3BN9bKoA8kPe'))
# cur = conn.cursor()