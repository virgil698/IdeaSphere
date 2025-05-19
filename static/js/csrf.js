/**
 * 获取CSRF Token
 * @returns {Promise<string>} CSRF Token
 */
async function getCSRFToken() {
    const response = await fetch('/api/csrf-token');
    const data = await response.json();
    return data.csrf_token;
}

/**
 * 设置CSRF Token到请求头
 * @param {string} csrfToken CSRF Token
 * @returns {Object} 包含CSRF Token的请求头
 */
function setCSRFTokenInHeader(csrfToken) {
    return {
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/json',
    };
}

// 将 getCSRFToken 函数暴露给全局作用域
window.getCSRFToken = getCSRFToken;