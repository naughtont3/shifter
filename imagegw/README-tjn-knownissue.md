Known Issues
------------

 - 1. Assume single fileystem for ImageGateway servers and user

    - TL;DR - run `tjn_setup.sh` in `systema` & `imagegw_worker_1` containers

    - Description: There is a problem with the pathing for the
      transfer.tranfer() code added for the ImageGateway worker.  The
      problem only occurs when the ImagewGW (imagegw_worker_1) and User
      (systema) environments do not have the same filesystem.  The correct
      action would be to have the transfer() routine copy the User's file to
      the proper location on ImageGW.

    - Work-Around: When testing imagegw under the Docker based environment,
      copy the 'tjntest.save.tar' file to '/tmp/testing/tjntest.save.tar'
      on both the `systema` and `imagegw_workera_1` containers.

        - Systema Docker container (`systema`)

         ```
            ubuntu:$ docker exec -ti systema bash
            root# cd /src/imagegw/
            root# ./tjn_setup.sh
         ```

            - (systema) Required Paths: /tmp/testing/tjntest.save.tar


        - ImageGW-Worker Docker container (`imagegw_workera_1`)

         ```
            ubuntu:$ docker exec -ti imagegw_workera_1 bash
            root# cd /usr/src/app/
            root# ./tjn_setup.sh
         ```

