/**
 * 权限组
 * @Dev Jason
 */

/**
 * 向后端发送权限组进行合规性验证
 * @param user_id
 * @param user_perm
 * @param operation
 */

function send_perm_data_to_backend(user_id, user_perm, operation) {
    // 参数有效性检查
    if (!user_id || !user_perm || !operation) {
        alert("参数无效: user_id, user_perm 和 operation 都不能为空");
        return false;
    }

    // 发送请求
    fetch(`/perm_groups/${encodeURIComponent(user_id)}/${encodeURIComponent(user_perm)}/${encodeURIComponent(operation)}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id, user_perm, operation })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        // 根据实际情况处理成功的响应数据
    })
    .catch(error => {
        console.error('Error:', error.message);
        alert("请求失败，请稍后再试或联系管理员。");
    });
}