import {send_log_data} from './logs.js'
send_log_data("msg", "info")

document.addEventListener('DOMContentLoaded', function () {
    // 更新步骤指示器状态
    function updateStepsIndicator(currentStep) {
        const steps = ['step1-indicator', 'step2-indicator', 'step3-indicator'];
        steps.forEach(step => {
            document.getElementById(step).classList.remove('active');
        });
        document.getElementById(steps[currentStep - 1]).classList.add('active');
    }

    document.getElementById('nextToStep2').addEventListener('click', function () {
        document.getElementById('step1').style.display = 'none';
        document.getElementById('step2').style.display = 'block';
        updateStepsIndicator(2);
    });

    document.getElementById('prevToStep1').addEventListener('click', function () {
        document.getElementById('step2').style.display = 'none';
        document.getElementById('step1').style.display = 'block';
        updateStepsIndicator(1);
    });

    document.getElementById('nextToStep3').addEventListener('click', function () {
        document.getElementById('step2').style.display = 'none';
        document.getElementById('step3').style.display = 'block';
        updateStepsIndicator(3);
    });

    document.getElementById('prevToStep2').addEventListener('click', function () {
        document.getElementById('step3').style.display = 'none';
        document.getElementById('step2').style.display = 'block';
        updateStepsIndicator(2);
    });

    // 密码强度检测
    const passwordInput = document.getElementById('adminPassword');
    const passwordConfirmInput = document.getElementById('adminPasswordConfirm');
    const strengthText = document.getElementById('passwordStrengthText');
    const strengthMeter = document.getElementById('passwordStrengthMeter');

    passwordInput.addEventListener('input', function () {
        const password = passwordInput.value;
        let strength = 0;

        if (password.length >= 8) strength += 1;
        if (/[A-Z]/.test(password)) strength += 1;
        if (/[a-z]/.test(password)) strength += 1;
        if (/[0-9]/.test(password)) strength += 1;
        if (/[^A-Za-z0-9]/.test(password)) strength += 1;

        let strengthClass = '';
        let strengthTextContent = '';

        if (strength === 0 || strength === 1) {
            strengthClass = '';
            strengthTextContent = '密码强度：弱';
        } else if (strength === 2 || strength === 3) {
            strengthClass = 'medium';
            strengthTextContent = '密码强度：中';
        } else if (strength >= 4) {
            strengthClass = 'strong';
            strengthTextContent = '密码强度：强';
        }

        strengthMeter.className = 'strength-fill ' + strengthClass;
        strengthMeter.style.width = (strength * 20) + '%';
        strengthText.textContent = strengthTextContent;
    });

    document.getElementById('installForm').addEventListener('submit', function (e) {
        e.preventDefault();

        const username = document.getElementById('adminUsername').value;
        const password = document.getElementById('adminPassword').value;
        const passwordConfirm = document.getElementById('adminPasswordConfirm').value;

        if (password !== passwordConfirm) {
            alert('密码和确认密码不一致！');
            return;
        }

        if (!username || !password) {
            alert('请填写所有必填项！');
            return;
        }

        fetch('/install', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCSRFToken()
            },
            body: new URLSearchParams({
                'username': username,
                'password': password,
                'password_confirm': passwordConfirm,
                'step': '3'
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('安装成功！请使用管理员账户登录论坛。');
                    window.location.href = data.redirect;
                } else {
                    alert(data.message || '安装失败！');
                }
            })
            .catch(error => {
                console.error('安装过程中发生错误:', error);
                alert('安装过程中发生错误，请重试！');
            });
    });

    function getCSRFToken() {
        return document.querySelector('input[name="csrf_token"]').value;
    }
});