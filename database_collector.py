from database_access import database_login
import pandas as pd

#----------------------------------------------------------------------------------------------------------------#

def boalf_data_collector(date_str):

    # SQL query with the WHERE clause for the specified time frame
    sql_bmra_boalf = f"""
    select bmra_boalf.id, bmra_boalflevel.ts, bmra_boalflevel.va, bmra_boalf.ts, bmra_boalf.ta, bmra_boalf.bmu_id, bmra_bmu.name, bmra_bmu.type_id from bmra_boalflevel
    left join bmra_boalf
        on bmra_boalf.id = bmra_boalflevel.boalf_id
    left join bmra_bmu
        on bmra_boalf.bmu_id = bmra_bmu.id
    where bmra_boalflevel.ts = '{date_str}'
    order by bmra_boalflevel.ts;
    """

    # Execute SQL query and read the data into a DataFrame
    boalf_data = pd.read_sql(sql_bmra_boalf, database_login())
    # Display the filtered DataFrame
    print('-boalf done-')
    return boalf_data

#----------------------------------------------------------------------------------------------------------------#

def bod_data_collector(date_str):

    # Your SQL query with the WHERE clause for the specified date
    sql_bmra_bod = f"""
    select bmra_bod.ts1, bmra_bod.ts2, bmra_bod.nn, bmra_bod.op, bmra_bod.bp, bmra_bod.vb1, bmra_bod.vb2, bmra_bmu.id, bmra_bmu.name, bmra_bmu.type_id  
    from bmra_bod
    left join bmra_bmu
        on bmra_bod.bmu_id = bmra_bmu.id
    where bmra_bod.ts1 = '{date_str}';
    """

    # Execute your SQL query and read the data into a DataFrame
    bod_data = pd.read_sql(sql_bmra_bod, database_login())
    # Display DataFrame
    print('-bod check-')
    return bod_data

#----------------------------------------------------------------------------------------------------------------#

def offers_data_collector(date_str):

    # SQL query with the WHERE clause for the specified time frame
    sql_bmra_offers = f"""
    select bmra_bod.nn, bmra_bod.op, bmra_bod.bp, bmra_bod.vb1, bmra_bod.vb2, bmra_bmu.id, bmra_bmu.name, bmra_bmu.type_id  
    from bmra_bod
    left join bmra_bmu
        on bmra_bod.bmu_id = bmra_bmu.id
    where bmra_bod.ts1 = '{date_str}'
        and bmra_bod.nn > 0
        and not (bmra_bod.op = 0 AND bmra_bod.bp = 0 AND bmra_bod.vb1 = 0 AND bmra_bod.vb2 = 0)
    order by bmra_bod.op;
    """

    # Execute SQL query and read the data into a DataFrame
    offers_data = pd.read_sql(sql_bmra_offers, database_login())
    # Display the filtered DataFrame
    print('-offers check-')
    return offers_data

#----------------------------------------------------------------------------------------------------------------#

def bids_data_collector(date_str):

    # SQL query with the WHERE clause for the specified time frame
    sql_bmra_bids = f"""
    select bmra_bod.nn, bmra_bod.op, bmra_bod.bp, bmra_bod.vb1, bmra_bod.vb2, bmra_bmu.id, bmra_bmu.name, bmra_bmu.type_id  
    from bmra_bod
    left join bmra_bmu
        on bmra_bod.bmu_id = bmra_bmu.id
    where bmra_bod.ts1 = '{date_str}'
        and bmra_bod.nn < 0
        and not (bmra_bod.op = 0 AND bmra_bod.bp = 0 AND bmra_bod.vb1 = 0 AND bmra_bod.vb2 = 0)
    order by bmra_bod.bp desc;
    """

    # Execute SQL query and read the data into a DataFrame
    bids_data = pd.read_sql(sql_bmra_bids, database_login())
    # Display the filtered DataFrame
    print('-bids check-')
    return bids_data

#----------------------------------------------------------------------------------------------------------------#

def mel_data_collector(date_str):

    # SQL query with the WHERE clause for the specified time frame
    sql_bmra_mel = f"""
    select bmra_mellevel.ts, bmra_mellevel.ve, bmra_mel.bmu_id
    from bmra_mellevel
    left join bmra_mel
        on bmra_mellevel.mel_id = bmra_mel.id
    where bmra_mellevel.ts = '{date_str}';
    """

    # Execute SQL query and read the data into a DataFrame
    mel_data = pd.read_sql(sql_bmra_mel, database_login())
    # Display the filtered DataFrame
    print('-mel done-')
    return mel_data