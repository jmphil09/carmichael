# Welcome to my Carmichael number repo!

This repo is designed to reproduce and extend the research done in my Master's Thesis:
[Phillips_thesis_final.pdf](Phillips_thesis_final.pdf)

This research was originally done between 2009-2011, and relies heavily on cpu computation power. One of the reasons I have created this repo is to reproduce my original results on much newer hardware in a fraction of the original time. For example, it took a few months of computation time to generate the original results and I can reproduce those results in a couple of days using a Threadripper CPU or a small raspberry pi compute cluster (see below for specifics).

The original results were created with Matlab and Mathematica, when I was new to writing code. The code in this repo is written in Python and, more importantly, I am much better at writing code now!

## How to run the code in this repo

This repository should work on most operating systems. It has been tested with linux (Ubuntu and Centos 7), MacOS, Windows, and on Raspberry Pi 4 running CentOS 7. You will need python 3.7 or later.

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

### Step 2) Set up a PC compute node

This can be done on the same machine you used as the main server node, or any other machine on the same local network as the main node. (With some tweaking, you could set up a static IP address for a machine on a different network, but we will assume all nodes in this tutorial are on the same network).

 - If using a different machine than the server node, clone this repo and install the requirements from `requirements.txt` as above.
 - In `compute_node_config.py`, change the `SERVER_URL` to the IP address of your server node.
 - In `compute_node_config.py`, change `NUM_CORES` to the number of CPU cores you wish to use on your worker node.
 - Optional: Play around with `BATCH_SIZE`, or the other values in `compute_node_config.py`. Refer to the comments in that file to see what the different values do. By default, these values will auto-adjust depending on how fast or slow the worker node is sending results back to the compute node.
 - Run the node with `python start_compute_node.py`.

### Step 3) Set up a Raspberry pi compute node

 - Follow the instructions in [Raspberry_Pi_4_Setup_Guide.txt](Raspberry_Pi_4_Setup_Guide.txt)
 - Update `compute_node_config.py` as in Step 2) above.
 - After following these steps, whenever the Raspberry pi boots it will pull the latest code from this repo (you can specify your own fork during the setup guide) and will run `start_compute_node.py`.
 - If you want to setup multiple Raspberry Pi's, you can follow the steps above for each pi (or you can create copies of the pi's sd card to save some time).
 - Note: right now these instructions will setup python 3.6 on the Raspberry Pi. This will work fine for computing numbers, but if you plan on using a Raspberry Pi for your main server node, or to run some of the database scripts, you will need python 3.7.

### TODO List
 - Add algorithms to compute 4-carmichael numbers and Chernick universal forms
 - Extend the original research by another order of magnitude
 - Use CUDA to compute carmichael numbers with one or more GPU's
