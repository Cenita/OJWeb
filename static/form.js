function login_verify(url) {
    var username = $("#entry_name")
    var password = $("#entry_password")
    username.removeClass("btn-danger")
    password.removeClass("btn-danger")
    if(!username.val()){
        username.addClass("btn-danger");
        return false;
    }
    if(!password.val()){
        password.addClass("btn-danger");
        return false;
    }
    var form = new FormData(document.getElementById("entry_login"));
    $.post({
        url:url,
        data:form,
        dataType:'json',
        processData:false,
        contentType:false,
        success:function (data) {
            console.log(data)
            if(data.status==200){
                alert(data.message)
                if(data.message=="账号不存在"){
                    username.addClass("btn-danger");
                }else if(data.message=="密码错误"){
                    password.addClass("btn-danger");
                }
            }else if(data.status==400){
                window.location.href=data.message;
            }
        },
        error:function (data) {
            alert("服务器请求失败",data)
        }
    })
}

function regist_verify(url) {
    var username = $("#entry_name");
    var truename = $("#entry_trueName");
    var email = $("#entry_email");
    var password1 = $("#entry_password");
    var password2 = $("#entry_password_again");
    var port = $("#entry_registPort");
    username.removeClass("btn-danger");
    truename.removeClass("btn-danger");
    email.removeClass("btn-danger");
    password1.removeClass("btn-danger");
    password2.removeClass("btn-danger");
    port.removeClass("btn-danger");
    if(!username.val()){
        username.addClass("btn-danger");
        return false
    }
    if(!truename.val()){
        truename.addClass("btn-danger")
        return false
    }
    if(!email.val()){
        email.addClass("btn-danger")
        return false
    }
    if(email.val().search(/(.*)@(.*)com/i)===-1){
        email.addClass("btn-danger")
        return false
    }
    if(!password1.val()){
        password1.addClass("btn-danger")
        return false
    }
    if(!password2.val()){
        password2.addClass("btn-danger")
        return false
    }
    if(!port.val()){
        port.addClass("btn-danger")
        return false
    }
    if(password1.val()!=password2.val()){
        password1.addClass("btn-danger")
        password2.addClass("btn-danger")
        return false
    }
    var form = new FormData(document.getElementById("entry_regist"));
    $.post({
        url:url,
        data:form,
        dataType:'json',
        processData:false,
        contentType:false,
        success:function (data) {
            console.log(data)
            if(data.status==200){
                alert(data.message)
                if(data.message=="用户名已经存在"){
                    username.addClass("btn-danger");
                }else if(data.message=="两次密码不相等"){
                    password1.addClass("btn-danger");
                    password2.addClass("btn-danger");
                }else if(data.message=="邮箱已存在"){
                    email.addClass("btn-danger");
                }else if(data.message=="真实姓名已存在"){
                    truename.addClass("btn-danger");
                }else if(data.message=="注册码错误"){
                    port.addClass("btn-danger");
                }
            }else if(data.status==400){
                window.location.href=data.message;
            }else if(data.status==300){
                alert(data.message)
            }
        },
        error:function (data) {
            alert("服务器请求失败",data)
        }
    })
}
function code_verify() {
    var form = new FormData(document.getElementById("question_form"));
    $("#question_form").hide()
    $("#core").show()
    $("#code_content").text($("#question_form textarea").val())
    $.post({
        url:"",
        data:form,
        dataType:'json',
        processData:false,
        contentType:false,
        success:function (data) {
            if(data.status==200){
                $("#question_form").show()
                $("#core").hide()
                alert("提交错误 ， 错误原因："+data.content)
            }else if(data.status==400){
                window.location.href=data.content
            }
        },
        error:function (data) {
            alert("服务器请求错误",data)
        }
    })
}