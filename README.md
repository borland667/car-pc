car-pc
======
The idea is to get information from car devices, sensors, processing that information, load data to storage, remote access to car devices. As server we will use raspberry pi or some compact like nettop. 

Tasks are: 
----------
1. Processing video from (web) cameras.
2. Streaming video to the Internet
3. Remote start engine
4. Geting location via GPS
5. Controlling devices of the car by voice commands
6. Controlling fuel consumption and mark up it on the map
7. Wi-fi voice connection between two twined cars (in case of joint travel)
8. Music and video center with possibility of separation for each passenger
9. Control of barriers and gates via IR receiver


Links:
----------
OBD2:
 1. http://www.stuffaboutcode.com/2013/07/raspberry-pi-reading-car-obd-ii-data.html
 2. https://github.com/martinohanlon/pyobd


Installing - debian:
----------
 1. add "deb http://repo.car-pc-online.com/binary amd64/" at /etc/apt/sources.list
 2. sudo apt-get update
 3. sudo apt-get install carpc

Installing - manual:
----------
 1. sudo apt-get install streamer vlc nodejs
 2. sudo npm install bower -g
 3. git clone https://github.com/dyus/car-pc.git
 4. cd car-pc/backend
 5. virtualenv --system-site-packages virt_env
 6. virt_env/bin/activate install -r requirements.txt
 7. cp project/settings_example.py project/settings.py
 8. virt_env/bin/python manage.py syncdb
 9. virt_env/bin/python manage.py migrate
 10. virt_env/bin/python manage.py loaddata obd_sensors
 11. cd ../frontend
 12. bower install

Starting (draft):
----------
 1. cd backend; ./manage.py supervisor
 2. cd frontend/www; python -m SimpleHTTPServer
 3. vlc -I http --http-password 123



Dev notes:
----------
 ./manage.py dumpdata obd.Sensor --indent=4 > obd/fixtures/obd_sensors.json


Build deb package via vagrant:
----------
 1. install vagrant
 2. install ansible
 3. copy gpg public and private keys at vagrant/ssh_keys/robot-public.key and vagrant/ssh_keys/robot-private.key for signing deb package
 4. add own ssh public key at .ssh/autorized_keys at git repository (github.com)
 5. add own ssh public key at .ssh/autorized_keys at deb repository (repo.car-pc-online.com)




