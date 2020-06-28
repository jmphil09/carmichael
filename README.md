# Welcome to my Carmichael number repo!

Note: this document is in the process of being updated.

This repo is designed to reproduce and extend the research done here: "insert link to paper here". Note: I am looking for a digital version of the paper to include. I have a hard copy, so I will scan it and create a digital copy if I can't find one soon.

This research was originally done between 2009-2011, and relies heavily on cpu computation power. One of the reasons I have created this repo is to reproduce my original results on much newer hardware in a fraction of the original time. For example, it took a few months of computation time to generate the original results and I can reproduce those results in a couple of days using a Threadripper CPU or a small raspberry pi compute cluster (see below for specifics).

The original results were created with Matlab and Mathematica, when I was new to writing code. The code in this repo is written in Python and, more importantly, I am much better at writing code now!

## How to run the code in this repo

This repository should work on most operating systems. It has been tested with linux (Ubuntu and Centos 7), MacOS, Windows, and on Raspberry Pi 4 running CentOS 7. You will need python 3.6 or later.

To get started:

1) Clone this repo.

2) Create a virtual environment with venv. Example: `python -m venv carm_env` and activate the environment with `source carm_env/bin/activate`. These commands will work on Linux and Mac but are slightly different for Windows.

3) Install the requirements with `python -m pip install -r requirements.txt`. (Use pi4_requirements.txt if using a raspberry pi or other Arm device).

There are 2 main ways to run this code.

1) Use the CarmCalculator class, and run the code locally on one machine. Look at `carm_calculator_example.py` for examples.

2) Use the CarmNodeCalculator class, and run the code on any number of machines as nodes which send data to a main server node. See below for more info.

## How to set up and run a compute cluster of 1 or more nodes
For this example we will:

1) Set up the main server node. This node uses a PostGres database to keep track of the data to compute and lets the compute nodes do the actual computing.

2) Set up a "PC" compute node. (Linux, MacOS, or Windows).

3) Set up a Raspberry Pi compute node on a Raspberry Pi 4. This will work on a 2, 4, or 8 GB model of a pi 4. You can _probably_ get this to run with a 1GB model or a pi 3 as well (Or another Arm device).

### Step 1) Set up the main server node

 - Follow the steps above to set up a virtual environment and install packages from requirements.txt
 - Set up a Postgres Database (The following steps were created using Ubuntu 18.04)
  - `sudo apt-get install wget ca-certificates`
  - `wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -`
  - ``sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'``
  - `sudo apt-get update`
  - `sudo apt-get install postgresql postgresql-contrib`
  - `sudo systemctl start postgresql@12-main`
  - Update the postgres password to "postgres" by entering `sudo passwd postgres` and typing `postgres` twice. (Feel free to use a more secure password and even a different user for the database commands, just remember to update these values in `db_config.py`).
  - `su - postgres`
  - `psql -d template1 -c "ALTER USER postgres WITH PASSWORD 'postgres';"`
  - Press ctrl+d to logout of the postgres user
 - Run `start_server.py`
 - Run `setup_db.py` to automatically set up the Postgres tables. **Important:** If you want to change the prime upper limit, you need to change the `upper_limit` value in `setup_db.py`. The default value for `upper_limit` is 10^6, which was the limit used in the original research paper.

### TODO List
 - Add more values to `db_config.py` and update Step 1) instructions above
 - Add algorithms to compute 4-carmichael numbers
 - Use CUDA to compute carmichael numbers with one or more GPU's
 - Extend the original research by another order of magnitude
