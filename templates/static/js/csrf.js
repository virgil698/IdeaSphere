/**
 * 获取CSRF Token
 * @returns {Promise<string>} CSRF Token
 */
import {send_log_data} from './logs.js'
send_log_data("msg", "info")

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

window.getCSRFToken = getCSRFToken;