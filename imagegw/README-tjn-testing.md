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

- **NOTE**: See also `README-tjn-knownissues.md` for manual setup steps for
     each of the three terminals (actually only Terminal-1 and Terminal-3).


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

- Change to source code directory with our helper scripts (in Docker, in VM)

   ```
    root# cd /src/imagegw/
    root# ls *.sh
    curl_list.sh  curl_load.sh  curl_pull.sh  entrypoint.sh  tjn_setup.sh
   ```

- **NOTE**: See also `README-tjn-knownissues.md` for manual setup steps (in Docker, in VM)

- To list existing images (in Docker, in VM):

   ```
    root# ./curl_list.sh
   ```

- To load a saved image (in Docker, in VM):

   ```
    root# ./curl_load.sh
   ```

- Assuming no errors, you should now see the image, either by running
  `curl_list.sh` or `shifterimg images`.


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

- **NOTE**: See also `README-tjn-knownissues.md` for manual setup steps (in Docker, in VM)

- Tail ImageGW-Worker process log (`celery.log`) (in Docker, in VM)

   ```
    tail -f /var/log/celery.log
   ```


Testing/Development
-------------------

We run most of our commands from Terminal-1, via the `systema` Docker container

- **NOTE**: See also `README-tjn-knownissues.md` for manual setup steps.

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

Running a Shifter Image in Docker Devel Environment
---------------------------------------------------

We run most of our commands from Terminal-1, via the `systema` Docker container

- Connect to `systema` Docker container (in VM)

   ```
    docker exec -ti systema bash
   ```

- Become a standard user (e.g., `canon`) (in Docker, in VM)

   ```
    root# su - canon
    canon@4500e3e05c69:~$
   ```

- As standard user, verify `shifter` and `shifterimg` in PATH (in Docker, in VM)

   ```
    canon@4500e3e05c69:~$ which shifter
    /opt/shifter/udiRoot/1.0/bin//shifter
    canon@4500e3e05c69:~$ which shifterimg
    /opt/shifter/udiRoot/1.0/bin//shifterimg
   ```

- List available images using `shifterimg` (in Docker, in VM)

   ```
    canon@4500e3e05c69:~$ shifterimg images
    systema    docker     READY    01f79c97b5   2018-01-21T23:26:59  tjntest:latest
    canon@4500e3e05c69:~$
   ```

- Launch container `tjntest:latest` with `hellosleep` executable (in Docker, in VM)

   ```
    canon@4500e3e05c69:~$ shifter --image=docker:tjntest:latest
    ~ $
    ~ $ hellosleep 5
    [372] INFO: PID = 372
    [372] INFO: 4500e3e05c69 Linux-4.4.0-109-generic  libc-2.23.stable
    [372] INFO: SLEEP 5  (loopcount: 1, total: 5)
    ~ $
   ```

