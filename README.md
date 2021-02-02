### pysaures - Saures API for Python

``` python
from saures_api import SauresAPI
from datetime import datetime

api = SauresAPI(email='login@email.com', password='password')

register = api.user_register(phone='+79998887766', firstname='Name', lastname='Surname')
print(register.status) #ok

login = api.login()
sid = login.data.sid #2eb74868-49fc-464b-accf-200e23c59cc1

object_add = api.object_add(sid=sid, city='Moscow', street='Sadovaya', building='75', utc=3)
object_id = object_add.data.id #11753

controller_add = api.sensor_add_first_step(sid=sid, sn='CC50E3FFFFFF')
print(controller_add.status) #ok

meters = [{'entrance_number': 1, 'name': 'Hot water meter (HWM)', 'sn': '20-085432'},
          {'entrance_number': 2, 'name': 'Cold water meter (CWM)', 'sn': '20-049876'}]
meters_add = api.sensor_add_second_step(sid=sid, sn='CC50E3FFFFFF', object_id=object_id, devices=meters)
print(meters_add.status) #ok

firmware_update = api.sensor_settings(sid=sid, sn='CC50E3FFFFFF', name='Home controller', new_firmware='4.4.1')
print(firmware_update.status) #ok

date_now = datetime.now().replace(microsecond=0).isoformat() #YYYY-MM-DDThh:mm:ss
meters_data = api.object_meters(sid=sid, id=11901, date=date_now)

hot_meter_value = meters_data.data.sensors[0].meters[0].vals[0] #0.05
cold_meter_value = meters_data.data.sensors[0].meters[1].vals[0] #0.07

if meters_data.status == "bad":
    for error in meters_data.errors:
        print(f"name: {error.name}, msg: {error.msg}") #name: WrongSIDException, msg: Неверный sid

```
