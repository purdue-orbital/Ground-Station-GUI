# Logging format
Structure and an example of the logging function output. This will be stored in logs/status_log.txt
## Structure
```
  --------ACTION TAKEN---------
  DATE:20xx-xx-xx hh:mm:ss
  TIMESTAMP:'hh:mm:ss:ms'
  *****************************
  ----------LOGS START---------
  temperature = deg C
  pressure = kPA
  humidity = Percent
  altitude = ft
  direction = rad
  acceleration = m/s/s
  velocity = m/s
  ----------LOGS END-----------
  -----------------------------
```
## Example
```
  -------PROGRAM RESTART-------
  DATE:2018-12-16 16:23:33
  TIMESTAMP:'00:00:00:00'
  *****************************
  ----------LOGS START---------
  temperature = 15000.0
  pressure = 6000.0
  humidity = 100.0
  altitude = 15000000
  direction = 0.1234
  acceleration = 90
  velocity = 12
  ----------LOGS END-----------
  -----------------------------
```
