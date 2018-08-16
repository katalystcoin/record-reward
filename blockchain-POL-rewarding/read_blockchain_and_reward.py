from blockchain_vars import sender
from dotenv import load_dotenv
from pathlib import Path
from sort import sorted_nicely
import base58
import json
import logging
import os
import pymysql
import pywaves as py
import sys

with open('reward_system.json') as json_data:
    reward_data = json.load(json_data)

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(level=logging.DEBUG,
                    filename='blockchain-reward.log',
                    format='%(asctime)s %(levelname)s %(message)s')

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=str(env_path))

py.setNode('https://sg.katalystcoin.com')

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE')

connection = pymysql.connect(  host=DB_HOST,
                               user=DB_USER,
                               password=DB_PASSWORD,
                               database=DB_DATABASE,
                               connect_timeout=3600)

cursor = connection.cursor()

current_height = py.height()-1
current_block = py.block(current_height)
transactions_in_block = current_block['transactions']
hashes_to_process = []

print('reading current height: ', current_height)

for i in range(len(transactions_in_block)):
    get_transactions_attachment = str(transactions_in_block[i]['attachment'])
    decoded_attachment = base58.b58decode(get_transactions_attachment)
    hashes_to_process.append( str(decoded_attachment.decode('utf-8')) )

hash_tuple = tuple(hashes_to_process)
print('hashes to process', hash_tuple)
logging.info( 'Read height: {}'.format( str(current_height) ))

try:
    with cursor:
        if(len(hash_tuple) == 1):
             update_semaphore_query = "UPDATE pol_record SET semaphore='L', blockheight={0} WHERE hash = {1} AND semaphore = '0';".format(current_height, str(hash_tuple[0]))
             cursor.execute(update_semaphore_query)
             connection.commit()

        elif(len(hash_tuple) > 1):
            update_semaphore_query = "UPDATE pol_record SET semaphore='L', blockheight={0} WHERE hash IN {1} AND semaphore = '0';".format(current_height, hash_tuple)
            cursor.execute(update_semaphore_query)
            connection.commit()

        select_locked_query = "SELECT id, app_name, data, blockheight FROM pol_record WHERE semaphore ='L';"
        cursor.execute(select_locked_query)
        all_locked_queries = cursor.fetchall()
        lock_queries_list = list(all_locked_queries)

        get_all_wallets = map(lambda all_locked_queries: all_locked_queries[2].split(', ')[1], all_locked_queries)
        sort_unique_wallets = sorted_nicely( set(get_all_wallets) )

        for wallet in sort_unique_wallets:
            # get all queries that are linked to unique wallet
            queries_for_unique_wallet = [query for query in lock_queries_list if wallet in query[2]]
            to_reward_user = 0
            mysql_id_rewarded = []
            blockheight_rewarded = []
            update_rewarded_semaphore_query = ''

            print('unique wallet', queries_for_unique_wallet)

            for query in queries_for_unique_wallet:
                query_id = query[0]
                query_app = query[1]
                query_asset_id = str(reward_data[query_app]['asset_id'])
                query_type = str(query[2].split(', ')[0])
                query_reward =  reward_data[query_app]['rewards'][query_type]

                mysql_id_rewarded.append(query_id)
                blockheight_rewarded.append(query[3])
                to_reward_user += query_reward
                print('current id', query_id, 'new mysql id', mysql_id_rewarded)

            mysql_id_tuple = tuple(mysql_id_rewarded)
            kat_bc_attch = str('reward for activty on {0} for block height: {1}'.format(query_app, str(blockheight_rewarded)))

            sender.sendAsset(recipient=py.Address(address=wallet), asset=py.Asset(query_asset_id), amount=to_reward_user, attachment=kat_bc_attch)

            if(len(mysql_id_tuple) == 1):
                update_rewarded_semaphore_query = "UPDATE pol_record SET semaphore='1' WHERE id={0};".format(str(mysql_id_tuple[0]))
                print('Inserting into mysql: ', update_rewarded_semaphore_query)
                cursor.execute(update_rewarded_semaphore_query)
                connection.commit()

            elif (len(mysql_id_tuple) > 1):
                update_rewarded_semaphore_query = "UPDATE pol_record SET semaphore='1' WHERE id in {0};".format(mysql_id_tuple)
                print('Inserting into mysql: ', update_rewarded_semaphore_query)
                cursor.execute(update_rewarded_semaphore_query)
                connection.commit()


            logging.info('{0}: User is rewarded: {1} {2} is send to {3} from {4}. MySql command executed: {5}'.format(current_height, to_reward_user, query_asset_id, wallet, sender.address, update_rewarded_semaphore_query))

except KeyboardInterrupt:
    logging.info('Keyboard interrupt. Exiting the program.')
    sys.exit()

except Exception as e:
    logging.error('Error occured in connecting to database: {}'.format(str(e)) )

finally:
    connection.close()
