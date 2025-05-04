/**
 * 举报功能
 * @Dev virgil698
 * @StructRefactor Jason
 */
window.handleReport = async function (reportId, status) {
    if (status !== 'valid' && status !== 'invalid') {
        alert('处理失败：无效的状态值');
        return;
    }
    if (confirm('确定要处理该举报吗？')) {
        const csrfToken = await getCSRFToken();
        fetch(`/handle_report/${reportId}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: status })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                location.reload(); // 刷新页面以更新举报状态
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }
}