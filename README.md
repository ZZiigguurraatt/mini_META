# mini_META


## Overview

mini_META is a test suite for validation testing of taproot assets lightning channels. It uses docker to create a small regtest network of 21 nodes. It is similiar to [Polar](https://lightningpolar.com/), but doesn't have a GUI, so it has the flexibility to run more experimental releases of lightning terminal (litd), and it automatically builds containers straight from the litd git repository.









## Usage

- Install
    - `sudo apt install git docker-compose-v2`
    - `git clone https://github.com/ZZiigguurraatt/mini_META`

- Build and start the network
    - `cd mini_META`
    - `./start_mini_META`


- Initialize the network
    - Open a new terminal
    - `docker exec -it mini_meta-controller-1 init_network`
        - Only need to run after first build
        - Mines some blocks, distributes BTC to each node, mints assets, makes TCP connections between nodes, synchronizes universes, and opens initial channels.

- Run tests
    - `docker exec -it mini_meta-controller-1 run_tests`

- Stop nework
    - Switch back to terminal used for `./start_mini_META`
    - `Control-C`

- Erase network and restart
    - `rm -r net_data/`
        - Note: you definitely need to do this step if you rebuild the bitcoind container because then the lightning nodes will be tracking an old regtest network that does not exist and everything will stall.
    - `./start_mini_META`





