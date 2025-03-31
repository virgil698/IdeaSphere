/**
 * 权限组
 * @Dev Jason
 */
async function getCSRFToken() {
    const response = await fetch('/api/csrf-token');
    const data = await response.json();
    return data.csrf_token;
}
/**
 * 向后端发送权限组进行合规性验证
 * @param user_id
 * @param user_perm
 * @param operation
 */

async function send_perm_data_to_backend(user_id, user_perm, operation) {
    const csrf = await getCSRFToken();
    if (user_id === '' || user_perm === '' || operation === '') {
        alert("内部错误");
    }
    const numericId = user_id.match(/\d+/)?.[0];
    // 发送请求
    fetch(`/perm_groups/${numericId}/${user_perm}/${operation}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf,
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                alert('权限组错误！')
            }
        })
        .catch(error => console.error('Error:', error));
}