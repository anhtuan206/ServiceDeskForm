import urllib3
import urllib
import json
import requests

urllib3.disable_warnings()


class ServiceDeskPlus:
    def __init__(
        self, url="hotrocntt.cpc.vn", authtoken="564C437D-62C0-4458-8B16-53847F2EEAD9"
    ) -> None:
        self.url = url
        self.authtoken = authtoken

    def api_get(self, endpoint=None, params=None, data=None):
        try:
            url = f"https://{self.url}/{endpoint}"
            headers = {"authtoken": self.authtoken}
            response = requests.get(
                url, headers=headers, params=params, data=data, verify=False
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return e

    def api_post(self, endpoint, data):
        try:
            url = f"https://{self.url}/{endpoint}"
            headers = {"authtoken": self.authtoken}
            response = requests.post(url, headers=headers, data=data, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return e

    def api_delete(self, endpoint, data):
        try:
            url = f"https://{self.url}/{endpoint}"
            headers = {"authtoken": self.authtoken}
            response = requests.delete(url, headers=headers, data=data, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return e

    def api_put(self, endpoint, data):
        try:
            url = f"https://{self.url}/{endpoint}"
            headers = {"authtoken": self.authtoken}
            response = requests.put(url, headers=headers, data=data, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return e

    def get_requests(self, request_id=None, params=None):
        if request_id is not None:
            return self.api_get(endpoint=f"api/v3/requests/{request_id}")
        return self.api_get(endpoint="api/v3/requests")

    def get_users(self, user_id=None, user_email=None):
        if user_id is not None:
            return self.api_get(endpoint=f"api/v3/users/{user_id}")
        if user_email is not None:
            input_data = json.dumps(
                {
                    "list_info": {
                        "get_total_count": True,
                        "search_fields": {"email_id": user_email},
                    }
                }
            )
            params = {"input_data": input_data}
            return self.api_get(endpoint="api/v3/users", params=params)
        return self.api_get(endpoint="api/v3/users")

    def get_sites(self, site_id=None, params=None):
        if site_id is not None:
            return self.api_get(endpoint=f"api/v3/sites/{site_id}")
        return self.api_get(endpoint="api/v3/sites")

    def get_technicians(self, technician_id=None, params=None):
        if technician_id is not None:
            return self.api_get(endpoint=f"api/v3/technicians/{technician_id}")
        return self.api_get(endpoint="api/v3/technicians")

    def get_categories(self, category_id=None, params=None):
        if category_id is not None:
            return self.api_get(endpoint=f"/api/v3/categories/{category_id}")
        return self.api_get(endpoint="api/v3/categories")

    def get_request_approval_levels(self, request_id, approval_level_id=None):
        if approval_level_id is not None:
            return self.api_get(
                endpoint=f"api/v3/requests/{request_id}/approval_levels/{approval_level_id}"
            )
        return self.api_get(endpoint=f"api/v3/requests/{request_id}/approval_levels")

    def delete_request_approval_levels(self, request_id, approval_level_id):
        return self.api_get(
            endpoint=f"api/v3/requests/{request_id}/approval_levels/{approval_level_id}"
        )

    def add_request_approval(self, request_id, approval_level_id, approver_id):
        input_data = json.dumps({"approval": {"approver": {"id": approver_id}}})
        payload = {"input_data": input_data}
        return self.api_post(
            endpoint=f"api/v3/requests/{request_id}/approval_levels/{approval_level_id}/approvals",
            data=payload,
        )

    def delete_request_approval(self, request_id, approval_level_id, approval_id):
        input_data = {}
        payload = {"input_data": input_data}
        return self.api_delete(
            endpoint=f"api/v3/requests/{request_id}/approval_levels/{approval_level_id}/approvals/{approval_id}",
            data=payload,
        )

    def send_notification_for_request_approval(
        self, request_id, approval_level_id, approval_id
    ):
        input_data = json.dumps(
            {
                "notification": {
                    "subject": "Approval required for a Request",
                    "description": "Your approval is required for a Request to act upon. The details of the Request can be found at $ApprovalLink",
                }
            }
        )
        payload = {"input_data": input_data}
        return self.api_put(
            endpoint=f"api/v3/requests/{request_id}/approval_levels/{approval_level_id}/approvals/{approval_id}/_send_notification",
            data=payload,
        )

    def get_request_approvals(self, request_id, approval_level_id, approval_id=None):
        if approval_id is not None:
            return self.api_get(
                endpoint=f"api/v3/requests/{request_id}/approval_levels/{approval_level_id}/approvals/{approval_id}"
            )
        return self.api_get(
            endpoint=f"api/v3/requests/{request_id}/approval_levels/{approval_level_id}/approvals"
        )

    def submit_for_approval(self, request_id, approver_id,message):
        try:
            request_details = self.get_requests(request_id=request_id, params=None)
            request_subject = request_details.get("request").get("subject")
            requester_name = request_details.get("request").get("requester").get("name")
            requester_email = (
                request_details.get("request").get("requester").get("email_id")
            )
            requester_mobile = (
                request_details.get("request").get("requester").get("mobile")
            )
            request_template = (
                request_details.get("request").get("udf_fields").get("udf_sline_3019")
            )
            notification_title = (
                f"Yêu cầu chờ phê duyệt {request_id} từ hotrocntt.cpc.vn"
            )
            notification_description = f"""<div>
                    {requester_name} gửi cho bạn có một yêu cầu phê duyệt có nội dung nội dung:<br>
                    - Phê duyệt khởi tạo cấu hình {request_template.upper()}<br>
                    - Tiêu đề: {request_subject} <br>
                    - Chi tiết cấu hình: <a target="_blank" href="https://nssa.cpc.vn/servicedesk/{request_template}/{request_id}">https://nssa.cpc.vn/servicedesk/{request_template}/{request_id}</a><br>
                    - Lời nhắn: {message} <br>
                    Thông tin người yêu cầu:<br>
                    - Email: {requester_email}<br>
                    - Mobile: {requester_mobile}<br><br>

                    Anh/Chị vui lòng truy cập link sau để xem chi tiết và thực hiện phê duyệt: <a target="_blank" href="$ApprovalLink">Phê Duyệt</a>
                </div>"""
            input_data = {
                "approvals": [
                    {"approver": {"id": approver}} for approver in approver_id
                ],
                "notification": {
                    "title": notification_title,
                    "description": notification_description,
                },
            }
            payload = "input_data=" + urllib.parse.quote(json.dumps(input_data))
            headers = {
                "Accept": "vnd.manageengine.v3+json",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "authtoken": "564C437D-62C0-4458-8B16-53847F2EEAD9",
            }
            url = f"https://{self.url}/api/v3/requests/{request_id}/submit_for_approval"
            response = requests.request("POST", url, headers=headers, data=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions as e:
            return e

    def get_request_approval_status(self,request_id) -> dict:
        request_details = self.get_requests(request_id=request_id)
        if type(request_details) is not dict:
            return {"code": 0, "message": "Exception occurs during get request information from hotrocntt.cpc.vn"}
        return {"code": 1, "message": request_details.get("request").get("approval_status")}

    def check_request_is_valid(self,request_id,request_template=None) -> dict:
        request_details = self.get_requests(request_id=request_id)
        if type(request_details) is not dict:
            return {"code": 0, "message": "Exception occurs during get request information from hotrocntt.cpc.vn"}
        if request_details.get("response_status").get("status_code") == 4000:
            return False
        if request_details.get("response_status").get("status_code") == 2000:
            if request_details.get("request").get("udf_fields") is None:
                return False
            if request_details.get("request").get("udf_fields").get("udf_sline_3019") is None:
                return False
            if request_details.get("request").get("udf_fields").get("udf_sline_3019") not in ["citrix","firewall"]:
                return False
            if request_template is not None:
                if request_details.get("request").get("udf_fields").get("udf_sline_3019") != request_template:
                    return False
            return True
        return False

    