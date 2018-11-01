#!/usr/bin/python

from in_toto.models.layout import Layout, Step
from in_toto.models.metadata import Metablock
from in_toto.util import generate_and_write_rsa_keypair, import_rsa_key_from_file

generate_and_write_rsa_keypair("jenkins_key")
jenkins_key = import_rsa_key_from_file("jenkins_key.pub")

layout = Layout()

build = Step(name="build")
build.pubkeys.append(jenkins_key['keyid'])
layout.steps.append(build)
layout.add_functionary_key(jenkins_key)

scan = Step(name="scan")
scan.expected_products.append(['ALLOW', 'microscanner-report.json'])
scan.pubkeys.append(jenkins_key['keyid'])
layout.steps.append(scan)
layout.add_functionary_key(jenkins_key)

kubesec = Step(name="kubesec")
kubesec.expected_products.append(['ALLOW', 'kubesec-report.json'])
kubesec.pubkeys.append(jenkins_key['keyid'])
layout.steps.append(kubesec)
layout.add_functionary_key(jenkins_key)

scan.pubkeys.append(jenkins_key['keyid'])
kubesec.pubkeys.append(jenkins_key['keyid'])

generate_and_write_rsa_keypair("root_key")
root_key = import_rsa_key_from_file("root_key")

metablock = Metablock(signed=layout)
metablock.sign(root_key)
metablock.dump("root.layout")
