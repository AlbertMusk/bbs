
$(function () {
    $('#captcha-button').click(function (event) {
        event.preventDefault();
        var email = $("input[name=email]").val();
        if(!email){
            zlalert.alertInfoToast('请输入邮箱');
            return;
        }

        zlajax.get({
           'url': '/cms/email_captcha',
           'data': {
               'email': email
           } ,
            'success': function (data) {
                if(data['code'] == 200){
                    zlalert.alertSuccessToast('验证码发送成功')
                }else{
                    zlalert.alertInfo(data['message'])
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError();
            }
        });

    });
});

$(function () {
    $('#submit').click(function (event) {
        event.preventDefault();
        var emailE = $("input[name='email']");
        var captchaE = $("input[name='captcha']");

        var email = emailE.val();
        var captcha = captchaE.val();

        zlajax.post({
            'url': '/cms/resetemail/',
            'data': {
                'email': email,
                'captcha': captcha
            },
            'success': function (data) {
                 if(data['code'] == 200){
                     zlalert.alertSuccessToast('邮箱更改成功');
                 }else{
                     zlalert.alertInfo(data['message'])
                 }
            },
            'fail': function (error) {
                zlalert.alertNetworkError();
            }
        })
    });
});