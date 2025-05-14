// 页面加载时获取并渲染所有评论的回复
document.addEventListener('DOMContentLoaded', function() {
    // 获取所有评论容器
    const comments = document.querySelectorAll('.media');

    // 遍历每个评论并获取其回复
    comments.forEach(comment => {
        const commentId = comment.querySelector('.reply-btn').getAttribute('data-comment-id');
        loadAndRenderReplies(commentId);
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

/**
 * 获取并渲染指定评论的回复
 * @param {number} commentId 评论的ID
 */
async function loadAndRenderReplies(commentId) {
    try {
        // 获取CSRF Token
        const csrfToken = await getCSRFToken();

        // 获取回复数据
        const response = await fetch(`/api/comment/${commentId}/replies`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrfToken
            }
        });

        if (!response.ok) {
            throw new Error('请求失败');
        }

        const data = await response.json();
        const replies = data.reply_list;

        // 渲染回复
        renderReplies(commentId, replies);

    } catch (error) {
        console.error('加载评论回复失败:', error);
    }
}

/**
 * 渲染评论回复
 * @param {number} commentId 评论ID
 * @param {Array} replies 回复数据数组
 */
function renderReplies(commentId, replies) {
    const repliesContainer = document.getElementById(`replies-${commentId}`);

    if (!repliesContainer) {
        console.error(`未找到评论ID为 ${commentId} 的回复容器`);
        return;
    }

    repliesContainer.innerHTML = ''; // 清空现有内容

    if (replies && replies.length > 0) {
        replies.forEach(reply => {
            const replyElement = document.createElement('div');
            replyElement.className = 'reply mt-3';
            replyElement.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <h5 class="mt-0">${reply.author} 回复：</h5>
                    <span class="text-success">点赞: ${reply.like_count || 0}</span>
                </div>
                <div class="markdown-content">
                    ${reply.reply_message}
                </div>
                <meta name="csrf-token" content="${reply.csrf_token}">
                <div class="d-flex justify-content-between align-items-center mt-2">
                    <a href="#" class="btn btn-success btn-sm" onclick="incrementLikeReply('${reply.id}')">
                        <i class="fas fa-thumbs-up"></i> 点赞
                    </a>
                    <a href="#" class="btn btn-warning btn-sm" onclick="reportReply('${reply.id}')">
                        <i class="fas fa-exclamation-triangle"></i> 举报回复
                    </a>
                </div>
            `;
            repliesContainer.appendChild(replyElement);
        });
    } else {
        repliesContainer.innerHTML = '<p class="text-muted">暂无回复</p>';
    }
}