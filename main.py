import oracledb
import mysql.connector
import os

ORACLE_USER = os.getenv("ORACLE_USER") 
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD") 
ORACLE_SCHEMA=  os.getenv("ORACLE_SCHEMA")
ORACLE_URL = os.getenv("ORACLE_URL")


MYSQL_USER = os.getenv("MYSQL_USER") 
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABSE=  os.getenv("MYSQL_DATABSE")
MYSQL_HOST = os.getenv("MYSQL_HOST") 

TABID = os.getenv("TABID")

def get_data_from_oracle(connection):
    print("--- GETTING DATA FROM ORACLE ---")
    with connection.cursor() as cursor:
        sql = f"""SELECT r.CARD_ID, rk.KEY_CODE FROM {ORACLE_SCHEMA}.REGISTRATION_KEYS
            rk LEFT JOIN {ORACLE_SCHEMA}.R_KEYS r ON rk.REG_ID = r.REG_ID"""
        return cursor.execute(sql).fetchall()


def delete_data_from_sql(connection):
    print("--- DELLITING DATA FROM MYSQL ---")
    sql = f"DELETE from {MYSQL_DATABSE}.personal where description = 'API_GUEST'"
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()


def transform_key(value):
    print(f"--- TRANSFORMING {value} KEY ---")
    return '380' + f'{int(value):x}'.upper()


def put_key_to_sql(OracleConnection_, MySqlConnection_):
    cards_n_keys = get_data_from_oracle(OracleConnection_)
    delete_data_from_sql(MySqlConnection_)
    cursor = MySqlConnection_.cursor()
    for i in cards_n_keys:
        something_cool = transform_key(i[1])

        print("--- INSERTING DATA TO MYSQL ---")
        cursor.execute(f'insert into {MYSQL_DATABSE}.personal(PARENT_ID,TYPE,EMP_TYPE,NAME,'
                        f'DESCRIPTION,STATUS,CODEKEY,CODEKEYTIME,CODEKEY_DISP_FORMAT,'
                        f"CREATEDTIME,BADGE,USER_APPLS_EDIT_CURRENT) "
                        f"values((select p.id from {MYSQL_DATABSE}.personal p where p.TABID = '{TABID}')"
                        f',"EMP","GUEST","{i[0]}","API_GUEST","AVAILABLE",'
                        f"x'{something_cool}'"
                        f',now(),"W58DEC",now(),"2","1")')
        MySqlConnection_.commit()
    

try:
    MySqlConnection = mysql.connector.connect(host=MYSQL_HOST,
                                user=MYSQL_USER, password=MYSQL_PASSWORD)
    OracleConnection = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=ORACLE_URL,
                          mode=oracledb.AUTH_MODE_SYSDBA)

    put_key_to_sql(OracleConnection, MySqlConnection)
    MySqlConnection.close()
    OracleConnection.close()

except Exception as Error:
    print(Error)
        


