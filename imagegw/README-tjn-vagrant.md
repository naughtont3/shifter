TJN Vagrant Setup Notes
-----------------------

Setup a Ubuntu 16.04 Vagrant VM for testing Shifter.
Our tests were run using VirtualBox v4.3.30 on a
Mac with Vagrant v1.8.1.


Steps
-----

Create direcectory for vagrant machines, and our Ubuntu 16.04 machine

    ```
      mkdir $HOME/vagrant/
      mkdir $HOME/vagrant/ubuntu1604/
    ```

Change to directory to initialize our Ubuntu 16.04 box via Vagrant

    ```
      cd $HOME/vagrant/ubuntu1604/
      vagrant init ubuntu/xenial64
      vagrant up
    ```

Connecting to the newly created VM 

    ```
      cd $HOME/vagrant/ubuntu1604/
      vagrant ssh
    ```

Notes
-----
    - We add the following customization to the `Vagrantfile`
      to increase the default memory to `2048`. 

        ```
        config.vm.provider "virtualbox" do |vb|  

            # Customize the amount of memory on the VM:
            vb.memory = "2048"

        end
        ```

    - We manually install the developer tools, e.g., `git` in the VM
      using `apt-get install git`.  We also download the Shifter code
      for our development testing.

References
----------

 - "Vagrant: ubuntu/xenial64"
    https://app.vagrantup.com/ubuntu/boxes/xenial64
