/**
 * 前端ICENTER登陆处理
 * @DEV JASON
 */
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new URLSearchParams(new FormData(e.target));
    const errorDiv = document.getElementById('errorMsg');
    errorDiv.textContent = '';

    try {
        const response = await fetch('/icenter_login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData,
            credentials: 'include'
        });

        // 处理重定向
        if (response.redirected) {
            window.location.href = response.url;
            return;
        }

        const data = await response.json();
        
        if (data.success) {
            window.location.href = data.redirectUrl || '/';
        } else {
            errorDiv.textContent = data.message || '登录失败';
        }
    } catch (error) {
        errorDiv.textContent = '请求失败: ' + error.message;
    }
});