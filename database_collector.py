from database_access import database_login
import pandas as pd

#----------------------------------------------------------------------------------------------------------------#
# skiprate_filter
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
    print('-bod done-')
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
    print('-offers done-')
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
    print('-bids done-')
    return bids_data

#----------------------------------------------------------------------------------------------------------------#

def mel_data_collector(date_str):

    # SQL query with the WHERE clause for the specified time frame
    sql_bmra_mel = f"""
    select bmra_mellevel.ts, bmra_mellevel.ve, bmra_mel.bmu_id
    from bmra_mellevel
    left join bmra_mel
        on bmra_mellevel.mel_id = bmra_mel.id
    where bmra_mellevel.ts = '{date_str}'
    order by bmra_mellevel.ts;
    """

    # Execute SQL query and read the data into a DataFrame
    mel_data = pd.read_sql(sql_bmra_mel, database_login())
    print('-mel done-')
    return mel_data

#----------------------------------------------------------------------------------------------------------------#

def mil_data_collector(date_str):

    # SQL query with the WHERE clause for the specified time frame
    sql_bmra_mil = f"""
    select bmra_millevel.ts, bmra_millevel.vf, bmra_mil.bmu_id
    from bmra_millevel
    left join bmra_mil
        on bmra_millevel.mil_id = bmra_mil.id
    where bmra_millevel.ts = '{date_str}'
    order by bmra_millevel.ts;
    """

    # Execute SQL query and read the data into a DataFrame
    mil_data = pd.read_sql(sql_bmra_mil, database_login())
    print('-mil done-')
    return mil_data

#----------------------------------------------------------------------------------------------------------------#

def fpn_data_collector(date_str):

    # SQL query with the WHERE clause for the specified time frame
    sql_bmra_fpn = f"""
    select bmra_fpnlevel.ts, bmra_fpnlevel.vp, bmra_fpn.bmu_id
    from bmra_fpnlevel
    left join bmra_fpn
        on bmra_fpn.id = bmra_fpnlevel.fpn_id
    where bmra_fpnlevel.ts = '{date_str}'
    order by bmra_fpnlevel.ts;
    """

    # Execute SQL query and read the data into a DataFrame
    fpn_data = pd.read_sql(sql_bmra_fpn, database_login())
    print('-fpn done-')
    return fpn_data

#----------------------------------------------------------------------------------------------------------------#
# BM_analyser 
#----------------------------------------------------------------------------------------------------------------#

def boav_data_collector(start_date, end_date):

    # SQL query with the WHERE clause for the specified time frame
    sql_bmra_boav = f"""
    select*
    from bmra_boav
    where bmra_boav.ts >= '{start_date}'
        and bmra_boav.ts <= '{end_date}';
    """

    # Execute SQL query and read the data into a DataFrame
    boav_data = pd.read_sql(sql_bmra_boav, database_login())
    print('-boav done-')
    return boav_data

def boalf2_data_collector(start_date, end_date):

    # SQL query with the WHERE clause for the specified time frame
    sql_bmra_boalf = f"""
    select*
    from bmra_boalflevel
    where bmra_boalflevel.ts >= '{start_date}'
        and bmra_boalflevel.ts <= '{end_date}';
    """
    # Execute SQL query and read the data into a DataFrame
    boalf2_data = pd.read_sql(sql_bmra_boalf, database_login())
    print('-boalf2 done-')
    return boalf2_data