import requests
from dotmap import DotMap
from typing import List
from user_agent import generate_user_agent


class SauresAPI:
    def __init__(self, email: str = None, password: str = None):
        """Limitations: Accessing the server at a speed of more than 10 calls per minute

        :param email: username
        :param password: user password
        """

        self.sid = None #sid: session id (ID lifetime 15 minutes otherwise WrongSIDException in errors)
        self.email = email
        self.password = password
        self.api_url = u"https://api.saures.ru/1.0/"
        self.headers = {'User-Agent': generate_user_agent()}

    def login(self) -> DotMap:
        """User authorization in the system

        :return: {"data": {}|[], "errors": [], "status": "ok|bad"}
        :rtype: <class 'dotmap.DotMap'>
        """

        url = self.api_url + u"login"
        body = {'email': self.email, 'password': self.password}
        data = requests.post(url, headers=self.headers, data=body)
        self.sid = data.json()['data']['sid']
        return DotMap(data.json())

    def user_profile(self) -> DotMap:
        """Account parameters

        :return: {"data": {}|[], "errors": [], "status": "ok|bad"}
        :rtype: <class 'dotmap.DotMap'>
        """

        url = self.api_url + f"user/profile?sid={self.sid}"
        data = requests.get(url, headers=self.headers)
        return DotMap(data.json())

    def user_profile_edit(self, firstname: str, lastname: str, phone: str) -> DotMap:
        """Change account settings

        :param firstname: first name
        :param lastname: surname & patronymic
        :param phone: phone number (+7XXXXXXXXXX|+7 (XXX) XXX-XX-XX)
        :return: {"data": {}|[], "errors": [], "status": "ok|bad"}
        :rtype: <class 'dotmap.DotMap'>
        """

        url = self.api_url + u"user/profile"
        body = {'sid': self.sid, 'email': self.email, 'firstname': firstname,
                'lastname': lastname, 'phone': phone, 'password': self.password}
        data = requests.post(url, headers=self.headers, data=body)
        return DotMap(data.json())

    def user_objects(self) -> DotMap:
        """User objects

        :return: {"data": {}|[], "errors": [], "status": "ok|bad"}
        :rtype: <class 'dotmap.DotMap'>
        """

        url = self.api_url + f"user/objects?sid={self.sid}"
        data = requests.get(url, headers=self.headers)
        return DotMap(data.json())

    def object_meters(self, id: int, date: str = None) -> DotMap:
        """Object indications

        :param id: object id
        :param date: (optional) datetime for which you want to return the meters data (ISO 8610 - YYYY-MM-DDThh:mm:ss)
        :return: {'data': {'sensors': []}, 'errors': [], 'status': 'ok'}
        :rtype: <class 'dotmap.DotMap'>
        """

        url = self.api_url + f"object/meters?sid={self.sid}&id={id}"
        if date:
            url += f"&date={date}"

        data = requests.get(url, headers=self.headers)
        return DotMap(data.json())

    def meter_get(self, id: int, start: str, finish: str, group: str, absolute: bool = False) -> DotMap:
        """Device indications

        :param id: object id
        :param start: start datetime (ISO 8610 - YYYY-MM-DDThh:mm:ss)
        :param finish: end datetime (ISO 8610 - YYYY-MM-DDThh:mm:ss)
        :param group: data grouping (hour|day|month)
        :param absolute: flow rate (false, default) or absolute value (true)
        :return: {"data": {}|[], "errors": [], "status": "ok|bad"}
        :rtype: <class 'dotmap.DotMap'>
        """

        url = self.api_url + f"meter/get?sid={self.sid}&id={id}&start={start}&" \
                             f"finish={finish}&group={group}&absolute={absolute}"
        data = requests.get(url, headers=self.headers)
        return DotMap(data.json())

    def meter_control(self, id: int, command: str) -> DotMap:
        """Crane and relay control

        :param id: object id
        :param command: activate / deactivate device (activate|deactivate)
        :return: {"data": {}|[], "errors": [], "status": "ok|bad"}
        :rtype: <class 'dotmap.DotMap'>
        """

        url = self.api_url + u"meter/control"
        body = {'sid': self.sid, 'id': id, 'command': command}
        data = requests.post(url, headers=self.headers, data=body)
        return DotMap(data.json())

    def meter_types(self) -> DotMap:
        """Types of devices in the system

        :return: {"data": {}|[], "errors": [], "status": "ok|bad"}
        :rtype: <class 'dotmap.DotMap'>
        """

        url = self.api_url + f"meter/types?sid={self.sid}"
        data = requests.get(url, headers=self.headers)
        return DotMap(data.json())

    def user_register(self, phone: str, firstname: str = None, lastname: str = None) -> DotMap:
        """New user Registration

        :param phone: phone number (+7XXXXXXXXXX|+7 (XXX) XXX-XX-XX)
        :param firstname: (optional) first name
        :param lastname: (optional) surname & patronymic
        :return: {"data": {}|[], "errors": [], "status": "ok|bad"}
        :rtype: <class 'dotmap.DotMap'>
        """

        url = self.api_url + u"user/register"
        body = {'email': self.email, 'password': self.password, 'phone': phone}
        optional = {'firstname': firstname, 'lastname': lastname}

        optional = {k: v for k, v in optional.items() if v is not None}
        body.update(optional)

        data = requests.post(url, headers=self.headers, data=body)
        return DotMap(data.json())

    def object_add(self, city: str, street: str, building: str, utc: int, number: str = None,
                   type: int = None, install_inn: int = None, management_inn: int = None, personal_account: str = None,
                   account_id: str = None) -> DotMap:
        """Adding an object

        :param city: city
        :param street:  street
        :param building: house number
        :param utc: timezone (-12...12)
        :param number: (optional) object number / name
        :param type: (optional) object type (0...22): 0 - Empty, 1 - Apartment, 2 - Cottage, 3 - Town house, 4 - Land plot, 5 - Office,
                    6 - Premises, 7 - Room, 8 - Warehouse, 9 - Garage, 10 - Server, 11 - Shield, 12 - Boiler room,
                    13 - Aquarium, 14 - Refrigerator, 15 - Nursery, 16 - Section, 17 - Sector, 18 - Store, 19 - Cafe,
                    20 - Restaurant, 21 - Factory, 22 - House
        :param install_inn: (optional) TIN of the installation company
        :param management_inn: (optional) TIN of the management company
        :param personal_account: (optional) personal account in the management company
        :param account_id: (optional) installation company ID
        :return: {"data": {}|[], "errors": [], "status": "ok|bad"}
        :rtype: <class 'dotmap.DotMap'>
        """

        url = self.api_url + u"object/add"
        body = {'sid': self.sid, 'city': city, 'street': street, 'building': building, 'utc': utc}
        optional = {'type': type, 'number': number, 'install_inn': install_inn, 'management_inn': management_inn,
                    'personal_account': personal_account, 'account_id': account_id}

        optional = {k: v for k, v in optional.items() if v is not None}
        body.update(optional)

        data = requests.post(url, headers=self.headers, data=body)
        return DotMap(data.json())

    def sensor_add_first_step(self, sn: str) -> DotMap:
        """Adding a controller to an object. The addition takes place in 2 stages:
        Step 1. Request for unbound controller inputs using the GET method

        :param sn: controller serial number
        :return: {"data": {}|[], "errors": [], "status": "ok|bad"}
        :rtype: <class 'dotmap.DotMap'>
        """

        url = self.api_url + f"sensor/add?sid={self.sid}&sn={sn}"
        data = requests.get(url, headers=self.headers)
        return DotMap(data.json())

    def sensor_add_second_step(self, sn: str, object_id: int, devices: List[dict]) -> DotMap:
        """Adding a controller to an object. The addition takes place in 2 stages:
        Step 2. Binding the received inputs using the POST method

        :param sn: controller serial number
        :param object_id: object id
        :param devices: device list [{'entrance_number': 1, 'name': "Hot water meter (HWM)", 'sn': "20-084125"},
                                    {'entrance_number': 2, 'name': "Cold water meter (CWM)", 'sn': "20-049331"}]
        :return: {"data": {}|[], "errors": [], "status": "ok|bad"}
        :rtype: <class 'dotmap.DotMap'>
        """

        url = self.api_url + u"sensor/add"
        body = {'sid': self.sid, 'sn': sn, 'object_id': object_id}

        for device in devices:
            device_number = device["entrance_number"]
            device_name = device["name"]
            device_sn = device["sn"]

            body[f"{device_number}_name"] = device_name
            body[f"{device_number}_sn"] = device_sn

        data = requests.post(url, headers=self.headers, data=body)
        return DotMap(data.json())

    def sensor_settings(self, sn: str, name: str, check_hours: int = None, new_firmware: str = None) -> DotMap:
        """Editing a controller

        :param sn: controller serial number
        :param name: controller name
        :param check_hours: (optional) (72, default) check period notify if there is no connection for more than
        :param new_firmware: (optional) new firmware version for the controller or empty to cancel the update
        :return: {"data": {}|[], "errors": [], "status": "ok|bad"}
        :rtype: <class 'dotmap.DotMap'>
        """

        url = self.api_url + u"sensor/settings"
        body = {'sid': self.sid, 'sn': sn, 'name': name}
        optional = {'check_hours': check_hours, 'new_firmware': new_firmware}

        optional = {k: v for k, v in optional.items() if v is not None}
        body.update(optional)

        data = requests.post(url, headers=self.headers, data=body)
        return DotMap(data.json())

    def meter_save(self, id: int, name: str, sn: str, approve_dt: str, eirc_num: str = None) -> DotMap:
        """Editing a device

        :param id: device id
        :param name: device name
        :param sn: serial number
        :param approve_dt: datetime of the next verification / replacement / service (ISO 8610 - YYYY-MM-DDThh:mm:ss)
        :param eirc_num: (optional) counter identifier in EIRTS (see https://www.saures.ru/kb/article-3914/)
        :return: {"data": {}|[], "errors": [], "status": "ok|bad"}
        :rtype: <class 'dotmap.DotMap'>
        """

        url = self.api_url + u"meter/save"
        body = {'sid': self.sid, 'id': id, 'name': name, 'sn': sn, 'approve_dt': approve_dt}

        if eirc_num:
            body["eirc_num"] = eirc_num

        data = requests.post(url, headers=self.headers, data=body)
        return DotMap(data.json())

    def object_journal(self, id: int, page: int, step: int) -> DotMap:
        """Object log

        :param id: object id
        :param page: page number
        :param step: number of records in the response
        :return: {"data": {}|[], "errors": [], "status": "ok|bad"}
        :rtype: <class 'dotmap.DotMap'>
        """

        url = self.api_url + f"object/journal?sid={self.sid}&id={id}&page={page}&step={step}"
        data = requests.get(url, headers=self.headers)
        return DotMap(data.json())

    def object_payments(self, id: int, page: int, step: int) -> DotMap:
        """Payment transactions

        :param id: object id
        :param page: page number
        :param step: number of records in the response
        :return: {"data": {}|[], "errors": [], "status": "ok|bad"}
        :rtype: <class 'dotmap.DotMap'>
        """

        url = self.api_url + f"object/payments?sid={self.sid}&id={id}&page={page}&step={step}"
        data = requests.get(url, headers=self.headers)
        return DotMap(data.json())

    def object_schedule(self, id: int) -> DotMap:
        """Schedules

        :param id: object id
        :return: {"data": {}|[], "errors": [], "status": "ok|bad"}
        :rtype: <class 'dotmap.DotMap'>
        """

        url = self.api_url + f"object/schedule?sid={self.sid}&id={id}"
        data = requests.get(url, headers=self.headers)
        return DotMap(data.json())

    def object_schedule_setup(self, type: str, day: int, time: str, personal_account: str,
                              fraction: bool, receiver: int, resource: int, object_id: int,
                              id: int = None, signature: str = None, delete: int = None) -> DotMap:
        """Schedule setup

        :param type: dispatch type (email|push|sms|telegram|mos_ru|mosobleirc)
        :param day: 0 - every day or 32 - the last day of the month (0...32)
        :param time: time (00:00...23:59)
        :param personal_account: personal account for mos_ru and mosobleirc
        :param fraction: transmission of indications with fractional part (0|1)
        :param receiver: schedule recipient (email|login|phone):
                        - phone in the format +7XXXXXXXXXX for sms
                        - username for push and telegram
                        - email address for email
        :param resource: types of resources to be sent (each type of resource should be sent in a separate field)
        :param object_id: id of the object in which you want to create a schedule (used only when creating)
        :param id: (optional) schedule id (used only when editing)
        :param signature: (optional) message signature
        :param delete: (optional) id of the schedule to be deleted
        :return: {"data": {}|[], "errors": [], "status": "ok|bad"}
        :rtype: <class 'dotmap.DotMap'>
        """

        url = self.api_url + u"object/schedule"
        body = {'sid': self.sid, 'type': type, 'day': day, 'time': time, 'personal_account': personal_account,
                'fraction': fraction, 'receiver': receiver, 'resource': resource, 'object_id': object_id}
        optional = {'id': id, 'signature': signature, 'delete': delete}

        optional = {k: v for k, v in optional.items() if v is not None}
        body.update(optional)

        data = requests.post(url, headers=self.headers, data=body)
        return DotMap(data.json())

    def object_notice(self, id: int) -> DotMap:
        """Notifications

        :param id: object id
        :return: {"data": {}|[], "errors": [], "status": "ok|bad"}
        :rtype: <class 'dotmap.DotMap'>
        """

        url = self.api_url + f"object/notice?sid={self.sid}&id={id}"
        data = requests.get(url, headers=self.headers)
        return DotMap(data.json())

    def object_notice_setup(self, type: str, dispatch: str, receiver: str,
                            id: int = None, object_id: int = None, delete: int = None) -> DotMap:
        """Configuring notifications

        :param type: type of notification (notification|error|notice+error)
        :param dispatch: dispatch type (email|push|sms|telegram)
        :param receiver: recipient of notification (email|login|phone):
                        - phone in the format +7XXXXXXXXXX for sms
                        - username for push and telegram
                        - email address for email
        :param id: (optional) id of the notification (used only when editing)
        :param object_id: (optional) id of the object in which the notification should be created (used only when creating)
        :param delete: (optional) id of the notification to be deleted
        :return: {"data": {}|[], "errors": [], "status": "ok|bad"}
        :rtype: <class 'dotmap.DotMap'>
        """

        url = self.api_url + u"object/notice"
        body = {'sid': self.sid, 'type': type, 'dispatch': dispatch, 'receiver': receiver}
        optional = {'id': id, 'object_id': object_id, 'delete': delete}

        optional = {k: v for k, v in optional.items() if v is not None}
        body.update(optional)

        data = requests.post(url, headers=self.headers, data=body)
        return DotMap(data.json())
