car-pc
======
The idea is to get information from car devices, sensors, processing that information, load data to storage, remote access to car devices. As server we will use raspberry pi or some compact like nettop. 

Tasks are: 
----------
1. Processing information from a video recorder.
2. Streaming video to the Internet
3. Remote start engine
4. Geting location
5. Controlling devices of the car by voice commands
6. Controlling fuel consumption and mark up it on the map
7. Wi-fi voice connection between two twined cars (in case of joint travel)
8. Music and video center with possibility of separation for each passenger
9. Control of barriers and gates


Links:
----------
OBD2:
 1. http://www.stuffaboutcode.com/2013/07/raspberry-pi-reading-car-obd-ii-data.html
 2. https://github.com/martinohanlon/pyobd


Installing:
 1. sudo apt-get install streamer vlc
 2. ./manage.py syncdb
 3. ./manage.py loaddata obd_sensors

Starting:
 1. ./manage.py supervisor
 2. vlc -I http --http-password 123


----
Dev notes:
 ./manage.py dumpdata obd.Sensor --indent=4 > obd/fixtures/obd_sensors.json
