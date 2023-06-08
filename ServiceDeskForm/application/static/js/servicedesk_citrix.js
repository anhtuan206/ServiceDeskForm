// 1. Template Script //
// 1.1. SideNav Initialization
$(".button-collapse").sideNav();

var container = document.querySelector('.custom-scrollbar');
var ps = new PerfectScrollbar(container, {
    wheelSpeed: 0.5,
    wheelPropagation: true,
    minScrollbarLength: 20
});

// 1.2. Data Picker Initialization
$('.datepicker').pickadate();

// 1.3. Tooltips Initialization
$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})
// 1.4. Dark Mode Button
$(function () {
    $('#dark-mode').on('click', function (e) {

        e.preventDefault();
        $('h4, button').not('.check').toggleClass('dark-grey-text text-white');
        $('.list-panel a').toggleClass('dark-grey-text');

        $('footer, .card').toggleClass('dark-card-admin');
        $('body, .navbar').toggleClass('white-skin navy-blue-skin');
        $(this).toggleClass('white text-dark btn-outline-black');
        $('body').toggleClass('dark-bg-admin');
        $('h6, .card, p, td, th, i, li a, h4, input, label').not(
            '#slide-out i, #slide-out a, .dropdown-item i, .dropdown-item').toggleClass('text-white');
        $('.btn-dash').toggleClass('grey blue').toggleClass('lighten-3 darken-3');
        $('.gradient-card-header').toggleClass('white black lighten-4');
        $('.list-panel a').toggleClass('navy-blue-bg-a text-white').toggleClass('list-group-border');

    });
});



// 2. Main page //
// 2.1. Đánh số thứ tự các dòng trong bảng
function SoThuTu() {
    let tbl_citrix_request = document.getElementById("tbl_citrix_request");
    if (tbl_citrix_request && tbl_citrix_request.rows.length > 0) {
        for (let index = 1; index < tbl_citrix_request.rows.length; index++) {
            let stt_cell = tbl_citrix_request.rows[index].cells.item(0);
            value = '<span class="me-2 p-1" id="span-' + index + '">' + index + '</span>';
            stt_cell.innerHTML = value;
        }
    }
}
document.addEventListener("DOMContentLoaded", () => {
    SoThuTu();
});
// 2.2. Thêm form mới để nhập thông tin
function AddForm() {
    let tbl_citrix_request = document.getElementById("tbl_citrix_request");
    let lbid = Math.random().toString(36).substring(2, 7);
    let requestid = document.getElementById("requestid").value
    let objectid = Math.random().toString(36).substring(2, 7);

    let newform = `
    <!-- Index Column -->
    <td>
      <span class="me-2 p-1" id="span-${lbid}">1</span>
    </td>
    <!-- Index Column -->
    <!-- IP Citrix -->
    <td>
      <div class="input-group ">
        <input type="text" class="form-control form-control-sm" placeholder="VIP" id="lb-${lbid}" required>
      </div>
    </td>
    <!-- IP Citrix -->
    <!-- Server column -->
    <td>
      <div id="server-array-${lbid}">
        <div class="input-group  data-edit" id="input-group-server-${lbid}-${objectid}" data-lbid="${lbid}"
          data-requestid="${requestid}" data-objectid="${objectid}">
          <input type="text" class="form-control form-control-sm data-edit" placeholder="Tên máy chủ"
            id="input-servername-${lbid}-${objectid}" data-lbid="${lbid}" data-requestid="${requestid}" data-objectid="${objectid}">
          <input type="text" class="form-control form-control-sm data-edit" placeholder="Địa chỉ IP"
            id="input-serverip-${lbid}-${objectid}" data-lbid="${lbid}" data-requestid="${requestid}" data-objectid="${objectid}">
          <div class="input-group-append data-edit">
            <button
              class="btn btn-sm btn-md btn-outline-default m-0 px-2 py-1 z-depth-0 waves-effect data-edit"
              type="button" id="btn-remove-server-${lbid}-${objectid}"
              onclick="RemoveObjectRow(this,objectType='server',removedb=false)" data-lbid="${lbid}"
              data-requestid="${requestid}" data-objectid="${objectid}">X
            </button>
          </div>
        </div>
      </div>
      <!-- Add server -->
      <div class="d-grid">
        <button class="btn btn-sm" type="button" id="btn-add-server-${lbid}"
          onclick="AddObjectRow(this,objectType='server')" data-lbid="${lbid}"
          data-requestid="${requestid}">
          Thêm
        </button>
      </div>
    </td>
    <!-- Server column -->
    <!-- Service and protocol column -->
    <td>
      <div id="serviceandprotocol-array-${lbid}">
        <div class="input-group  data-edit" id="input-group-serviceandprotocol-${lbid}-${objectid}"
          data-lbid="${lbid}" data-requestid="${requestid}" data-objectid="${objectid}">
          <input type="text" class="form-control form-control-sm data-edit" placeholder="Cổng"
            id="input-port-${lbid}-${objectid}" data-lbid="${lbid}" data-requestid="${requestid}"
            data-objectid="${objectid}">
          <select class="browser-default custom-select custom-select-sm data-edit"
            id="slt-protocol-${lbid}-${objectid}" data-lbid="${lbid}" data-requestid="${requestid}"
            data-objectid="${objectid}">
            <option selected>Giao thức</option>
            <option value="HTTP">HTTP</option>
            <option value="HTTPS">HTTPS</option>
            <option value="TCP">TCP</option>
            <option value="UDP">UDP</option>
          </select>
          <div class="input-group-append data-edit">
            <button
              class="btn btn-sm btn-md btn-outline-default m-0 px-2 py-1 z-depth-0 waves-effect data-edit"
              type="button" id="btn-remove-serviceandprotocol-${lbid}-${objectid}"
              onclick="RemoveObjectRow(this,objectType='serviceandprotocol',removedb=false)"
              data-lbid="${lbid}" data-requestid="${requestid}" data-objectid="${objectid}">
              X
            </button>
          </div>
        </div>
      </div>
      <!-- Button Add -->
      <div class="d-grid">
        <button class="btn btn-sm" type="button" id="btn-add-serviceandprotocol-${lbid}"
          onclick="AddObjectRow(this,objectType='serviceandprotocol')" data-lbid="${lbid}"
          data-requestid="${requestid}" data-objectid="${objectid}">
          Thêm
        </button>
      </div>
    </td>
    <!-- Service and protocol column -->
    <!-- Description Column -->
    <td>
      <textarea class="form-control form-control-sm data-edit" placeholder="Mô tả"
        id="description-${lbid}"></textarea>
    </td>
    <!-- Description Column -->
    <!-- Functional Column -->
    <td>
      <div class="input-group">
        <!-- button save -->
        <button type="button" class="btn btn-outline-primary btn-sm waves-effect waves-light mt-0" id="btn-save-lb-${lbid}" data-lbid="${lbid}"
          data-requestid="${requestid}" onclick="SaveLB(this)">
          Lưu
        </button>
        <!-- button remove -->
        <button type="button" class="btn btn-outline-danger btn-sm waves-effect waves-light mt-0" id="btn-remove-lb-${lbid}" data-lbid="${lbid}"
          data-requestid="${requestid}"
          onclick="RemoveObjectRow(this,objectType='lb',removedb=false)">
          Xóa
        </button>
      </div>
    </td>
    <!-- Functional Column -->
    `;
    let newrow = tbl_citrix_request.insertRow(tbl_citrix_request.rows.length);
    newrow.innerHTML = newform;
    SoThuTu();

}
// 2.3. Thêm input cho các chột ip nguồn, ip đích, cổng
function AddObjectRow(clicked, objectType) {
    let lbid = clicked.dataset.lbid;
    let requestid = clicked.dataset.requestid
    let objectarray = document.getElementById(objectType + '-array-' + lbid);
    // let objectid = objectarray.childElementCount;
    let objectid = Math.random().toString(36).substring(2, 7);
    objectHTML = null
    if (objectType == "server") {
        let objectHtml = `
        <div class="input-group  data-edit" id="input-group-${objectType}-${lbid}-${objectid}" data-lbid="${lbid}" data-requestid="${requestid}" data-objectid="${objectid}">
          <input type="text"  class="form-control form-control-sm data-edit" placeholder="Tên máy chủ" id="input-servername-${lbid}-${objectid}" data-lbid="${lbid}" data-requestid="${requestid}" data-objectid="${objectid}">
          <input type="text"  class="form-control form-control-sm data-edit" placeholder="Địa chỉ IP" id="input-serverip-${lbid}-${objectid}" data-lbid="${lbid}" data-requestid="${requestid}" data-objectid="${objectid}">
          <div class="input-group-append data-edit">
            <button class="btn btn-sm btn-md btn-outline-default m-0 px-2 py-1 z-depth-0 waves-effect data-edit" type="button" id="btn-remove-${objectType}-${lbid}-${objectid}" onclick="RemoveObjectRow(this,'${objectType}',removedb=false)" data-lbid="${lbid}" data-requestid="${requestid}" data-objectid="${objectid}">
                X
            </button>
          </div>
        </div>
          `;
        $("#" + objectType + "-array-" + lbid).append(objectHtml);

        // objectarray.insertAdjacentHTML('beforeend', objectHtml);
    };
    if (objectType == "serviceandprotocol") {
        let objectHtml = `
        <div class="input-group  data-edit" id="input-group-${objectType}-${lbid}-${objectid}" data-lbid="${lbid}" data-requestid="${requestid}" data-objectid="${objectid}">
          <input type="text"  class="form-control form-control-sm data-edit"
            placeholder="Cổng" id="input-port-${lbid}-${objectid}" data-lbid="${lbid}" data-requestid="${requestid}" data-objectid="${objectid}">
          <select class="browser-default custom-select custom-select-sm data-edit" id="slt-protocol-${lbid}-${objectid}" data-lbid="${lbid}" data-requestid="${requestid}" data-objectid="${objectid}">
            <option selected>Giao thức</option>
            <option value="HTTP">HTTP</option>
            <option value="HTTPS">HTTPS</option>
            <option value="TCP">TCP</option>
            <option value="UDP">UDP</option>
          </select>
          <div class="input-group-append data-edit">
            <button
              class="btn btn-sm btn-md btn-outline-default m-0 px-2 py-1 z-depth-0 waves-effect data-edit"
              type="button" id="btn-remove-${lbid}-${objectid}"
              onclick="RemoveObjectRow(this,objectType='${objectType}',removedb=false)" data-lbid="${lbid}" data-requestid="${requestid}" data-objectid="${objectid}">
              X
            </button>
          </div>
        </div>`;
        $("#" + objectType + "-array-" + lbid).append(objectHtml);
        // objectarray.insertAdjacentHTML('beforeend', objectHtml);

    }
}
// 2.4. Xóa một dòng trong bảng
function Delete_Table_Row(table_id, row_number) {
    document.getElementById(table_id).deleteRow(row_number);
}
// 2.5. Hàm chạy khi click nút xóa đối tượng và xóa dòng
function RemoveObjectRow(clicked, objectType, removedb = false) {
    let requestid = clicked.dataset.requestid
    let lbid = clicked.dataset.lbid;
    let objectid = clicked.dataset.objectid;
    // Xóa một đối tượng
    if (objectType != "lb") {
        if (removedb == true) {
            let postData = {
                type: objectType,
                lbid: lbid,
                objectid: objectid
            };
            fetch("/servicedesk/citrix/" + requestid, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(postData)
            })
                .then((response) => {
                    return response.json()
                })
                .then((data) => {
                    let result = data;
                    if (result["code"] == 1) {
                        location.reload();
                    }
                    else {
                        message = null;
                        if (result.error) { message = result.error }
                        if (result.data) { message = result.data }
                        document.getElementById("alert_content").innerText = message;
                        document.getElementById("tbl_alert").removeAttribute("hidden", true)
                    }
                })
                .catch(error => console.error(error));
        }
        else {
            $("#input-group-" + objectType + "-" + lbid + "-" + objectid).remove();
        }
    }
    // Xóa một rule
    if (objectType == 'lb') {
        // let idprefix = "btn-remove-lb-";
        // objectrow = clicked.substring(idprefix.length);

        if (removedb == true) {
            let postData = {
                type: "lb",
                lbid: clicked.dataset.lbid
            };
            fetch("/servicedesk/citrix/" + requestid, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(postData)
            })
                .then((response) => {
                    return response.json()
                })
                .then(result => {
                    if (result["code"] == 1) {
                        location.reload();
                    }
                    else {
                        message = null;
                        if (result.error) { message = result.error }
                        if (result.data) { message = result.data }
                        document.getElementById("alert_content").innerText = message;
                        document.getElementById("tbl_alert").removeAttribute("hidden", true)
                    }
                })
                .catch(error => console.error(error));
        }
        else {
            let btn = document.getElementById(clicked.id);
            let tr = btn.parentNode.parentNode;
            Delete_Table_Row("tbl_citrix_request", tr.rowIndex);
            SoThuTu();
        }
    }
}
// 2.6. Hàm chạy khi click nút lưu rule mới
function SaveLB(clicked) {
    let requestid = clicked.dataset.requestid;
    let lbid = clicked.dataset.lbid;
    let vip = $("#lb-" + lbid).val();
    let description = $("#description-" + lbid).val();
    let servers = []
    let services = []
    $("#server-array-" + lbid).children(".data-edit").each(function () {
        let object_id = $(this).data("objectid");
        let servername = $("#input-servername-" + lbid + "-" + object_id).val();
        let serverip = $("#input-serverip-" + lbid + "-" + object_id).val();
        servers.push({
            servername: servername,
            serverip: serverip
        });
    });
    $("#serviceandprotocol-array-" + lbid).children(".data-edit").each(function () {
        let object_id = $(this).data("objectid")
        let port = $("#input-port-" + lbid + "-" + object_id).val();
        let protocol = $("#slt-protocol-" + lbid + "-" + object_id).val();
        services.push({
            port: parseInt(port),
            protocol: protocol
        });
    });
    postData = {
        vip: vip,
        servers: servers,
        services: services,
        description: description
    }
    fetch("/servicedesk/citrix/" + requestid, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(postData)
    })
        .then(response => {
            return response.json()
        })
        .then(result => {
            if (result["code"] == 1) {
                location.reload();
            }
            else {
                message = null;
                if (result.error) { message = result.error }
                if (result.data) { message = result.data }
                if (result.message) { message = result.message }
                document.getElementById("alert_content").innerText = message;
                document.getElementById("tbl_alert").removeAttribute("hidden", true)
            }
        })
        .catch(error => console.error(error));
}

// 2.7. Hàm chạy khi click nút sửa
function EditLB(clicked) {
    // ẩn và hiện các trường thông tin
    let btn_edit = clicked;
    $("#row-" + btn_edit.dataset.lbid + " td").each(function () {
        $(this).find(".data-view").each(function () {
            $(this).hide();
        });
        $(this).find(".data-edit").each(function () {
            $(this).attr({
                "disabled": false,
                "hidden": false
            });
        })
    })
    // ẩn và hiện các trường thông tin

}
// Hàm chạy khi click nút sửa
// 2.8. Hàm chạy khi click nút cập nhật
function UpdateLB(clicked) {
    // ẩn và hiện các trường thông tin
    let btn_clicked = clicked;
    let requestid = btn_clicked.dataset.requestid
    // Lấy dữ liệu từ các trường và chạy fetch
    let lbid = btn_clicked.dataset.lbid;
    let vip = $("#lb-" + lbid).val();
    let description = $("#description-" + lbid).val();
    let servers = []
    let services = []
    $("#server-array-" + lbid).children(".data-edit").each(function () {
        let object_id = $(this).data("objectid")
        let servername = $("#input-servername-" + lbid + "-" + object_id).val();
        let serverip = $("#input-serverip-" + lbid + "-" + object_id).val();
        servers.push({
            serverid: parseInt(object_id),
            servername: servername,
            serverip: serverip
        });
    });
    $("#serviceandprotocol-array-" + lbid).children(".data-edit").each(function () {
        let object_id = $(this).data("objectid")
        let port = $("#input-port-" + lbid + "-" + object_id).val();
        let protocol = $("#slt-protocol-" + lbid + "-" + object_id).val();
        services.push({
            serviceid: parseInt(object_id),
            port: parseInt(port),
            protocol: protocol
        });
    });

    postData = {
        vip: vip,
        lbid: parseInt(lbid),
        servers: servers,
        services: services,
        description: description
    }
    // Goi fetch data
    fetch("/servicedesk/citrix/" + requestid, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(postData)
    })
        .then((response) => {
            return response.json()
        })
        .then(result => {
            if (result["code"] == 1) {
                location.reload();
            }
            else {
                message = null;
                if (result.error) { message = result.error }
                if (result.data) { message = result.data }
                document.getElementById("alert_content").innerText = message;
                document.getElementById("tbl_alert").removeAttribute("hidden", true)
            }
        })
        .catch(error => console.error(error));
}

// 3. Submit for approval modal //
function submit_for_approval(clicked) {
    let requestid = clicked.dataset.requestid
    let approver = $("#md-slt-approver-" + requestid).val();
    let message = $("#md-textarea-message-" + requestid).val();
    let postData = {
        email_id: approver,
        message: message
    };
    fetch("/servicedesk/citrix/" + requestid + "/submitforapproval", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(postData)
    })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            let result = data;
            if (result["code"] == 1) {
                location.reload();
            }
            else {
                message = null;
                if (result.error) { message = result.error }
                if (result.data) { message = result.data }
                document.getElementById("md_alert_content").innerText = message;
                document.getElementById("md__alert").removeAttribute("hidden", true)
            }
        })
        .catch(error => console.error(error));
};
function open_modal(clicked) {
    requestid = clicked.dataset.requestid
    $('#md_submit_for_approval_' + requestid).modal('show')
}
