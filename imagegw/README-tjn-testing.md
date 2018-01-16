README TJN Testing Notes
-------------------------

Quick summary of steps used in testing with `curl_*.sh` and `tjn_setup.sh`.

- NOTE: I tested this using a Ubuntu 16.04 Vagrant VM environment, which can run
  the Shifter testing environment in Docker containers (within the VM).  I
  assume you know how to create a Vagrant VM and have already checkout all
  the Shifter Git code.  The following just starts the VM and gets started.

Initial Startup
---------------

   ```
     # Start the VM
    cd  $HOME/vagrant/ubuntu1604/
    vagrant up
   ```

- Connect to VM

   ```
    vagrant ssh
   ```

- Create/Start Shifter Docker containers for testing (in VM)

   ```
    cd /home/ubuntu/projects/shifter/naughtont3-shifter/imagegw/
    make -f Makefile.test starttest
   ```

- Show Docker containers running (in VM)

   ```
    ubuntu-xenial:$ docker ps
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
    cdf14307f0a1        imagegwapi          "./entrypoint.sh work"   28 minutes ago      Up 28 minutes                                imagegw_workera_1
    96874fe93e78        shifter-test        "/entrypoint.sh"         28 minutes ago      Up 28 minutes       0.0.0.0:2222->22/tcp     systema
    6fed1cf8cbfd        imagegwapi          "./entrypoint.sh mung"   5 weeks ago         Up 28 minutes       0.0.0.0:5555->5000/tcp   imagegw_api_1
    31c71f5d96a4        mongo:2.6           "/entrypoint.sh --sma"   7 weeks ago         Up 28 minutes       27017/tcp                imagegw_mongo_1
    56d0d96d2ea6        redis               "docker-entrypoint.sh"   7 weeks ago         Up 28 minutes       6379/tcp                 imagegw_redis_1
   ```


- Start three terminals for testing
    - Terminal-1: Systema (user commands)
    - Terminal-2: ImageGW-API
    - Terminal-3: ImageGW-Worker
    - See below for per-teriminal commands


Terminal-1: Systema
-------------------

- Connect to VM

   ```
    cd  $HOME/vagrant/ubuntu1604/
    vagrant ssh
   ```

- Connect to `systema` Docker container (in VM)

   ```
    docker exec -ti systema bash
   ```

- Change to source code directory with our helper scripts

   ```
    root# cd /src/imagegw/
    root# ls *.sh
    curl_list.sh  curl_load.sh  curl_pull.sh  entrypoint.sh  tjn_setup.sh
   ```


Terminal-2: ImageGW-API
-----------------------

- Connect to VM

   ```
    cd  $HOME/vagrant/ubuntu1604/
    vagrant ssh
   ```

- Connect to `imagegw_api_1` Docker container (in VM)

   ```
    docker exec -ti imagegw_api_1 bash
   ```

- Tail ImageGW-API process log (`gunicorn.log`) (in Docker, in VM)

   ```
    tail -f /var/log/gunicorn.log
   ```


Terminal-3: ImageGW-Worker
--------------------------

- Connect to VM

   ```
    cd  $HOME/vagrant/ubuntu1604/
    vagrant ssh
   ```

- Connect to `imagegw_workera_1` Docker container (in VM)

   ```
    docker exec -ti imagegw_workera_1 bash
   ```

- Tail ImageGW-Worker process log (`celery.log`) (in Docker, in VM)

   ```
    tail -f /var/log/celery.log
   ```


Testing/Development
-------------------

We run most of our commands from Terminal-1, via the `systema` Docker container

- Stage the saved image we want to load

   ```
    root# cd /src/imagegw/
    root# ./tjn_setup.sh
   ```

- Show current Shifter images in system (e.g., from previous load/pull/etc.)

   ```
    root# ./curl_list.sh
   ```

- Pull an image manually (same as `shifterimg pull xyz`)

   ```
    root# ./curl_pull.sh
   ```

- Load an image manually

   ```
    root# ./curl_load.sh
   ```

