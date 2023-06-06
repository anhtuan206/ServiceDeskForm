import mysql.connector
from mysql.connector import errorcode
from datetime import datetime


class FirewallRule:
    def __init__(
        self, database="netsecops", host="10.72.28.249", user="python", password=""
    ):
        self.database = database
        self.host = host
        self.user = user
        self.password = password
        self.dbconnect = None

    def connect(self):
        try:
            self.dbconnect = mysql.connector.connect(
                database=self.database,
                host=self.host,
                user=self.user,
                password=self.password,
            )
        except mysql.connector.Error as err:
            message = {"code": 0, "data": err.msg}
            return message

    def execute_query(self, query, data=None, dictionary=False):
        try:
            cursor = self.dbconnect.cursor(dictionary=dictionary)
            cursor.execute(query, data)
            result = cursor.fetchall()
            cursor.close()
            return result
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "data": err.msg}
            return message

    def disconnect(self):
        self.dbconnect.close()

    # Lấy các yêu cầu tạo firewall từ db
    def get_servicedesk_firewall_request(self):
        try:
            self.connect()
            query = f"SELECT * FROM servicedeskrequests WHERE request_template LIKE 'firewall'"
            result = self.execute_query(query=query, dictionary=True)
            self.disconnect()
            return result
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "data": err.msg}
            return message

    # Lấy requestid của các yêu càu tạo firewall từ db
    def get_servicedesk_request_id_list(self):
        try:
            self.connect()
            query = f"SELECT requestid FROM servicedeskrequests WHERE request_template LIKE 'firewall'"
            result = self.execute_query(query=query, dictionary=True)
            self.disconnect()
            return result
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "data": err.msg}
            return message

    # Lấy yêu cầu tạo firewall từ db theo requestid
    def get_servicedesk_firewall(self, requestid):
        try:
            self.connect()
            query = f"SELECT * FROM servicedeskrequests WHERE request_template LIKE 'firewall' AND requestid LIKE {requestid}"
            result = self.execute_query(query=query, dictionary=True)
            self.disconnect()
            message = {"code": 1, "data": result}
            return message
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "data": err.msg}
            return message

    # Lấy thông tin rule mà người dùng request
    def get_firewall_user_submit_rule(self, requestid=None, ruleid=None):
        try:
            self.connect()
            query = "SELECT id,name,description FROM firewall_user_submit_rule"
            if requestid:
                query = f"SELECT id,name,description,approved FROM firewall_user_submit_rule WHERE requestid LIKE '{requestid}'"
            if requestid and ruleid:
                query = f"SELECT id,name,description,approved FROM firewall_user_submit_rule WHERE requestid LIKE '{requestid}' AND id = '{ruleid}'"
            result = self.execute_query(query=query, dictionary=True)
            if len(result) > 0:
                for rule in result:
                    rule["source"] = self.get_firewall_user_submit_object(
                        data_type="source", ruleid=rule["id"]
                    )
                    rule["destination"] = self.get_firewall_user_submit_object(
                        data_type="destination", ruleid=rule["id"]
                    )
                    rule["service"] = self.get_firewall_user_submit_object(
                        data_type="service", ruleid=rule["id"]
                    )
            self.disconnect()
            message = {"code": 1, "data": result}
            return message
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "data": err.msg}
            return message

    # Lấy thông tin các object mà người dùng request theo điều kiện đầu vào
    def get_firewall_user_submit_object(self, data_type, ruleid):
        try:
            self.connect()
            query = f"SELECT * FROM firewall_user_submit_{data_type}"
            if ruleid:
                query = f"SELECT * FROM firewall_user_submit_{data_type} WHERE ruleid={ruleid}"
            result = self.execute_query(query=query, dictionary=True)
            self.disconnect()
            return result
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "error": err.msg}
            return message

    # Insert rule vào database
    def insert_firewall_user_submit_rule(self, data):
        try:
            self.connect()
            query = "INSERT INTO firewall_user_submit_rule(name,description,requestid,approved) VALUE (%s, %s, %s, %s)"
            insertdata = (data["name"], data["description"], data["requestid"], False)
            cursor = self.dbconnect.cursor()
            cursor.execute(query, insertdata)
            self.dbconnect.commit()
            ruleid = cursor.lastrowid
            self.disconnect()
            for item in data["source"]:
                self.insert_firewall_user_submit_object(
                    data_type="source", data={"ruleid": ruleid, "object": item}
                )
            for item in data["destination"]:
                self.insert_firewall_user_submit_object(
                    data_type="destination", data={"ruleid": ruleid, "object": item}
                )
            for item in data["service"]:
                self.insert_firewall_user_submit_object(
                    data_type="service",
                    data={
                        "ruleid": ruleid,
                        "protocol": item["protocol"],
                        "port": item["port"],
                    },
                )
            return True
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "error": err.msg}
            return message

    # Insert object dữ liệu vào database
    def insert_firewall_user_submit_object(self, data, data_type):
        try:
            self.connect()
            query = None
            insertdata = None
            if data_type == "source" or data_type == "destination":
                query = f"INSERT INTO firewall_user_submit_{data_type}(ruleid,{data_type}) VALUE (%s, %s)"
                insertdata = (data["ruleid"], data["object"])
            if data_type == "service":
                query = f"INSERT INTO firewall_user_submit_{data_type}(ruleid,protocol,port) VALUE (%s, %s, %s)"
                insertdata = (data["ruleid"], data["protocol"], data["port"])
            if query is not None and insertdata is not None:
                cursor = self.dbconnect.cursor()
                cursor.execute(query, insertdata)
                self.dbconnect.commit()
                self.disconnect()
            return True
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "error": err.msg}
            return message

    # Xóa một rule
    def remove_user_submit_rule(self, requestid, ruleid):
        try:
            self.connect()
            query = f"DELETE FROM firewall_user_submit_rule WHERE id = {ruleid} AND requestid LIKE '{requestid}'"
            cursor = self.dbconnect.cursor()
            cursor.execute(query)
            self.dbconnect.commit()
            self.disconnect()
            return {"code": 1, "message": "Success"}
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "error": err.msg}
            return message

    # Xóa một object
    def remove_firewall_user_submit_object(self, ruleid, objectid, data_type):
        try:
            self.connect()
            query = f"DELETE FROM firewall_user_submit_{data_type} WHERE id = {objectid} AND ruleid LIKE '{ruleid}'"
            cursor = self.dbconnect.cursor()
            cursor.execute(query)
            self.dbconnect.commit()
            self.disconnect()
            return True
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "error": err.msg}
            return message

    # Cập nhật dữ liệu object
    def update_firewall_user_submit_object(self, ruleid, objectid, datatype, value):
        if datatype not in ["sources", "destinations", "services"]:
            return {"code": 0, "error": "Kiểu dữ liệu datatype không hợp lệ"}
        try:
            if datatype == "sources":
                query = f"UPDATE firewall_user_submit_source SET source = '{value}' WHERE id = {objectid} AND ruleid = {ruleid}"
            if datatype == "destinations":
                query = f"UPDATE firewall_user_submit_destination SET destination = '{value}' WHERE id = {objectid} AND ruleid = {ruleid}"
            if datatype == "services":
                query = f"UPDATE firewall_user_submit_service SET port = {value} WHERE id = {objectid} AND ruleid = {ruleid}"
            self.connect()
            cursor = self.dbconnect.cursor()
            cursor.execute(query)
            self.dbconnect.commit()
            self.disconnect()
            return True
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "error": err.msg}
            return message

    # Cập nhật dữ liệu rule
    def update_firewall_user_submit_rule(self, ruleid, name, description):
        try:
            self.connect()
            query = f"UPDATE firewall_user_submit_rule SET name = '{name}',description='{description}' WHERE id = '{ruleid}'"
            cursor = self.dbconnect.cursor()
            cursor.execute(query)
            self.dbconnect.commit()
            self.disconnect()
            return True
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "error": err.msg}
            return message
    # Tạo dữ liệu mới cho bảng servicedeskrequests
    def insert_firewall_servicedeskrequest(
        self,
        requestid,
        requester = None,
        subject = None,
        requestdate = None,
        request_template = "firewall",
        request_description = None

    ):
        try:
            dataset = {}
            dataset["requestid"] = requestid
            dataset["requester"] = requester
            dataset["subject"] = subject
            dataset["requestdate"] = requestdate
            dataset["request_template"] = request_template
            dataset["request_description"] = request_description

            query = f"INSERT INTO servicedeskrequests "

            columns = ", ".join(dataset.keys())
            query += f"({columns}) "
            values = "', '".join(map(str, dataset.values()))
            query += f"VALUES ('{values}')"

            self.connect()
            cursor = self.dbconnect.cursor()
            cursor.execute(query)
            self.dbconnect.commit()
            self.disconnect()
            return True
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "error": err.msg}
            return message

    # ===KHÔNG SỬ DỤNG===
    # Lấy dữ liệu về danh sách thiết bị - Không sử dụng ở đây
    def get_devices(self):
        try:
            self.connect()
            query = f"SELECT * FROM devices"
            result = self.execute_query(query=query, dictionary=True)
            self.disconnect()
            message = {"code": 1, "data": result}
            return message
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "data": err.msg}
            return message

    # Lấy dữ liệu về danh sách thiết bị - Không sử dụng ở đây
    def get_device(self, deviceid):
        try:
            self.connect()
            query = f"SELECT * FROM devices WHERE deviceid LIKE '{deviceid}'"
            result = self.execute_query(query=query, dictionary=True)
            self.disconnect()
            message = {"code": 1, "data": result}
            return message
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "data": err.msg}
            return message

    # Lấy thông tin tài khoản đăng nhập thiết bị - Không sử dụng ở đây
    def get_device_credential(self, deviceid, cred_type, cred_permission):
        try:
            self.connect()
            query = f"SELECT * FROM device_credentials WHERE deviceid LIKE '{deviceid}' AND type LIKE '{cred_type}' AND readwrite = {cred_permission}"
            result = self.execute_query(query=query, dictionary=True)
            self.disconnect()
            message = {"code": 1, "data": result}
            return message
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "data": err.msg}
            return message

    # Cập nhật thông tin published session vào database - Không sử dụng
    def insert_published_session(
        self, uid, name, type, state, publish_time, application, deviceid
    ):
        try:
            self.connect()
            query = "INSERT INTO firewall_published_session (uid, name, type, state, publish_time, application, deviceid) VALUE (%s, %s, %s, %s, %s, %s, %s)"
            insertdata = (uid, name, type, state, publish_time, application, deviceid)
            cursor = self.dbconnect.cursor()
            cursor.execute(query, insertdata)
            self.dbconnect.commit()
            self.disconnect()
            return True
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "error": err.msg}
            return message

    def get_published_session(self, deviceid):
        try:
            self.connect()
            query = f"SELECT * FROM firewall_published_session WHERE deviceid LIKE '{deviceid}'"
            result = self.execute_query(query=query, dictionary=True)
            self.disconnect()
            message = {"code": 1, "data": result}
            return message
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "data": err.msg}
            return message

    def update_published_session(
        self, uid, name, type, state, publish_time, application, deviceid
    ):
        # Kiểm tra nếu có exist record thì xóa
        result = self.get_published_session(deviceid=deviceid)
        if result:
            if result["code"] == 1 and len(result["data"]) > 0:
                remove_exist_sesion = self.remove_published_session(deviceid=deviceid)
                if remove_exist_sesion is True:
                    # Thêm mới record
                    return self.insert_published_session(
                        uid, name, type, state, publish_time, application, deviceid
                    )
                else:
                    return remove_exist_sesion
            if result["code"] == 1 and len(result["data"]) < 1:
                return self.insert_published_session(
                    uid, name, type, state, publish_time, application, deviceid
                )
        return result

    def remove_published_session(self, deviceid):
        try:
            self.connect()
            query = f"DELETE FROM firewall_published_session WHERE deviceid LIKE '{deviceid}'"
            cursor = self.dbconnect.cursor()
            cursor.execute(query)
            self.dbconnect.commit()
            self.disconnect()
            return True
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "error": err.msg}
            return message

    # ===KHÔNG SỬ DỤNG===

class Firewall:
    def __init__(
        self, database="netsecops", host="10.72.28.249", user="python", password=""
    ):
        self.database = database
        self.host = host
        self.user = user
        self.password = password
        self.dbconnect = None

    def connect(self):
        try:
            self.dbconnect = mysql.connector.connect(
                database=self.database,
                host=self.host,
                user=self.user,
                password=self.password,
            )
        except mysql.connector.Error as err:
            message = {"code": 0, "data": err.msg}
            return message

    def execute_query(self, query, data=None, dictionary=True):
        try:
            cursor = self.dbconnect.cursor(dictionary=dictionary)
            cursor.execute(query, data)
            result = cursor.fetchall()
            cursor.close()
            return result
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "data": err.msg}
            return message

    def disconnect(self):
        self.dbconnect.close()
    # Lấy thông tin từ bảng servicedeskrequests
    def get_servicedesk_firewall_request(self, requestid=None):
        try:
            query = f"SELECT * FROM servicedeskrequests"
            conditions = []
            if requestid is not None:
                conditions.append(f"requestid LIKE '{requestid}'")
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            self.connect()
            result = self.execute_query(query=query, dictionary=True)
            self.disconnect()
            message = {"code": 1, "data": result}
            return message
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "data": err.msg}
            return message

class Citrix:
    def __init__(
        self, database="netsecops", host="10.72.28.249", user="python", password=""
    ):
        self.database = database
        self.host = host
        self.user = user
        self.password = password
        self.dbconnect = None

    def connect(self):
        try:
            self.dbconnect = mysql.connector.connect(
                database=self.database,
                host=self.host,
                user=self.user,
                password=self.password,
            )
        except mysql.connector.Error as err:
            message = {"code": 0, "message": err}
            return message

    def execute_query(self, query, data=None, dictionary=False):
        try:
            cursor = self.dbconnect.cursor(dictionary=dictionary)
            cursor.execute(query, data)
            result = cursor.fetchall()
            cursor.close()
            return result
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "message": err}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "message": err}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "message": err}
            return message

    def disconnect(self):
        self.dbconnect.close()

    # Lấy thông tin từ bảng citrix_user_submit_lb
    def get_citrix_lb(self, requestid=None, vip=None):
        try:
            query = f"SELECT * FROM citrix_user_submit_lb"
            conditions = []
            if requestid is not None:
                conditions.append(f"requestid LIKE '{requestid}'")
            if vip is not None:
                conditions.append(f"vip LIKE '{vip}'")

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            self.connect()
            result = self.execute_query(query=query, dictionary=True)
            self.disconnect()
            message = {"code": 1, "data": result}
            return message
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "data": err.msg}
            return message

    # Lấy thông tin từ 3 bảng citrix_user_submit_lb, citrix_user_submit_server, citrix_user_submit_service
    def get_servicedesk_request_info_all_by_requestid(self, requestid):
        try:
            query = f"SELECT * FROM citrix_user_submit_lb lb INNER JOIN citrix_user_submit_server as srv ON lb.lbid = srv.lbid INNER JOIN citrix_user_submit_service svc ON svc.lbid = lb.lbid WHERE lb.requestid LIKE '{requestid}'"
            self.connect()
            result = self.execute_query(query=query, dictionary=True)
            self.disconnect()
            message = {"code": 1, "data": result}
            return message
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "data": err.msg}
            return message

    # Lấy thông tin từ bảng servicedeskrequests
    def get_servicedesk_citrix_request(self, requestid=None):
        try:
            query = f"SELECT * FROM servicedeskrequests"
            conditions = []
            if requestid is not None:
                conditions.append(f"requestid LIKE '{requestid}'")
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            self.connect()
            result = self.execute_query(query=query, dictionary=True)
            self.disconnect()
            message = {"code": 1, "data": result}
            return message
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "data": err.msg}
            return message

    # Lấy thông tin từ bảng citrix_user_submit_server
    def get_citrix_servers(self, requestid=None, serverid=None, lbid=None):
        try:
            query = f"SELECT * FROM citrix_user_submit_server"
            conditions = []
            if requestid is not None:
                conditions.append(f"requestid LIKE '{requestid}'")
            if serverid is not None:
                conditions.append(f"serverid = {serverid}")
            if lbid is not None:
                conditions.append(f"lbid = {lbid}")
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            self.connect()
            result = self.execute_query(query=query, dictionary=True)
            self.disconnect()
            message = {"code": 1, "data": result}
            return message
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "data": err.msg}
            return message

    # Lấy thông tin từ bảng citrix_user_submit_service
    def get_citrix_services(self, requestid=None, serviceid=None, lbid=None):
        try:
            query = f"SELECT * FROM citrix_user_submit_service"
            conditions = []
            if requestid is not None:
                conditions.append(f"requestid LIKE '{requestid}'")
            if serviceid is not None:
                conditions.append(f"serviceid = {serviceid}")
            if lbid is not None:
                conditions.append(f"lbid = {lbid}")
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            self.connect()
            result = self.execute_query(query=query, dictionary=True)
            self.disconnect()
            message = {"code": 1, "data": result}
            return message
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "data": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "data": err.msg}
            return message

    # Cập nhật dữ liệu cho bảng citrix_user_submit_lb
    def update_citrix_lb(
        self, lbid, requestid=None, vip=None, name=None, description=None
    ):
        try:
            dataset = {}
            if requestid is not None:
                dataset["requestid"] = requestid
            if vip is not None:
                dataset["vip"] = vip
            if name is not None:
                dataset["name"] = name
            if description is not None:
                dataset["description"] = description
            condition = f"lbid = {lbid}"
            query = f"UPDATE citrix_user_submit_lb SET "

            column_assignments = []
            for column, value in dataset.items():
                column_assignments.append(f"{column} = '{value}'")
            query += ", ".join(column_assignments)
            query += f" WHERE {condition}"
            self.connect()
            cursor = self.dbconnect.cursor()
            cursor.execute(query)
            self.dbconnect.commit()
            self.disconnect()
            return True
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "error": err.msg}
            return message

    # Cập nhật dữ liệu cho bảng citrix_user_submit_server
    def update_citrix_server(
        self,
        serverid,
        lbid=None,
        servername=None,
        serveripaddress=None,
        servercomment=None,
        serverstate=None,
        requestid=None,
        created=None,
        createdtime=None,
    ):
        try:
            dataset = {}
            if requestid is not None:
                dataset["requestid"] = requestid
            if servername is not None:
                dataset["servername"] = servername
            if serveripaddress is not None:
                dataset["serveripaddress"] = serveripaddress
            if servercomment is not None:
                dataset["servercomment"] = servercomment
            if serverstate is not None:
                dataset["serverstate"] = serverstate
            if requestid is not None:
                dataset["requestid"] = requestid
            if created is not None:
                dataset["created"] = created
            if createdtime is not None:
                dataset["createdtime"] = createdtime
            if lbid is not None:
                dataset["lbid"] = lbid

            condition = f"serverid = {serverid}"
            query = f"UPDATE citrix_user_submit_server SET "

            column_assignments = []
            for column, value in dataset.items():
                column_assignments.append(f"{column} = '{value}'")
            query += ", ".join(column_assignments)
            query += f" WHERE {condition}"
            self.connect()
            cursor = self.dbconnect.cursor()
            cursor.execute(query)
            self.dbconnect.commit()
            self.disconnect()
            return True
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "error": err.msg}
            return message

    # Cập nhật dữ liệu cho bảng citrix_user_submit_service
    def update_citrix_service(
        self,
        serviceid,
        lbid=None,
        servicename=None,
        servicetype=None,
        servicecomment=None,
        requestid=None,
        created=None,
        createdtime=None,
        serviceport=None,
    ):
        try:
            dataset = {}
            if requestid is not None:
                dataset["requestid"] = requestid
            if servicename is not None:
                dataset["servicename"] = servicename
            if servicetype is not None:
                dataset["servicetype"] = servicetype
            if servicecomment is not None:
                dataset["servicecomment"] = servicecomment
            if requestid is not None:
                dataset["requestid"] = requestid
            if created is not None:
                dataset["created"] = created
            if createdtime is not None:
                dataset["createdtime"] = createdtime
            if lbid is not None:
                dataset["lbid"] = lbid
            if serviceport is not None:
                dataset["serviceport"] = serviceport

            condition = f"serviceid = {serviceid}"
            query = f"UPDATE citrix_user_submit_service SET "

            column_assignments = []
            for column, value in dataset.items():
                column_assignments.append(f"{column} = '{value}'")
            query += ", ".join(column_assignments)
            query += f" WHERE {condition}"

            self.connect()
            cursor = self.dbconnect.cursor()
            cursor.execute(query)
            self.dbconnect.commit()
            self.disconnect()
            return True
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "error": err.msg}
            return message

    # Tạo dữ liệu mới cho bảng citrix_user_submit_lb
    def insert_citrix_lb(
        self, requestid, lbid=None, vip=None, name=None, description=None,lastrowid = False
    ):
        try:
            dataset = {}
            dataset["lbid"] = lbid
            dataset["requestid"] = requestid
            dataset["vip"] = vip
            dataset["name"] = name
            dataset["description"] = description

            query = f"INSERT INTO citrix_user_submit_lb  "

            columns = ", ".join(dataset.keys())
            query += f"({columns}) "
            values = "', '".join(map(str, dataset.values()))
            query += f"VALUES ('{values}')"

            self.connect()
            cursor = self.dbconnect.cursor()
            cursor.execute(query)
            self.dbconnect.commit()
            self.disconnect()
            if lastrowid is True:
                return cursor.lastrowid
            return True
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "error": err.msg}
            return message

    # Tạo dữ liệu mới cho bảng citrix_user_submit_server
    def insert_citrix_server(
        self,
        lbid,
        requestid,
        serveripaddress,
        serverid=None,
        servername=None,
        servercomment=None,
        serverstate=None,
        created=None,
        createdtime=None,
    ):
        try:
            dataset = {}
            dataset["serverid"] = serverid
            dataset["lbid"] = lbid
            dataset["requestid"] = requestid
            dataset["servername"] = servername
            dataset["serveripaddress"] = serveripaddress
            dataset["servercomment"] = servercomment
            dataset["serverstate"] = serverstate
            dataset["requestid"] = requestid
            dataset["created"] = created
            dataset["createdtime"] = createdtime

            query = f"INSERT INTO citrix_user_submit_server "

            columns = ", ".join(dataset.keys())
            query += f"({columns}) "
            values = "', '".join(map(str, dataset.values()))
            query += f"VALUES ('{values}')"

            self.connect()
            cursor = self.dbconnect.cursor()
            cursor.execute(query)
            self.dbconnect.commit()
            self.disconnect()
            return True
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "error": err.msg}
            return message

    # Tạo dữ liệu mới cho bảng citrix_user_submit_service
    def insert_citrix_service(
        self,
        lbid,
        serviceport,
        servicetype,
        serviceid=None,
        servicename=None,
        servicecomment=None,
        requestid=None,
        created=None,
        createdtime=None,
    ):
        try:
            dataset = {}
            dataset["serviceid"] = serviceid
            dataset["requestid"] = requestid
            dataset["servicename"] = servicename
            dataset["servicetype"] = servicetype
            dataset["servicecomment"] = servicecomment
            dataset["requestid"] = requestid
            dataset["created"] = created
            dataset["createdtime"] = createdtime
            dataset["lbid"] = lbid
            dataset["serviceport"] = serviceport

            query = f"INSERT INTO citrix_user_submit_service "

            columns = ", ".join(dataset.keys())
            query += f"({columns}) "
            values = "', '".join(map(str, dataset.values()))
            query += f"VALUES ('{values}')"

            self.connect()
            cursor = self.dbconnect.cursor()
            cursor.execute(query)
            self.dbconnect.commit()
            self.disconnect()
            return True
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "error": err.msg}
            return message
    # Tạo dữ liệu mới cho bảng servicedeskrequests
    def insert_citrix_servicedeskrequest(
        self,
        requestid,
        requester = None,
        subject = None,
        requestdate = None,
        request_template = "citrix",
        request_description = None

    ):
        try:
            dataset = {}
            dataset["requestid"] = requestid
            dataset["requester"] = requester
            dataset["subject"] = subject
            dataset["requestdate"] = requestdate
            dataset["request_template"] = request_template
            dataset["request_description"] = request_description

            query = f"INSERT INTO servicedeskrequests "

            columns = ", ".join(dataset.keys())
            query += f"({columns}) "
            values = "', '".join(map(str, dataset.values()))
            query += f"VALUES ('{values}')"

            self.connect()
            cursor = self.dbconnect.cursor()
            cursor.execute(query)
            self.dbconnect.commit()
            self.disconnect()
            return True
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "error": err.msg}
            return message

    # Xóa dữ liệu trong bảng citrix_user_submit_lb
    def delete_citrix_lb(self, lbid, requestid=None):
        try:
            conditions = []

            conditions.append(f"lbid = '{lbid}'")
            if requestid is not None:
                conditions.append(f"requestid = '{requestid}'")

            query = f"DELETE FROM citrix_user_submit_lb"

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            self.connect()
            cursor = self.dbconnect.cursor()
            cursor.execute(query)
            self.dbconnect.commit()
            self.disconnect()
            return True
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "error": err.msg}
            return message

    # Xóa dữ liệu trong bảng citrix_user_submit_lb
    # Xóa dữ liệu trong bảng user_submit_server
    def delete_citrix_server(self, serverid, requestid=None, lbid=None):
        try:
            conditions = []
            conditions.append(f"serverid = '{serverid}'")
            if lbid is not None:
                conditions.append(f"lbid = '{lbid}'")
            if requestid is not None:
                conditions.append(f"requestid = '{requestid}'")

            query = f"DELETE FROM citrix_user_submit_server"

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            self.connect()
            cursor = self.dbconnect.cursor()
            cursor.execute(query)
            self.dbconnect.commit()
            self.disconnect()
            return True
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "error": err.msg}
            return message

    # Xóa dữ liệu trong bảng user_submit_server
    # Xóa dữ liệu trong bảng user_submit_service
    def delete_citrix_service(self, serviceid, requestid=None, lbid=None):
        try:
            conditions = []
            conditions.append(f"serviceid = '{serviceid}'")
            if lbid is not None:
                conditions.append(f"lbid = '{lbid}'")
            if requestid is not None:
                conditions.append(f"requestid = '{requestid}'")

            query = f"DELETE FROM citrix_user_submit_service"

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            self.connect()
            cursor = self.dbconnect.cursor()
            cursor.execute(query)
            self.dbconnect.commit()
            self.disconnect()
            return True
        except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.ProgrammingError as err:
            message = {"code": 0, "error": err.msg}
            return message
        except mysql.connector.Error as err:
            message = {"code": 0, "error": err.msg}
            return message

    # Xóa dữ liệu trong bảng user_submit_service
