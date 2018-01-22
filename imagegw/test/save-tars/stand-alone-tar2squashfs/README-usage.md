Example Usage
-------------

 - 1. Export an OCI save image (e.g., `docker save -o FILE.save.tar`), which
      will be converted to a Squashfs image by this utility.
      The below assumes a file named `tjntest.save.tar`.

 - 2. Convert OCI save image (save.tar) to squashfs image

    ```
    ubuntu-xenial:$ ./image-tar2squashfs-v2.py ./naughtont3-tjntest.save.tar

       ...<snip>...

    ##################################################
      Created image: /tmp/myworkingdir/01f79c97b5f1337c14802e9913e530428e0d1c770a0dd84f2d73cca9aee88c4a.squashfs
      Metadata file: /tmp/myworkingdir/01f79c97b5f1337c14802e9913e530428e0d1c770a0dd84f2d73cca9aee88c4a.meta
    ##################################################
    ```

 - 3. Then this new squashfs image can imported directly into Shifter using
    the recently added `import` command (Shifter-PR-188).


Inspecting Squashfs Image
-------------------------

You can mount the squashfs image directly to ensure the contents are as expected.

    ```
    ubuntu-xenial:$ sudo mount -o loop -t squashfs \
        /tmp/myworkingdir/01f79c97b5f1337c14802e9913e530428e0d1c770a0dd84f2d73cca9aee88c4a.squashfs \
        /mnt
    ```

See the expected `hellosleep` executable

    ```
    ubuntu-xenial:$ ls /mnt/
    bin  dev  etc  home  root  tmp  usr  var
    ubuntu-xenial:$ ls /mnt/usr/bin/hellosleep
    /mnt/usr/bin/hellosleep
    ubuntu-xenial:$
    ```

Unmount the squashfs image

    ```
    ubuntu-xenial:$ sudo umount /mnt
    ```


Example Output
--------------

The following shows example output when running the converter script.

    ```
    ubuntu-xenial:$ ./image-tar2squashfs-v2.py ./naughtont3-tjntest.save.tar
    Parallel mksquashfs: Using 2 processors
    Creating 4.0 filesystem on /tmp/myworkingdir/01f79c97b5f1337c14802e9913e530428e0d1c770a0dd84f2d73cca9aee88c4a.squashfsQWLakl.partial, block size 131072.
    [======================================================================================/] 21/21 100%

    Exportable Squashfs 4.0 filesystem, gzip compressed, data block size 131072
        compressed data, compressed metadata, compressed fragments, compressed xattrs
        duplicates are removed
    Filesystem size 1019.40 Kbytes (1.00 Mbytes)
        51.73% of uncompressed filesystem size (1970.65 Kbytes)
    Inode table size 382 bytes (0.37 Kbytes)
        46.59% of uncompressed inode table size (820 bytes)
    Directory table size 1980 bytes (1.93 Kbytes)
        36.05% of uncompressed directory table size (5492 bytes)
    Number of duplicate files found 0
    Number of inodes 22
    Number of files 7
    Number of fragments 1
    Number of symbolic links  1
    Number of device nodes 0
    Number of fifo nodes 0
    Number of socket nodes 0
    Number of directories 14
    Number of ids (unique uids + gids) 1
    Number of uids 1
        root (0)
    Number of gids 1
        root (0)
    ##################################################
      Created image: /tmp/myworkingdir/01f79c97b5f1337c14802e9913e530428e0d1c770a0dd84f2d73cca9aee88c4a.squashfs
      Metadata file: /tmp/myworkingdir/01f79c97b5f1337c14802e9913e530428e0d1c770a0dd84f2d73cca9aee88c4a.meta
    ##################################################
    ubuntu-xenial:$
    ```
