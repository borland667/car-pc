#!/usr/bin/env bash

apt-get update
apt-get install -y dpkg-dev file gcc g++ libc6-dev make patch perl dh-make debhelper devscripts fakeroot gnupg gnupg-agent lintian dupload
apt-get install -y git

git clone https://github.com/dyus/car-pc.git
cd car-pc/
dh_builddeb

# TODO: upload package to debian repository
# TODO: commit and push incremented version of package