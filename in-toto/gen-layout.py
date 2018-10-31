#!/usr/bin/python

from in_toto.models.layout import Layout, Step
from in_toto.models.metadata import Metablock
from in_toto.util import generate_and_write_rsa_keypair, import_rsa_key_from_file

generate_and_write_rsa_keypair("build_key")
build_key = import_rsa_key_from_file("build_key.pub")

layout = Layout()
build = Step(name="build")
build.expected_materials.append(['ALLOW', 'package.json'])
build.expected_materials.append(['ALLOW', 'index.js'])
layout.steps.append(build)
layout.add_functionary_key(build_key)

build.pubkeys.append(build_key['keyid'])

generate_and_write_rsa_keypair("root_key")
root_key = import_rsa_key_from_file("root_key")

metablock = Metablock(signed=layout)
metablock.sign(root_key)
metablock.dump("root.layout")
