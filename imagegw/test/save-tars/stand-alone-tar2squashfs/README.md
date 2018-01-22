README
------

Simple utility to convert an OCI saved image to a Shifter squashfs image.

In short, this converts an save.tar archive created using a command like,
`docker save -o FILE.save.tar`, to a `squashfs` version of the image.  The
resulting squashfs image can then be imported directly into Shifter using
the recently added `import` command (Shifter-PR-188).

 - [Shifter-PR-188](https://github.com/NERSC/shifter/pull/188)


NOTES
-----
 - This work assumes a version of Shifter that includes the 'import' capability,
   which was added to the Shifter development branch in Nov-2017.

 - This work was guided by the Shifter PR-176 and subsequent PR-188 for
   importing a squashfs image.
    - [Shifter PullRequest-176](https://github.com/NERSC/shifter/pull/176)
    - [Shifter-PR-188](https://github.com/NERSC/shifter/pull/188)

 - This code assumes an OCI image specification v1.1 (Docker >=1.10) or higher.
    - [Docker Image Specification v1.1.0](https://github.com/docker/docker-ce/blob/master/components/engine/image/spec/v1.1.md)
    - [Combined Image JSON + Filesystem Changeset Format v1.1.0](https://github.com/docker/docker-ce/blob/master/components/engine/image/spec/v1.1.md#combined-image-json--filesystem-changeset-format)

 - The Docker `Layers` in the `manifest.json` file for the [OCI Image Manifest Specification](https://github.com/opencontainers/image-spec/blob/master/manifest.md),
   begin with the base layer (`layers[0]`) through the top-layer
   (`layers[len(layers)-1]`).

 - Note: The `shifter_converts.py` and `shifter_util.py` files were extracted
   from the Shifter imagegw code and saved locally for use by our tool.
   The copyrights were retained as-is.  The files were prefixed with
   `shifter_` to clearly indicate they were taken from the Shifter code and
   to avoid any conflicts with the original filenames.
