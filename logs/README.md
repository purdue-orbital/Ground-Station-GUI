# Logging format
Structure and an example of the logging function output. This will be stored in `logs/status.log`
## Structure
```
  --------ACTION TAKEN---------
  DATE:20xx-xx-xx hh:mm:ss
  MISSION START TIMESTAMP: 'hh:mm:ss:ms'
  LAUNCH START TIMESTAMP: 'hh:mm:ss:ms'
  *****************************
  ----------LOGS START---------
  ----------BALLOON DATA-------
  Longitude = longitude in degrees
  Latitude = latitude in degrees
  Gyro(X) = degrees/sec
  Gyro(Y) = degrees/sec
  Gyro(Z) = degrees/sec
  Temperature = temperature in celsius
  Acceleration(X) = m/s/s
  Acceleration(Y) = m/s/s
  Acceleration(Z) = m/s/s
  ----------LOGS END-----------
  -----------------------------
```
## Example
```
  -------PROGRAM RESTART-------
  DATE:2018-12-16 16:23:33
  MISSION START TIMESTAMP:'01:10:24:31'
  LAUNCH START TIMESTAMP:'01:10:53:09'
  *****************************
  ----------LOGS START---------
  Longitude = -86.913
  Latitude = 40.419
  Gyro(X) = .008
  Gyro(Y) = .012
  Gyro(Z) = .109
  Temperature = 8.183
  Acceleration(X) = .010
  Acceleration(Y) = .012
  Acceleration(Z) = .992
  ----------LOGS END-----------
  -----------------------------
```
