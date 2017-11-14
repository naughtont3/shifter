Docker Notes
------------

Docker
------
 - [OCI Image Manifest Specification](https://github.com/opencontainers/image-spec/blob/master/manifest.md)
    - NOTE: The `Layers` in the `manifest.json` begin with the base layer
      (`layers[0]`) through the top-layer (`layers[len(layers)-1]`).

 - [Docker Image Specification v1.1.0](https://github.com/docker/docker-ce/blob/master/components/engine/image/spec/v1.1.md)
    - [Combined Image JSON + Filesystem Changeset Format v1.1.0](https://github.com/docker/docker-ce/blob/master/components/engine/image/spec/v1.1.md#combined-image-json--filesystem-changeset-format)
    - NOTE: Docker v1.10 was first to use spec v1.1.0.

 - [Docker Image Specification v1.2.0](https://github.com/docker/docker-ce/blob/master/components/engine/image/spec/v1.2.md)
    - [Combined Image JSON + Filesystem Changeset Format v1.2.0](https://github.com/docker/docker-ce/blob/master/components/engine/image/spec/v1.2.md#combined-image-json--filesystem-changeset-format)

 - [Image Tarball format](https://docs.docker.com/engine/api/v1.24/#image-tarball-format)

 - [Example Manifest](https://docs.docker.com/registry/spec/manifest-v2-1/#example-manifest)

 - [Load a tarball with a set of images and tags into docker](https://docs.docker.com/engine/api/v1.24/)

