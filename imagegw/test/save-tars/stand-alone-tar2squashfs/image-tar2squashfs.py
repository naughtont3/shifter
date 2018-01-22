#!/usr/bin/env python2
#
# Shifter, Copyright (c) 2015, The Regents of the University of California,
# through Lawrence Berkeley National Laboratory (subject to receipt of any
# required approvals from the U.S. Dept. of Energy).  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#  1. Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#  3. Neither the name of the University of California, Lawrence Berkeley
#     National Laboratory, U.S. Dept. of Energy nor the names of its
#     contributors may be used to endorse or promote products derived from this
#     software without specific prior written permission.`
#
# See LICENSE for full text.
#  - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - -
#
# Copyright (c) 2017       UT Battelle, LLC. All rights reserved.
#
# Authors:
#   Thomas Naughton <naughtont@ornl.gov>
#
# TJN: Portions of the code were taken from the Shifter code so including
#      that Copyright notice as well (see above).
#
#--------------------------------------------------------------------------
# NOTES:
#  - Tested with 'naughtont3-iperf-ubuntu.save.tar'
#                'naughtont3-tjntest.save.tar'
#  - Refs:
#  -  - [OCI Image Manifest Specification](https://github.com/opencontainers/image-spec/blob/master/manifest.md)
#     - NOTE: The `Layers` in the `manifest.json` begin with the base layer
#          (`layers[0]`) through the top-layer (`layers[len(layers)-1]`).
#
#  - Docker Image Spec v1.1md (adopted in Docker v1.10)
#    https://github.com/docker/docker-ce/blob/master/components/engine/image/spec/v1.1.md
#
#####

import json
import io
import sys
import os
import tarfile
import tempfile
import shutil
from subprocess import Popen, PIPE

# TJN: Following 2 modules from Shifter (16.04) code (see README.md notes)
import shifter_util
import shifter_converters

VERBOSE = 0
WORKDIR = '/tmp/myworkingdir'

def inflate_savefile(options, expand_dir, cache_dir):
    """
    Do all the driver work in single routine for now.
    """
    scratch_dir = None
    filepath = options['filePath']
    manifest_file = None
    base_working_dir = expand_dir
    image_base_dir = None

    repo = None
    tag = None
    image_id = None
    file_path = filepath

    scratch_dir = tempfile.mkdtemp(suffix='scratch',
                                   prefix='FooBarID',
                                   dir=base_working_dir)
    try:
        tar = tarfile.open(file_path)
        tar.extractall(scratch_dir)
        tar.close()
        if VERBOSE > 0:
            print "DBG: Extracted %s to %s" % (file_path, scratch_dir)
    except:
        raise ValueError("failed while opening archive")

    manifest_file = scratch_dir + "/manifest.json"
    if VERBOSE > 0:
        print "DBG: Manifest-file: %s" % manifest_file

    json_data = open(manifest_file)
    jdata = json.load(json_data)
    # print "====================================================================="
    # print json.dumps(jdata, sort_keys=True, indent=4, separators=(',', ':'))
    # print "====================================================================="


    config_file = jdata[0]['Config']
    if VERBOSE > 0:
        print "DBG: Manifest-CfgFile: %s" % config_file
    image_id, _junk = config_file.split(".")

    # Just take the 1st repotag (not sure if we can have more?)
    repotag = jdata[0]['RepoTags'][0]
    repo,tag = repotag.split(":")
    if VERBOSE > 0:
        print "DBG: REPOTAG: ", repotag
        print "DBG:    REPO: ", repo
        print "DBG:    TAG: ", tag
        print "DBG: ImageID: %s " % image_id

    repo = repo
    tag = tag
    image_id = image_id

    # # XXX: We should probably use the normal ExpandDir in CONFIG
    #expand_dir = os.path.join(scratch_dir, "expand")
    #if not os.path.exists(expand_dir):
    #    os.mkdir(expand_dir)

    layers = jdata[0]['Layers']
    youngest = layers[len(layers)-1]
    youngest_id = (youngest.split("/"))[0]
    #print "DBG: youngest_id: %s" % youngest_id
    image_config_file = os.path.join(scratch_dir, youngest_id, "json")

    if VERBOSE > 0:
        print "  Config file: %s" % image_config_file

    # Get path to 'config' file within image manifest archive
    try:
        json_cdata = open(image_config_file)
        cdata = json.load(json_cdata)
    except:
        print "E135"
        raise

    if VERBOSE > 0:
        print "=================== Config Data ====================================="
        print json.dumps(cdata, sort_keys=True, indent=4, separators=(',', ':'))
        print "====================================================================="

    ################
    # NOTE: The 'youngest' layer for manifest should match
    #       the config info we get from 'image_config_file' (see above)
    #       but the 'image_config_file' also has history and other entries.
    # NOTE: The format of this 'manifest' info is not the same as
    #       what we have with a loaded image, we have subset of data
    #       that we must use to create/initialize full data,
    #       e.g., 'id' key not in the 'config' dictionary in save.tar
    #       manifest.json or image_config_file.
    ################
    # Get image config details (i.e., metadata)
    try:
        #config = cdata[0]['Config']  # if use <topdir>/<id>.json
        config = cdata['config']      # if use <topdir>/<youngest_layer>/json
    except:
        print "E157"
        raise

    # Metadata
    if 'Env' in config:
        envdata = config['Env']
        for e in envdata:
            k,v = e.split("=")
            if VERBOSE > 0:
                print " ENV:  %s = %s" % (k,v)

    if 'Entrypoint' in config:
        entrypt = config['Entrypoint']
        if VERBOSE > 0:
            print "Entrypoint: %s" % entrypt

    if 'Workdir' in config:
        # lowercase
        config['workdir'] = config['Workdir']
        if VERBOSE > 0:
            print "Workdir: %s" % config['workdir']

    # HACKS: set so we pass out the metadata (expects lowercase)
    config['env'] = config['Env']
    config['entrypoint'] = config['Entrypoint']
    options['env'] = config['Env']
    options['entrypoint'] = config['Entrypoint']

    # XXX: Not sure what we should be returning here,
    #      but for sure need these 3 pieces of info
    #      so add to other config info and return
    if 'id' not in config:
        config['id'] = image_id
    if 'repo' not in config:
        config['repo'] = repo
    if 'tag' not in config:
        config['tag'] = tag

    ###
    # TODO: TJN This is where we get the proper files from tar layers.
    #       Note, it slightly differs from pull b/c of the different
    #       manifest format in save.tar layout.
    ###
    def filter_layer(layer_members, to_remove):
        """Remove members and members starting with to_remove from layer"""
        trailing = '/' if not to_remove.endswith('/') else ''
        prefix_to_remove = to_remove + trailing

        return [x for x in layer_members \
                if (not x.name == to_remove
                    and not x.name.startswith(prefix_to_remove))]

    layer_paths = []
    tar_file_refs = []
    for x in layers:
        #print "Layer: %s" % x
        try:
            tfname = scratch_dir + "/" + x
            #print "Expand: %s" % tfname
            tar = tarfile.open(tfname)
            tar_file_refs.append(tar)

            ## get directory of tar contents
            members = tar.getmembers()

            ## remove all illegal files
            members = filter_layer(members, 'dev/')
            members = filter_layer(members, '/')
            members = [z for z in members if not z.name.find('..') >= 0]

            ## find all whiteouts
            whiteouts = [z for z in members \
                    if z.name.find('/.wh.') >= 0 or z.name.startswith('.wh.')]

            ## remove the whiteout tags from this layer
            for wh_ in whiteouts:
                members.remove(wh_)

            ## remove the whiteout targets from all ancestral layers
            for idx, ancs_layer in enumerate(layer_paths):
                for wh_ in whiteouts:
                    path = wh_.name.replace('/.wh.', '/')
                    if path.startswith('.wh.'):
                        path = path[4:]
                    ancs_layer_iter = (z for z in ancs_layer if z.name == path)
                    ancs_member = next(ancs_layer_iter, None)
                    if ancs_member:
                        ancs_layer = filter_layer(ancs_layer, path)
                layer_paths[idx] = ancs_layer

            ## remove identical paths (not dirs) from all ancestral layers
            notdirs = [z.name for z in members if not z.isdir()]
            for idx, ancs_layer in enumerate(layer_paths):
                ancs_layer = [z for z in ancs_layer if not z.name in notdirs]
                layer_paths[idx] = ancs_layer

            ## push this layer into the collection
            layer_paths.append(members)

        except:
            print "E255"
            raise


    # # Extract the selected files from layers
    # layer_idx = 0
    # for x in layers:
    #    #print "Layer: %s" % x
    #    tar = tar_file_refs[layer_idx]
    #    members = layer_paths[layer_idx]
    #    for m in members:
    #        print "M: %s" % m
    #    layer_idx += 1

    image_base_dir = os.path.join(expand_dir, image_id)

    #
    # Extract Tar layers
    #
    layer_idx = 0
    for x in layers:
        #print "Layer: %s" % x
        try:
            tar = tar_file_refs[layer_idx]
            members = layer_paths[layer_idx]
            #print "Expand: %s" % tar
            #tar.extractall(path=expand_dir, members=members)
            tar.extractall(path=image_base_dir, members=members)

            layer_idx += 1
        except:
            print "E286"
            raise

    for tar in tar_file_refs:
        tar.close()

    #print "Expand_dir: %s" % expand_dir
    if VERBOSE > 0:
        print "Expand_dir: %s" % image_base_dir


    if VERBOSE > 0:
        print "DELETING ScratchDir: %s " % scratch_dir
    shutil.rmtree(scratch_dir)

    # fix permissions on the extracted files
    #cmd = ['chmod', '-R', 'a+rX,u+w', expand_dir]
    cmd = ['chmod', '-R', 'a+rX,u+w', image_base_dir]
    pfp = Popen(cmd)
    pfp.communicate()

    return config

def do_metadata(options, image_id, repo, tag, edir):

    # TJN - Manually set items we know are needed by caller
    request = {}
    request['meta'] = {}

    request['id']           = image_id
    request['meta']['id']   = image_id
    request['meta']['repo'] = repo
    request['meta']['tag']  = tag

    if 'env' in options:
        request['meta']['env']  = options['env']
    if 'entrypoint' in options:
        request['meta']['entrypoint']  = options['entrypoint']
    if 'workdir' in options:
        request['meta']['workdir']  = options['workdir']

    expandedpath = os.path.join(edir, '%s' % request['id'])
    request['expandedpath'] = expandedpath

def main():
    script = sys.argv[0]

    if len(sys.argv) < 2:
        print "ERROR: Missing archive filename"
        print "Usage: %s FILE.tar" % script
        sys.exit(1)

    base_working_dir = WORKDIR
    base_expand_dir = os.path.join(base_working_dir, '%s' % 'expand')

    try:
        if not os.path.exists(base_working_dir):
            os.mkdir(base_working_dir)

        if not os.path.exists(base_expand_dir):
            os.mkdir(base_expand_dir)

        archive_file = str(sys.argv[1])
        scratch_dir = tempfile.mkdtemp(suffix='scratch',
                                       prefix='FooID',
                                       dir=base_working_dir)

        # Important Keys
        #   id
        #   repo
        #   tag
        #   filePath  # need to fix naming to avoid dup
        #   filepath
        #   imagefile
        #   entrypoint
        #   workdir
        #   env
        #
        manifest = inflate_savefile({'filePath':archive_file},
                                    cache_dir=base_working_dir,
                                    expand_dir=base_expand_dir)

        if not 'id' in manifest:
            raise OSError('Missing id key in manifest')

        image_id = manifest['id']
#         do_metadata(manifest,
#                     image_id=manifest['id'],
#                     repo=manifest['repo'],
#                     tag=manifest['tag'],
#                     edir=base_working_dir)

        fmt = 'squashfs'
        image_path = os.path.join(base_working_dir, '%s.%s' % (image_id, fmt))
        expand_dir = os.path.join(base_expand_dir, '%s' % image_id)

        if VERBOSE > 0:
            print "*****************************************"
            print ""
            print "DBG:        fmt: %s" % fmt
            print "DBG:  expand_dir: %s" % expand_dir
            print "DBG: image_path: %s" % image_path
            print ""
            print "*****************************************"

        if not shifter_converters.convert(fmt, expand_dir, image_path):
            raise OSError('Convert image failed')

        # TJN - Manually set items we know are needed for metadata
        info = {}
        info['meta'] = {}

        info['id']           = manifest['id']
        info['meta']['id']   = manifest['id']
        info['meta']['repo'] = manifest['repo']
        info['meta']['tag']  = manifest['tag']
        info['expandedpath'] = expand_dir

        if 'env' in manifest:
            info['meta']['env']  = manifest['env']
        if 'entrypoint' in manifest:
            info['meta']['entrypoint']  = manifest['entrypoint']
        if 'workdir' in manifest:
            info['meta']['workdir']  = manifest['workdir']

        metafile = os.path.join(base_working_dir, '%s.%s' % (image_id, 'meta'))
        if not shifter_converters.writemeta(fmt, info, metafile):
            raise OSError('Metadata file creation failed')

        print "##################################################"
        print "  Created image: %s" % image_path
        print "  Metadata file: %s" % metafile
        print "##################################################"
        return True

    except:
        print "ERROR: failed to load image"
        raise

###
# MAIN
###
if __name__ == '__main__':
    main()

