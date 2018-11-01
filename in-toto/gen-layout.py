#!/usr/bin/python

from in_toto.models.layout import Layout, Step
from in_toto.models.metadata import Metablock
from in_toto.util import generate_and_write_rsa_keypair, import_rsa_key_from_file

generate_and_write_rsa_keypair("build_key")
generate_and_write_rsa_keypair("scan_key")
build_key = import_rsa_key_from_file("build_key.pub")
scan_key = import_rsa_key_from_file("scan_key.pub")

layout = Layout()
build = Step(name="build")
layout.steps.append(build)
layout.add_functionary_key(build_key)

scan = Step(name="scan")
layout.steps.append(scan)
layout.add_functionary_key(scan_key)

build.pubkeys.append(build_key['keyid'])
scan.pubkeys.append(scan_key['keyid'])

generate_and_write_rsa_keypair("root_key")
root_key = import_rsa_key_from_file("root_key")

metablock = Metablock(signed=layout)
metablock.sign(root_key)
metablock.dump("root.layout")
