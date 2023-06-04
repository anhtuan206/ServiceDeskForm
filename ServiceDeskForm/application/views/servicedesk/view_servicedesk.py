import urllib3
from flask import Blueprint, render_template, json, request, make_response, jsonify
from email_validator import validate_email, EmailNotValidError
from ...database import FirewallRule
from ...database import Citrix
from ...api.manage_engine import ServiceDeskPlus
import ipaddress

urllib3.disable_warnings()

bp_servicedesk = Blueprint("servicedesk", __name__, url_prefix="/servicedesk")

mysql_firewall = FirewallRule
mysql_citrix = Citrix
hotrocntt = ServiceDeskPlus(
    url="hotrocntt.cpc.vn", authtoken="564C437D-62C0-4458-8B16-53847F2EEAD9"
)


@bp_servicedesk.get("/")
def servicedesk_root():
    return make_response(jsonify({"code": 1, "message": "Success"}), 200)


# Firewall Section
@bp_servicedesk.get("/firewall1/<string:request_id>")
def view_servicedesk_firewall1(request_id):
    pass

@bp_servicedesk.route(
    "/firewall/<string:requestid>", methods=["GET", "POST", "DELETE", "PUT"]
)
def view_servicedesk_firewall(requestid):
    # Validate form data
    def validate_new_rule_data(form_data):
        result = {"code": 0, "message": None}
        if not requestid == form_data.get("requestid"):
            message = "RequestID không hợp lệ!"
            return result
        name = form_data.get("name")
        if not name or not len(name) > 0:
            result["message"] = "Tên không hợp lệ!"
            return result
        sources = form_data.get("source")
        if not sources:
            result["message"] = "Địa chỉ nguồn không hợp lệ!"
            return result
        else:
            for source in sources:
                if not len(source) > 0 or validate_ipaddress(source) is False:
                    result["message"] = "Địa chỉ nguồn không hợp lệ!"
                    return result

        destinations = form_data.get("destination")
        if not destinations:
            result["message"] = "Địa chỉ đích không hợp lệ!"
            return result
        else:
            for destination in destinations:
                if not len(destination) > 0 or validate_ipaddress(destination) is False:
                    result["message"] = "Địa chỉ đích không hợp lệ!"
                    return result

        services = form_data.get("service")
        if not services:
            result["message"] = "Cổng kết nối không hợp lệ!"
            return result
        else:
            for service in services:
                if type(service.get("port")) is not int or service.get("port") is None:
                    result["message"] = "Cổng kết nối không hợp lệ!"
                    return result
        return True

    # Validate form data
    # Validate IP Address
    def validate_ipaddress(ip_string):
        try:
            ip_object = ipaddress.ip_address(ip_string)
            return True
        except ValueError:
            return False

    # Validate IP Address
    # Submit form data
    if request.method == "POST":
        content_type = request.headers.get("Content-Type")
        if content_type == "application/json":
            jsonData = request.json
            valid_data = validate_new_rule_data(jsonData)
            if valid_data is not True:
                return make_response(jsonify(valid_data), 200)
            if mysql_firewall().insert_firewall_user_submit_rule(jsonData) is True:
                return make_response(jsonify({"code": 1, "message": "Success"}), 200)
            return make_response(jsonify(result), 200)
        else:
            return make_response(
                jsonify({"code": 0, "message": "Kiểu dữ liệu không hỗ trợ"}), 200
            )
    # Submit form data
    # Get form data
    if request.method == "GET":
        servicedeskid = mysql_firewall().get_servicedesk_firewall(requestid=requestid)
        # Case 1: ticket không tồn tại trong database
        if servicedeskid["code"] == 1 and len(servicedeskid["data"]) > 0:
            request_data = mysql_firewall().get_firewall_user_submit_rule(
                requestid=requestid
            )
            if request_data["code"] == 1 and len(request_data["data"]) > 0:
                return render_template(
                    "servicedesk/servicedesk_firewall.html",
                    requestid=requestid,
                    request_data=request_data["data"],
                )
            elif request_data["code"] == 0:
                return render_template(
                    "servicedesk/servicedesk_firewall.html",
                    requestid=requestid,
                    error=request_data["data"],
                )
            else:
                return render_template(
                    "servicedesk/servicedesk_firewall.html", requestid=requestid
                )
        elif servicedeskid["code"] == 0:
            return render_template(
                "servicedesk/servicedesk_firewall.html",
                requestid=requestid,
                error=servicedeskid["data"],
            )
        else:
            return render_template(
                "servicedesk/servicedesk_firewall.html",
                requestid=requestid,
                error=f"Request ID {requestid} không hợp lệ",
            )
    # Get form data
    # Delete form record
    if request.method == "DELETE":
        content_type = request.headers.get("Content-Type")
        if content_type == "application/json":
            jsonData = request.json
            if jsonData["type"] == "rule":
                result = mysql_firewall().remove_user_submit_rule(
                    requestid=requestid, ruleid=jsonData["ruleid"]
                )
                if result["code"] == 1:
                    return make_response(result, 200)
                else:
                    message = jsonify(code="0", message="Error")
                    return make_response(message, 200)
            if jsonData["type"] in ["source", "destination", "service"]:
                result = mysql_firewall().remove_firewall_user_submit_object(
                    ruleid=jsonData["ruleid"],
                    objectid=jsonData["objectid"],
                    dtype=jsonData["type"],
                )
                if result["code"] == 1:
                    return make_response(result, 200)
                else:
                    message = jsonify(code="0", message="Error")
                    return make_response(message, 200)

    # Delete form record
    # Validate form update data
    def validate_update_rule_data(form_data):
        name = form_data.get("name")
        sources = form_data.get("sources")
        destinations = form_data.get("destinations")
        services = form_data.get("services")
        result = {"code": 0, "message": None}
        if not name or not len(name) > 0:
            result["message"] = "Tên không hợp lệ!"
            return result
        if not sources:
            result["message"] = "Địa chỉ nguồn không hợp lệ!"
            return result
        else:
            for source in sources:
                if (
                    not len(source["value"]) > 0
                    or validate_ipaddress(source["value"]) is False
                ):
                    result["message"] = "Địa chỉ nguồn không hợp lệ!"
                    return result
        if not destinations:
            result["message"] = "Địa chỉ đích không hợp lệ!"
            return result
        else:
            for destination in destinations:
                if (
                    not len(destination["value"]) > 0
                    or validate_ipaddress(destination["value"]) is False
                ):
                    result["message"] = "Địa chỉ đích không hợp lệ!"
                    return result
        if not services:
            result["message"] = "Cổng kết nối không hợp lệ!"
            return result
        else:
            for service in services:
                if type(service["value"]) is not int or service["value"] is None:
                    result["message"] = "Cổng kết nối không hợp lệ!"
                    return result
        return True

    # Validate form update data
    # Update form data
    if request.method == "PUT":
        content_type = request.headers.get("Content-Type")
        if content_type == "application/json":
            # Update rule name and description
            jsonData = request.json
            valid_data = validate_update_rule_data(jsonData)
            if valid_data is not True:
                return make_response(jsonify(valid_data), 200)
            result = mysql_firewall().update_firewall_user_submit_rule(
                ruleid=jsonData.get("ruleid"),
                name=jsonData.get("name"),
                description=jsonData.get("description"),
            )
            # Update Source, Destination, Service
            if result is not True:
                return make_response(jsonify(result), 200)
            datatype = ["sources", "destinations", "services"]
            for item in datatype:
                for element in jsonData[item]:
                    result = mysql_firewall().update_firewall_user_submit_object(
                        ruleid=element.get("ruleid"),
                        objectid=element.get("objectid"),
                        datatype=item,
                        value=element.get("value"),
                    )
                    if result is not True:
                        return make_response(jsonify(result), 200)
            return make_response(jsonify({"code": 1, "message": "Success"}), 200)
        else:
            return make_response(
                jsonify({"code": 0, "message": "Kiểu dữ liệu không hỗ trợ"}), 200
            )
    # Update form data


# Firewall Section

# Citrix Section
@bp_servicedesk.get("/citrix/<string:requestid>")
def view_servicedesk_citrix(requestid):
    # Check if request valid
    servicedesk_request = mysql_citrix().get_servicedesk_citrix_request(
        requestid=requestid
    )
    if type(servicedesk_request) is not (dict or json):
        return render_template(
            "servicedesk/servicedesk_citrix.html",
            requestid=requestid,
            case=1,
            data={"code": 0, "data": f"Lỗi kết nối cơ sở dữ liệu"},
        )
    # Case 1: Ticket không tồn tại trong hệ thống -> trả về thông báo lỗi
    if servicedesk_request["code"] == 1 and not len(servicedesk_request["data"]) > 0:
        if hotrocntt.check_request_is_valid(request_id=requestid) is True:
            result = mysql_citrix().insert_citrix_servicedeskrequest(
                    requestid=requestid
                )
            if result is not True:
                return render_template(
                    "servicedesk/servicedesk_citrix.html",
                    requestid=requestid,
                    case=1,
                    data={
                        "code": 0,
                        "data": f"Lỗi khi nhập yêu cầu vào cơ sở dữ liệu",
                    },
                )
            return render_template(
                "servicedesk/servicedesk_citrix.html",
                requestid=requestid,
                case=3,
                data=mysql_citrix().get_servicedesk_citrix_request(requestid=requestid),
                approval_status=hotrocntt.get_request_approval_status(
                    request_id=requestid
                ),
            )
        return render_template(
            "servicedesk/servicedesk_citrix.html",
            requestid=requestid,
            case=1,
            data={"code": 0, "data": f"Request_id {requestid} không hợp lệ!"},
        )
        
    # Case 2: Query database trả về query exception => render template với thông tin lỗi
    if not servicedesk_request["code"] == 1:
        return render_template(
            "servicedesk/servicedesk_citrix.html",
            requestid=requestid,
            case=2,
            data=servicedesk_request,
        )
    # Case 3: Ticket tồn tại trong hệ thống và chưa nhập dữ liệu
    if servicedesk_request["code"] == 1 and len(servicedesk_request["data"]) > 0:
        all_request_data = mysql_citrix().get_servicedesk_request_info_all_by_requestid(
            requestid=requestid
        )
        if (
            all_request_data.get("code") == 1
            and not len(all_request_data.get("data")) > 0
        ):
            return render_template(
                "servicedesk/servicedesk_citrix.html",
                requestid=requestid,
                case=3,
                data=None,
                approval_status=hotrocntt.get_request_approval_status(
                    request_id=requestid
                ),
            )
        # Case 4: Ticket tồn tại trong hệ thống và đã nhập dữ liệu
        data = []
        lb_data = mysql_citrix().get_citrix_lb(requestid=requestid)
        # Nếu request lb_data trả về exception
        if not lb_data.get("code") == 1:
            return render_template(
                "servicedesk/servicedesk_citrix.html",
                requestid=requestid,
                case=2,
                data=lb_data,
            )
        for lb in lb_data["data"]:
            servers = mysql_citrix().get_citrix_servers(lbid=lb.get("lbid"))
            if not servers.get("code") == 1:
                return render_template(
                    "servicedesk/servicedesk_citrix.html",
                    requestid=requestid,
                    case=2,
                    data=servers,
                )
            services = mysql_citrix().get_citrix_services(lbid=lb.get("lbid"))
            if not services.get("code") == 1:
                return render_template(
                    "servicedesk/servicedesk_citrix.html",
                    requestid=requestid,
                    case=2,
                    data=services,
                )
            data.append(
                {
                    "lb": lb,
                    "servers": servers.get("data"),
                    "services": services.get("data"),
                }
            )
        # return make_response(jsonify({"code": 1,"data": data}),200)
        return render_template(
            "servicedesk/servicedesk_citrix.html",
            requestid=requestid,
            case=4,
            data={"code": 1, "data": data},
            approval_status=hotrocntt.get_request_approval_status(request_id=requestid),
        )

    return make_response(jsonify(servicedesk_request), 200)
    # return render_template('servicedesk/servicedesk_citrix.html')


# View form
@bp_servicedesk.post("/citrix/<string:requestid>")
def post_servicedesk_citrix(requestid):
    def validate_ipaddress(ip_string):
        try:
            ip_object = ipaddress.ip_address(ip_string)
            return True
        except ValueError:
            return False

    def validate_data(postData):
        message = {"code": 0, "message": None}
        if not validate_ipaddress(postData.get("vip")):
            message["message"] = f"Địa chỉ VIP không hợp lệ! {postData.get('vip')}"
            return make_response(jsonify(message), 200)
        if type(postData.get("description")) is not str:
            message[
                "message"
            ] = f"Kiểu dữ liệu mô tả không hợp lệ! {postData.get('description')}"
            return make_response(jsonify(message), 200)
        for item in postData.get("servers"):
            if type(item.get("servername")) is not str:
                message[
                    "message"
                ] = f"Tên máy chủ không hợp lệ! {item.get('servername')}"
                return make_response(jsonify(message), 200)
            if not validate_ipaddress(item.get("serverip")):
                message[
                    "message"
                ] = f"Địa chỉ IP server không hợp lệ! {item.get('serverip')}"
                return make_response(jsonify(message), 200)
        for item in postData.get("services"):
            if type(item.get("port")) is not int:
                message[
                    "message"
                ] = f"Kiểu dữ liệu cổng không hợp lệ! {item.get('port')}"
                return make_response(jsonify(message), 200)
            if type(item.get("protocol")) is not str or item.get("protocol") not in [
                "TCP",
                "UDP",
                "HTTP",
                "HTTPS",
            ]:
                message["message"] = f"Giao thức ko hợp lệ! {item.get('protocol')}"
                return make_response(jsonify(message), 200)

    jsonData = request.json
    validate_data(jsonData)
    # Insert citrix_user_submit_lb
    insert_lb = mysql_citrix().insert_citrix_lb(
        requestid=requestid,
        description=jsonData.get("description"),
        vip=jsonData.get("vip"),
    )
    if insert_lb is not True:
        return make_response(jsonify(insert_lb), 200)
    # Lấy ID LB vừa tạo
    inserted_lb = mysql_citrix().get_citrix_lb(
        requestid=requestid, vip=jsonData.get("vip")
    )
    if inserted_lb.get("code") != 1:
        return make_response(jsonify(inserted_lb), 200)
    lb_table = inserted_lb.get("data")
    lbid = lb_table[0].get("lbid")
    # Lấy ID LB vừa tạo
    # Tạo server
    for item in jsonData.get("servers"):
        insert_server = mysql_citrix().insert_citrix_server(
            lbid=lbid,
            servername=item.get("servername"),
            serveripaddress=item.get("serverip"),
            requestid=requestid,
        )
        if insert_server is not True:
            return make_response(jsonify(insert_server), 200)
    # Tạo server
    # Tạo service
    for item in jsonData.get("services"):
        insert_service = mysql_citrix().insert_citrix_service(
            lbid=lbid,
            serviceport=item.get("port"),
            servicetype=item.get("protocol"),
            requestid=requestid,
        )
        if insert_service is not True:
            return make_response(jsonify(insert_server), 200)
    # Tạo service
    # Return True
    message = {"code": 1, "message": "Success"}
    return make_response(jsonify(message), 200)


# Gọi hàm submit for approval
@bp_servicedesk.post("/citrix/<string:requestid>/submitforapproval")
def post_submit_for_approval(requestid):
    def check_email(email):
        try:
            v = validate_email(email)
            return True
        except EmailNotValidError as e:
            return False

    try:
        jsonData = request.json
        email_id = jsonData.get("email_id")
        if email_id is None or check_email(email_id) is not True:
            return make_response(
                jsonify({"code": 0, "data": "Người phê duyệt không hợp lệ"}), 200
            )
        message = jsonData.get("message")
        approver_details = hotrocntt.get_users(user_email=email_id)
        if type(approver_details) is not dict:
            return make_response(
                jsonify({"code": 0, "data": "Lỗi lấy thông tin người phê duyệt"}), 200
            )
        approver_id = [user.get("id") for user in approver_details.get("users")]
        result = hotrocntt.submit_for_approval(
            request_id=requestid, approver_id=approver_id, message=message
        )
        if type(result) is not dict:
            return make_response(
                jsonify({"code": 0, "data": "Gửi phê duyệt không thành công"}), 200
            )
        if (
            result.get("response_status").get("status_code") == 2000
            and result.get("response_status").get("status") == "success"
        ):
            return make_response(
                jsonify({"code": 1, "data": result.get("submit_for_approval")}), 200
            )
    except:
        return make_response(
            jsonify({"code": 0, "data": "Có lỗi xảy ra khi gửi yêu cầu phê duyệt"}), 200
        )


# Update form
@bp_servicedesk.put("/citrix/<string:requestid>")
def put_servicedesk_citrix(requestid):
    def validate_ipaddress(ip_string):
        try:
            ip_object = ipaddress.ip_address(ip_string)
            return True
        except ValueError:
            return False

    def validate_data(postData):
        message = {"code": 0, "message": None}
        if not validate_ipaddress(postData.get("vip")):
            message["message"] = f"Địa chỉ VIP không hợp lệ! {postData.get('vip')}"
            return make_response(jsonify(message), 200)
        if type(postData.get("description")) is not str:
            message[
                "message"
            ] = f"Kiểu dữ liệu mô tả không hợp lệ! {postData.get('description')}"
            return make_response(jsonify(message), 200)
        if type(postData.get("lbid")) is not int:
            message["message"] = f"Kiểu dữ lbid không hợp lệ! {postData.get('lbid')}"
            return make_response(jsonify(message), 200)
        for item in postData.get("servers"):
            if type(item.get("serverid")) is not int:
                message[
                    "message"
                ] = f"Kiểu dữ serverid không hợp lệ! {item.get('serverid')}"
                return make_response(jsonify(message), 200)
            if type(item.get("servername")) is not str:
                message[
                    "message"
                ] = f"Tên máy chủ không hợp lệ! {item.get('servername')}"
                return make_response(jsonify(message), 200)
            if not validate_ipaddress(item.get("serverip")):
                message[
                    "message"
                ] = f"Địa chỉ IP server không hợp lệ! {item.get('serverip')}"
                return make_response(jsonify(message), 200)
        for item in postData.get("services"):
            if type(item.get("serviceid")) is not int:
                message[
                    "message"
                ] = f"Kiểu dữ serviceid không hợp lệ! {item.get('serviceid')}"
                return make_response(jsonify(message), 200)
            if type(item.get("port")) is not int:
                message[
                    "message"
                ] = f"Kiểu dữ liệu cổng không hợp lệ! {item.get('port')}"
                return make_response(jsonify(message), 200)
            if type(item.get("protocol")) is not str or item.get("protocol") not in [
                "TCP",
                "UDP",
                "HTTP",
                "HTTPS",
            ]:
                message["message"] = f"Giao thức ko hợp lệ! {item.get('protocol')}"
                return make_response(jsonify(message), 200)

    jsonData = request.json
    validate_data(jsonData)
    # Update citrix_user_submit_lb
    result = mysql_citrix().update_citrix_lb(
        lbid=jsonData.get("lbid"),
        description=jsonData.get("description"),
        vip=jsonData.get("vip"),
    )
    if result is not True:
        return make_response(jsonify(result), 200)
    for item in jsonData.get("servers"):
        result = mysql_citrix().update_citrix_server(
            serverid=item.get("serverid"),
            servername=item.get("servername"),
            serveripaddress=item.get("serverip"),
        )
        if result is not True:
            return make_response(jsonify(result), 200)
    for item in jsonData.get("services"):
        result = mysql_citrix().update_citrix_service(
            serviceid=item.get("serviceid"),
            servicetype=item.get("protocol"),
            serviceport=item.get("port"),
        )
        if result is not True:
            return make_response(jsonify(result), 200)
    return make_response(jsonify({"code": 1, "message": "Success"}), 200)


# Delete request
@bp_servicedesk.delete("/citrix/<string:requestid>")
def delete_servicedesk_citrix(requestid):
    jsonData = request.json
    if jsonData.get("type") == "lb":
        lbid = jsonData.get("lbid")
        result = mysql_citrix().delete_citrix_lb(lbid=lbid, requestid=requestid)
        if result is not True:
            return make_response(jsonify(result), 200)
    if jsonData.get("type") == "server":
        lbid = jsonData.get("lbid")
        objectid = jsonData.get("objectid")
        result = mysql_citrix().delete_citrix_server(
            serverid=objectid, lbid=lbid, requestid=requestid
        )
        if result is not True:
            return make_response(jsonify(result), 200)
    if jsonData.get("type") == "service":
        lbid = jsonData.get("lbid")
        objectid = jsonData.get("objectid")
        result = mysql_citrix().delete_citrix_service(
            serviceid=objectid, lbid=lbid, requestid=requestid
        )
        if result is not True:
            return make_response(jsonify(result), 200)
    return make_response(jsonify({"code": 1, "data": "Success"}), 200)


# Citrix Section


# Service Desk Section: hotrocntt post thông tin request thông qua webhook
@bp_servicedesk.post("/<string:servicedesk_template>")
def post_servicedesk(servicedesk_template):
    jsonData = request.json
    if servicedesk_template == "citrix":
        result = mysql_firewall().insert_firewall_servicedeskrequest(
            requestid=jsonData.get("requestid"), subject=jsonData.get("subject")
        )
        if result is not True:
            return make_response(jsonify(result), 200)
    if servicedesk_template == "firewall":
        result = mysql_citrix().insert_citrix_servicedeskrequest(
            requestid=jsonData.get("requestid"), subject=jsonData.get("subject")
        )
        if result is not True:
            return make_response(jsonify(result), 200)
    return make_response(jsonify({"code": 0, "message": "Success"}), 200)


# Service Desk Section
