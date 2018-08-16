from dotenv import load_dotenv
from pathlib import Path
import logging
import os
import sys
import pymysql

id_file = open('iki_login_ID.txt', 'r+')
text = id_file.read().splitlines()
last_index = text[-1]

logging.basicConfig(level=logging.DEBUG,
                    filename='iki-login.log',
                    format='%(asctime)s %(levelname)s %(message)s')

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=str(env_path))

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('IKI_DATABASE')

POL_HOST = os.getenv('POL_HOST')
POL_USER = os.getenv('POL_USER')
POL_PASSWORD = os.getenv('POL_PASSWORD')
POL_DATABASE = os.getenv('POL_DATABASE')

pol_conn = pymysql.connect(host=POL_HOST,
                            user=POL_USER,
                            password=POL_PASSWORD,
                            database=POL_DATABASE)

mysql_conn = pymysql.connect(host=DB_HOST,
                             user=DB_USER,
                             password=DB_PASSWORD,
                             database=DB_DATABASE)

pol_cur = pol_conn.cursor()
mysql_cur = mysql_conn.cursor()


try:
    with pol_cur , mysql_cur:
        sql = """
                SELECT uc.id, uc.WalletAddress, g.Name as userChoice
                FROM UnfilteredUseCase uc
                	LEFT JOIN CoinList g ON g.Symbol = uc.Choice
                WHERE uc.Id > %s;
                """

        mysql_cur.execute(sql, last_index)
        all_new_result = mysql_cur.fetchall()
        length_all_result = len(all_new_result)
        print(all_new_result)

        if(length_all_result >= 1):

            first_new_result = all_new_result[0]
            last_new_result =  all_new_result[-1]

            idx_first_result = first_new_result[0]
            idx_last_result = last_new_result[0]

            for row in all_new_result:
                user = str('Anonymous') if row[1] is None else str(row[1])

                insert_into_pol_query = "INSERT INTO pol_record (app_name, data) VALUES('hotx', %s)"
                val =  'likes, {0}, {1} likes {2}' \
                        .format( str(row[0]), str(user), str(row[2]) )
            #     pol_cur.execute( insert_into_pol_query, val )
            #     pol_conn.commit()
            #
            # id_file.write( '{0}\n'.format(str(idx_last_result)) )
            # id_file.close()

            logging.info( 'Detected new row: {0} - {1}'.format(str(idx_first_result), str(idx_last_result)) )

        else:
            logging.info( 'No new entry detected')

except KeyboardInterrupt:
    logging.info('Keyboard interrupt. Exiting the program.')
    sys.exit()

except Exception as e:
    logging.error('Error occured in send_to_blockchain.py: ', e )

finally:
    pol_conn.close()
    mysql_conn.close()
