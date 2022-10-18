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
import subprocess
import sys
from traceback import print_tb
import toml

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
    config_dict = toml.loads(toml_string)
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
    subprocess.run(['touch /usr/local/opnsense/scripts/OPNsense/ICAPeg/inside_restarticap'], shell=True)
    subprocess.run(['chmod +x ' + icapeg_path], shell=True)
    subprocess.run(['killall -9 icapeg || true'], shell=True)
    subprocess.run([icapeg_path + ' 2> /dev/null &'], shell=True)


main()
