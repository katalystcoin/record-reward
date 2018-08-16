# File system

The files are being organised as per their functions.

In general, there are 3 main systems involved in the POL structure.

__1.__ App backend database

_Run by app owner, e.g. daebak database_


__2.__ POL database

_Run by Katalyst_

This database record all the recorded activity as the structure below:

```
id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
app_name VARCHAR(10) NOT NULL,
data, [structure will be explained below]
hash CHAR(64), [using SHA256
timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
semaphore CHAR(1) DEFAULT 0,   
blockheight INT(10) UNSIGNED
```


__3.__ Katalyst blockchain

_Decentralise_

View our explorer at https://e.katalystcoin.com

### mysql-to-POL-recording

The scripts inside this folder will detect __NEW INSERT__ in the APP database and send the information to the POL database.

App database owners will have to __INSERT__ data in this format in order for the rewarding to work:
```
<type of activity>, <wallet address to reward>, <copy>
```

### POL-to-blockchain-recording

The scripts inside this folder will detect __INSERT__ in the POL database which has _null_ in the hash column. It will hash the id and the data in SHA256 hash and send to the blockchain.

### blockchain-POL-rewarding

The scripts will first inside this folder will detect the entry in the POL blockchain. It will read the transactions in (current blockheight() -1). If there is an attachment, it will be base58 decoded. The resulting decoded string will be the hash from the POL database.

Once the row with the hash is detected and _semaphore='0'_, it will locked the row by  __UPDATE__ semaphore='L'.

When a row with semaphore='L' is detected, the script will carry out its rewarding algorithm of the amount to reward by type to the wallet address in the data field.

Once the rewarding is done, the row will __UPDATE__ semaphore='1'.


# Running the scripts

Create a virtual environment before downloading dependencies and running the scripts to prevent conflicts of packages. These are instructions for running the script on Ubuntu.

## How to install a virtualenv:

### Install pip first

```
sudo apt-get install python3-pip
```

### Then install virtualenv using pip3

```
sudo pip3 install virtualenv
```

### Create a virtual environment

```
virtualenv venv
```

> You can use any name instead of **venv**

### You can also use a Python interpreter of your choice

```
virtualenv -p /usr/bin/python2.7 venv
```

### Activate your virtual environment:    

```
source venv/bin/activate
```

### To deactivate:

```
deactivate
```


### Run the script in virtual environment in screen

> Before running the various script, make sure the file is executable by running chmod +x name_of_file.
> The shell script in this repo is just for reference.
> _To note: bash script written in Windows cannot be run on Linux._
> To write the script on the machine that is running the script.  For the reward scripts, it will be preferably run in an interval of 10 seconds prevent missing out of any block.

```
screen -S <name_of_screen>
./run.sh

screen -S <name_of_second_screen>
./reward.sh
```
