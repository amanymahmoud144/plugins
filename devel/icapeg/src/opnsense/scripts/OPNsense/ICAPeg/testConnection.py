#!/usr/local/bin/python3

"""
    Copyright (c) 2015-2019 Ad Schellevis <ad@opnsense.org>
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES,
    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
    AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
    AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
    OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
    SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
    INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
    CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.

    --------------------------------------------------------------------------------------

    perform some tests for the icapeg application
"""
from operator import itemgetter
import string
import subprocess
import sys
from traceback import print_tb
import toml
import re
import json
import fileinput

Conf_file_path = "/usr/local/etc/icapeg/icapeg.conf"
toml_file_path = "/usr/local/opnsense/scripts/OPNsense/ICAPeg/config.toml"
icapeg_path = "/usr/local/opnsense/scripts/OPNsense/ICAPeg/icapeg"


def main():
    subprocess.run(['touch /usr/local/opnsense/scripts/OPNsense/ICAPeg/outside_main'], shell=True)
    update_toml(Conf_file_path,toml_file_path)
    restart_icapeg(icapeg_path)

def update_toml(Conf_file_path,toml_file_path):
    subprocess.run(['touch /usr/local/opnsense/scripts/OPNsense/ICAPeg/inside_updateToml'], shell=True)
    toml_file = toml.load(toml_file_path) 
    conf_file = open(Conf_file_path, 'r')
    toml_string = conf_file.read()
    toml_string_rep=(toml_string.replace('1"', 'true"'))
    toml_string_rep1=(toml_string_rep.replace('0"', 'false"'))
    toml_string_rep2=(toml_string_rep1.replace("TXT", '"txt"'))
    toml_string_rep3=(toml_string_rep2.replace("EXE", '"exe"'))
    toml_string_rep4=(toml_string_rep3.replace("DOCX", '"docx"'))
    toml_string_rep5=(toml_string_rep4.replace("DOC", '"doc"'))
    toml_string_rep6=(toml_string_rep5.replace("PDF", '"pdf"'))
    toml_string_rep7=(toml_string_rep6.replace("ZIP", '"zip"'))


    config_dict = toml.loads(toml_string_rep7)
    for key_1 in config_dict:
        if type(config_dict[key_1]) is dict:
            for key_2 in config_dict[key_1]:
                toml_file[key_1][key_2] = config_dict[key_1][key_2]
        else:
            toml_file[key_1] = config_dict[key_1]

    config_toml = open("/usr/local/opnsense/scripts/OPNsense/ICAPeg/config.toml",'w')
    toml.dump(toml_file, config_toml)
    config_toml.close()
        


def restart_icapeg(icapeg_path):
    subprocess.run(['cp /usr/local/opnsense/scripts/OPNsense/ICAPeg/block-page.html .'], shell=True)
    subprocess.run(['cp /usr/local/opnsense/scripts/OPNsense/ICAPeg/config.toml .'], shell=True)
    subprocess.run(['chmod +x ' + icapeg_path], shell=True)
    subprocess.run(['killall -9 icapeg || true'], shell=True)
    subprocess.run([icapeg_path + ' 2> /dev/null &'], shell=True)


main()
