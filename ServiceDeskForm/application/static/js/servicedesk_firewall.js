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
    let tbl_firewall_rule = document.getElementById("tbl_firewall_rule");
    if (tbl_firewall_rule && tbl_firewall_rule.rows.length > 0) {
        for (let index = 1; index < tbl_firewall_rule.rows.length; index++) {
            let stt_cell = tbl_firewall_rule.rows[index].cells.item(0);
            value = '<span class="me-2 p-1" id="span-' + index + '">' + index + '</span>';
            stt_cell.innerHTML = value;
        }
    }
}
document.addEventListener("DOMContentLoaded", () => {
    SoThuTu();
});
// 2.2. Thêm form mới để nhập thông tin
function AddForm(clicked) {
    let requestid = clicked.dataset.requestid
    let tbl_firewall_rule = document.getElementById("tbl_firewall_rule");
    let ruleid = Math.random().toString(36).substring(2, 7);
    let objectid = Math.random().toString(36).substring(2, 7);

    let newform = `
    <form  id="row-${ruleid}" class="needs-validation" novalidate>
        <td>
          <span class="me-2 p-1" id="span-${ruleid}"></span>
        </td>
        <td>
          <div class="input-group">
            <input type="text" class="form-control form-control-sm data-edit" placeholder="Tên rule"
              id="name-${ruleid}" required>
          </div>
        </td>
        <!-- Source column -->
        <td>
          <div id="source-array-${ruleid}">
            <div class="input-group" id="input-group-source-${ruleid}-${objectid}">
              <input type="text" class="form-control form-control-sm data-edit" placeholder="Địa chỉ nguồn"
                id="input-source-${ruleid}-${objectid}"
                data-ruleid="${ruleid}" data-requestid="${requestid}" data-objectid="${objectid}"
                required>
              <div class="input-group-append">
                <button
                  class="btn btn-sm btn-md btn-outline-default m-0 px-2 py-1 z-depth-0 waves-effect"
                  type="button" id="btn-remove-source-${ruleid}-${objectid}"
                  data-ruleid="${ruleid}" data-requestid="${requestid}" data-objectid="${objectid}"
                  onclick="RemoveObjectRow(this,objectType='source',removedb=false)">X
                </button>
              </div>
            </div>
          </div>
          <!-- Add source -->
          <div class="d-grid">
            <button class="btn btn-sm" type="button" id="button-add-source-${ruleid}"
            data-ruleid="${ruleid}" data-requestid="${requestid}"
              onclick="AddObjectRow(this,objectType='source')">
              Thêm
            </button>
          </div>
        </td>
        <!-- Source column -->
        <!-- Destination column -->
        <td>
          <div id="destination-array-${ruleid}">
            <div class="input-group" id="input-group-destination-${ruleid}-${objectid}">
              <input type="text" class="form-control form-control-sm data-edit" placeholder="Địa chỉ đích"
                data-ruleid="${ruleid}" data-requestid="${requestid}" data-objectid="${objectid}"
                id="input-destination-${ruleid}-${objectid}" required>
              <div class="input-group-append">
                <button
                  class="btn btn-sm btn-md btn-outline-default m-0 px-2 py-1 z-depth-0 waves-effect"
                  type="button" id="btn-remove-destination-${ruleid}-${objectid}"
                  data-ruleid="${ruleid}" data-requestid="${requestid}" data-objectid="${objectid}"
                  onclick="RemoveObjectRow(this,objectType='destination',removedb=false)">
                  X
                </button>
              </div>
            </div>
          </div>
          <!-- Button Add Destination -->
          <div class="d-grid">
            <button class="btn btn-sm" type="button" id="button-add-destination-${ruleid}"
            data-ruleid="${ruleid}" data-requestid="${requestid}"
              onclick="AddObjectRow(this,objectType='destination')">
              Thêm
            </button>
          </div>
        </td>
        <!-- Destination Column -->
        <!-- Service Column -->
        <td>
          <div id="service-array-${ruleid}">
            <div class="input-group" id="input-group-service-${ruleid}-${objectid}">
              <input type="text" class="form-control form-control-sm data-edit" placeholder="Cổng"
                id="input-service-${ruleid}-${objectid}"
                data-ruleid="${ruleid}" data-requestid="${requestid}" data-objectid="${objectid}" required>
                <select class="browser-default custom-select custom-select-sm data-edit" id="slt-protocol-${ruleid}-${objectid}" data-ruleid="${ruleid}" data-requestid="${requestid}" data-objectid="${objectid}">
                    <option selected>Giao thức</option>
                    <option value="TCP">TCP</option>
                    <option value="UDP">UDP</option>
                    <option value="ICMP" disabled>ICMP</option>
                </select>

              <div class="input-group-append">
                <button
                  class="btn btn-sm btn-md btn-outline-default m-0 px-2 py-1 z-depth-0 waves-effect"
                  type="button" id="btn-remove-service-${ruleid}-${objectid}"
                  data-ruleid="${ruleid}" data-requestid="${requestid}" data-objectid="${objectid}"
                  onclick="RemoveObjectRow(this,objectType='service',removedb=false)">
                  X
                </button>
              </div>
            </div>
          </div>
          <!-- Button add Service -->
          <div class="d-grid">
            <button class="btn btn-sm" type="button" id="button-add-service-${ruleid}"
            data-ruleid="${ruleid}" data-requestid="${requestid}"
              onclick="AddObjectRow(this,objectType='service')">
              Thêm
            </button>
          </div>
        </td>
        <!-- Service Column -->
        <!-- Description Column -->
        <td>
          <textarea class="form-control form-control-sm" placeholder="Mô tả"
            id="description-${ruleid}"></textarea>
        </td>
        <!-- Description Column -->
        <!-- Functional Column -->
        <td>
          <!-- button save -->
          <button type="button" class="btn btn-outline-primary btn-sm waves-effect waves-light mt-0" id="btn-save-rule-${ruleid}" data-ruleid="${ruleid}" data-requestid="${requestid}" onclick="SaveRule(this)">
            Lưu
          </button>
          <!-- button remove -->
          <button type="button" class="btn btn-outline-danger btn-sm waves-effect waves-light mt-0" id="btn-remove-rule-${ruleid}" data-ruleid="${ruleid}" data-requestid="${requestid}"
            onclick="RemoveObjectRow(this,objectType='rule',removedb=false)">
            Xóa
          </button>
        </td>
        <!-- Functional Column -->
    `
    let newrow = tbl_firewall_rule.insertRow(tbl_firewall_rule.rows.length);
    newrow.innerHTML = newform;
    SoThuTu();

}
// 2.3. Thêm input cho các chột ip nguồn, ip đích, cổng

function AddObjectRow(clicked, objectType) {
    let requestid = clicked.dataset.requestid;
    let ruleid = clicked.dataset.ruleid;
    // let objectarray = document.getElementById(objectType + '-array-' + ruleid);
    let objectid = Math.random().toString(36).substring(2, 7);

    let placeholder = "";
    if (objectType == "service") {
        placeholder = "Cổng";
        const objectHtml = `
                <div class="input-group" id="input-group-${objectType}-${ruleid}-${objectid}">
                    <input type="text" class="form-control form-control-sm data-edit" placeholder="${placeholder}" 
                    id="input-${objectType}-${ruleid}-${objectid}" 
                    data-ruleid="${ruleid}" data-requestid="${requestid}" data-objectid="${objectid}" required>
                    <select class="browser-default custom-select custom-select-sm data-edit" id="slt-protocol-${ruleid}-${objectid}" data-ruleid="${ruleid}" data-requestid="${requestid}" data-objectid="${objectid}">
                        <option selected>Giao thức</option>
                        <option value="TCP">TCP</option>
                        <option value="UDP">UDP</option>
                        <option value="ICMP" disabled>ICMP</option>
                    </select>
                    <div class="input-group-append">
                    <button class="btn btn-sm btn-md btn-outline-default m-0 px-2 py-1 z-depth-0 waves-effect" type="button" 
                    id="btn-remove-${objectType}-${ruleid}-${objectid}" 
                    data-ruleid="${ruleid}" data-requestid="${requestid}" data-objectid="${objectid}" 
                    onclick="RemoveObjectRow(this,'${objectType}')">X</button>
                    </div>
                </div>
            `;
        $("#" + objectType + "-array-" + ruleid).append(objectHtml);
    }
    else {
        if (objectType == "destination") {
            placeholder = "Địa chỉ đích";
        }
        if (objectType == "source") {
            placeholder = "Địa chỉ nguồn";
        }
        const objectHtml = `
                <div class="input-group" id="input-group-${objectType}-${ruleid}-${objectid}">
                    <input type="text" class="form-control form-control-sm data-edit" placeholder="${placeholder}" 
                    id="input-${objectType}-${ruleid}-${objectid}" 
                    data-ruleid="${ruleid}" data-requestid="${requestid}" data-objectid="${objectid}" required>
                    <div class="input-group-append">
                    <button class="btn btn-sm btn-md btn-outline-default m-0 px-2 py-1 z-depth-0 waves-effect" type="button" 
                    id="btn-remove-${objectType}-${ruleid}-${objectid}" 
                    data-ruleid="${ruleid}" data-requestid="${requestid}" data-objectid="${objectid}" 
                    onclick="RemoveObjectRow(this,'${objectType}')">X</button>
                    </div>
                </div>
            `;
        $("#" + objectType + "-array-" + ruleid).append(objectHtml);
    }
}
// 2.4. Xóa một dòng trong bảng
function Delete_Table_Row(table_id, row_number) {
    document.getElementById(table_id).deleteRow(row_number);
}
// 2.5. Hàm chạy khi click nút xóa đối tượng và xóa dòng
function RemoveObjectRow(clicked, objectType, removedb = false) {
    let requestid = clicked.dataset.requestid;
    // Xóa một đối tượng
    if (objectType != "rule") {
        let ruleid = clicked.dataset.ruleid;
        let objectid = clicked.dataset.objectid;

        if (removedb == true) {
            let postData = {
                type: objectType,
                ruleid: parseInt(ruleid),
                objectid: parseInt(objectid)
            };
            fetch("/servicedesk/firewall/" + requestid, {
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
                        if (result.message) { message = result.message }
                        document.getElementById("alert_content").innerText = message;
                        document.getElementById("tbl_alert").removeAttribute("hidden", true)
                    }
                })
                .catch(error => console.error(error));
        }
        else {
            $("#input-group-"+objectType+"-"+ruleid+"-"+objectid).remove();
        }
    }
    // Xóa một rule
    if (objectType == 'rule') {
        const postData = {
            type: "rule",
            ruleid: clicked.dataset.ruleid
        };
        if (removedb == true) {
            fetch("/servicedesk/firewall/" + requestid, {
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
                        if (result.message) { message = result.message }
                        document.getElementById("alert_content").innerText = message;
                        document.getElementById("tbl_alert").removeAttribute("hidden", true)
                    }
                })
                .catch(error => console.error(error));
        }
        else {
            let tr = clicked.parentNode.parentNode;
            Delete_Table_Row("tbl_firewall_rule", tr.rowIndex);
            SoThuTu();
        }
    }
}
// 2.6. Hàm chạy khi click nút lưu rule mới
function SaveRule(clicked) {
    let requestid = clicked.dataset.requestid
    let ruleid = clicked.dataset.ruleid
    let name = $("#name-" + ruleid).val();
    let description = $("#description-" + ruleid).val();
    let sourceData = [];
    let destinationData = [];
    let serviceData = [];
    $("#source-array-" + ruleid + " input").each(function () {
        sourceData.push($(this).val());
    });
    $("#destination-array-" + ruleid + " input").each(function () {
        destinationData.push($(this).val());
    });
    $("#service-array-" + ruleid + " input").each(function () {
        let objectid = this.dataset.objectid
        serviceData.push(
            {
                "protocol": $("#slt-protocol-"+ruleid+"-"+objectid).val(),
                "port": parseInt($(this).val())
            }
        );
    });

    let postData = {
        name: name,
        source: sourceData,
        destination: destinationData,
        service: serviceData,
        description: description,
        requestid: requestid
    };
    fetch("/servicedesk/firewall/" + requestid, {
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
function EditRule(clicked) {
    // ẩn và hiện các trường thông tin
    let btn_edit = clicked;
    $("#row-" + btn_edit.dataset.ruleid + " td").each(function () {
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
};
// 2.8. Hàm chạy khi click nút cập nhật
function UpdateRule(clicked) {
    let requestid = clicked.dataset.requestid;
    let ruleid = clicked.dataset.ruleid;
    let sources = []
    let destinations = []
    let services = []
    let name = $("#name-" + ruleid).val();
    let description = $("#description-" + ruleid).val();
    $("#source-array-" + ruleid).children(".data-edit").each(function () {
        let object_id = $(this).data("objectid")
        let object_value = $("#input-source-" + ruleid + "-" + object_id).val();
        sources.push({
            objectid: parseInt(object_id),
            ruleid: parseInt(ruleid),
            value: object_value
        });
    });
    $("#destination-array-" + ruleid).children(".data-edit").each(function () {
        let object_id = $(this).data("objectid")
        let object_value = $("#input-destination-" + ruleid + "-" + object_id).val();
        destinations.push({
            objectid: parseInt(object_id),
            ruleid: parseInt(ruleid),
            value: object_value
        });
    });
    $("#service-array-" + ruleid).children(".data-edit").each(function () {
        let object_id = $(this).data("objectid")
        let port = $("#input-service-" + ruleid + "-" + object_id).val();
        let protocol = $("#slt-protocol-" + ruleid + "-" + object_id).val();
        services.push({
            objectid: parseInt(object_id),
            ruleid: parseInt(ruleid),
            value: parseInt(port),
            protocol: protocol
        });
    });
    postData = {
        name: name,
        sources: sources,
        destinations: destinations,
        services: services,
        description: description,
        ruleid: parseInt(ruleid)
    }
    fetch("/servicedesk/firewall/" + requestid, {
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
                if (result.message) { message = result.message }
                document.getElementById("alert_content").innerText = message;
                document.getElementById("tbl_alert").removeAttribute("hidden", true)
            }
        })
        .catch(error => console.error(error));
};
// 3. Submit for approval modal //

function submit_for_approval(clicked) {
    let requestid = clicked.dataset.requestid
    let approver = $("#md-slt-approver-" + requestid).val();
    let message = $("#md-textarea-message-" + requestid).val();
    let postData = {
        email_id: approver,
        message: message
    };
    fetch("/servicedesk/firewall/" + requestid + "/submitforapproval", {
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