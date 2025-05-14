function showReplyBox(commentId) {
    const replyForm = document.getElementById(`reply-form-${commentId}`);
    const repliesContainer = document.getElementById(`replies-${commentId}`);

    if (replyForm.classList.contains('d-none')) {
        // 如果没有其他回复表单显示，则显示当前表单
        replyForm.classList.remove('d-none');
        replyForm.querySelector('textarea').focus();
    } else {
        // 如果当前表单已显示，则隐藏它
        replyForm.classList.add('d-none');
    }

    // 隐藏同级评论的回复表单
    const otherReplyForms = document.querySelectorAll('.reply-form:not(#reply-form-' + commentId + ')');
    otherReplyForms.forEach(form => {
        form.classList.add('d-none');
    });
}

function submitReply(event, commentId) {
    event.preventDefault();

    const form = event.target;
    const content = form.querySelector('textarea').value;

    if (!content.trim()) {
        alert('回复内容不能为空');
        return;
    }

    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

    fetch('/api/comment/' + commentId + '/reply', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            content: content
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert('回复成功');
            const repliesContainer = document.getElementById(`replies-${commentId}`);

            const replyElement = document.createElement('div');
            replyElement.className = 'reply mt-3';
            replyElement.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <h5 class="mt-0">${g.user.username} 回复：</h5>
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

            // 将回复添加到评论下方
            repliesContainer.insertBefore(replyElement, form);

            // 隐藏回复表单并清空内容
            form.classList.add('d-none');
            form.querySelector('textarea').value = '';
        } else {
            alert(data.message || '回复失败');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('回复失败，请检查控制台日志');
    });
}