from dotenv import load_dotenv
from pathlib import Path
from blockchain_vars import sender, recipient, token
import hashlib
import logging
import os
import pymysql
import pywaves as py
import sys

id_file = open('ID_to_read.txt', 'r+')
text = id_file.read().splitlines()
last_index = text[-1]

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(level=logging.DEBUG,
                    filename='pol-blockchain.log',
                    format='%(asctime)s %(levelname)s %(message)s')

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=str(env_path))

py.setNode('https://sg.katalystcoin.com')

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE')

connection = pymysql.connect(host=DB_HOST,
                             user=DB_USER,
                             password=DB_PASSWORD,
                             database=DB_DATABASE,
                             connect_timeout=3600)

cursor = connection.cursor()

try:
    with cursor:
        sql = "SELECT id FROM pol_record WHERE hash IS NULL AND id > %s;"
        # sql = "SELECT id FROM pol_record WHERE id > %s;" (for easy testing only)
        cursor.execute(sql, last_index)
        all_new_result = cursor.fetchall()
        length_all_result = len(all_new_result)

        if(length_all_result >= 1):
            idx_first_result = all_new_result[0][0]
            idx_last_result = all_new_result[-1][0]

            id_file.write( '{0}\n'.format(str(idx_last_result)) )
            id_file.close()

            logging.info( 'Detected new row: {0} - {1}'.format(str(idx_first_result), str(idx_last_result)) )

            for i in range( idx_first_result, idx_last_result+1 ):  # to change to one time sql query
                select_data_query = "SELECT data FROM pol_record WHERE id = %s;"
                cursor.execute(select_data_query, i)

                activity_string = str("{0}: {1}".format(i, cursor.fetchone()))
                activity_hashed = hashlib.sha256(activity_string.encode('utf-8')).hexdigest()

                update_hash_query = "UPDATE pol_record SET hash='{0}' WHERE id = {1}"\
                                     .format(str(activity_hashed), i)
                cursor.execute(update_hash_query)
                connection.commit()
                sender.sendAsset(recipient=recipient, asset=token, amount=1, attachment=activity_hashed)

                logging.info( 'New information is hashed and recorded in blockchain: {0}, hashed: {1}'.format(str(activity_string), str(activity_hashed)))

        else:
            sender.sendAsset(recipient=recipient, asset=token, amount=1, attachment='there is no activity')
            logging.info( 'No new activity detected')

except KeyboardInterrupt:
    logging.info('Keyboard interrupt. Exiting the program.')
    sys.exit()

except Exception as e:
    logging.error('Error occured in send_to_blockchain.py: {}'.format(str(e)) )

finally:
    connection.close()
