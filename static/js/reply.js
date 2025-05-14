// 显示/隐藏回复框
function showReplyBox(commentId) {
    const replyForm = document.getElementById(`reply-form-${commentId}`);

    // 切换当前表单状态
    const isActive = replyForm.classList.contains('active');

    // 关闭所有其他回复框
    document.querySelectorAll('.reply-form').forEach(form => {
        form.classList.remove('active');
        form.style.maxHeight = null;
    });

    // 切换当前表单
    if (!isActive) {
        replyForm.classList.add('active');
        replyForm.style.maxHeight = replyForm.scrollHeight + "px";
        replyForm.querySelector('textarea').focus();
    } else {
        replyForm.style.maxHeight = null;
        replyForm.classList.remove('active');
    }

    // 添加过渡结束监听
    replyForm.addEventListener('transitionend', () => {
        if (!replyForm.classList.contains('active')) {
            replyForm.style.maxHeight = null;
        }
    }, { once: true });
}

// 提交回复
async function submitReply(event, commentId) {
    event.preventDefault();

    const form = event.target;
    const content = form.querySelector('textarea').value;

    if (!content.trim()) {
        alert('回复内容不能为空');
        return;
    }

    // 显示加载状态
    const submitButton = form.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;
    submitButton.textContent = '提交中...';
    submitButton.disabled = true;

    // 获取CSRF Token
    const csrfToken = await getCSRFToken();

    // 获取当前登录的用户名
    const userInfoDiv = document.getElementById('user-info');
    const userInfo = userInfoDiv.getAttribute('data-username');

    fetch('/api/comment/' + commentId + '/reply', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({content: content})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // 创建新的回复元素
            const repliesContainer = document.getElementById(`replies-${commentId}`);
            const replyElement = document.createElement('div');
            replyElement.className = 'reply mt-3';
            replyElement.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <h5 class="mt-0">${userInfo} 回复：</h5>
                    <span class="text-success">点赞: 0</span>
                </div>
                <div class="markdown-content">
                    ${content}
                </div>
                <meta name="csrf-token" content="${csrfToken}">
                <div class="d-flex justify-content-between align-items-center mt-2">
                    <a href="#" class="btn btn-success btn-sm">
                        <i class="fas fa-thumbs-up"></i> 点赞
                    </a>
                    <a href="#" class="btn btn-warning btn-sm">
                        <i class="fas fa-exclamation-triangle"></i> 举报回复
                    </a>
                </div>
            `;

            // 直接将回复添加到评论下方的 replies-container 中
            if (repliesContainer) {
                repliesContainer.appendChild(replyElement);
            }

            // 收起回复编辑框并清空内容
            form.style.maxHeight = null;
            form.classList.remove('active');

            // 恢复按钮状态
            submitButton.textContent = originalText;
            submitButton.disabled = false;

            alert('回复成功');
        } else {
            // 恢复按钮状态
            submitButton.textContent = originalText;
            submitButton.disabled = false;

            alert(data.message || '回复失败');
        }
    })
    .catch(error => {
        // 恢复按钮状态
        submitButton.textContent = originalText;
        submitButton.disabled = false;

        console.error('Error:', error);
        alert('回复失败，请检查控制台日志');
    });
}

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', function() {
    // 默认隐藏所有回复框
    const replyForms = document.querySelectorAll('.reply-form');
    replyForms.forEach(form => {
        form.classList.add('d-none');
    });

    // 为所有回复按钮添加点击事件
    const replyButtons = document.querySelectorAll('.reply-btn');
    replyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const commentId = this.getAttribute('data-comment-id');
            showReplyBox(commentId);
        });
    });
});
