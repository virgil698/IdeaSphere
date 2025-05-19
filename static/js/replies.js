// 获取 CSRF Token
async function getCSRFToken() {
    const response = await fetch('/api/csrf-token');
    const data = await response.json();
    return data.csrf_token;
}

// 显示所有回复
document.addEventListener('DOMContentLoaded', function() {
    // 为所有"点击查看回复"按钮添加点击事件
    const viewAllRepliesBtns = document.querySelectorAll('.view-all-replies-btn');
    viewAllRepliesBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const commentId = this.getAttribute('data-comment-id');
            showAllReplies(commentId);
        });
    });
});

/**
 * 显示评论的所有回复
 * @param {number} commentId 评论ID
 */
async function showAllReplies(commentId) {
    try {
        // 获取CSRF Token
        const csrfToken = await getCSRFToken();

        // 获取所有回复数据
        const response = await fetch(`/api/comment/${commentId}/replies?page=1`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrfToken
            }
        });

        if (!response.ok) {
            throw new Error('请求失败');
        }

        const data = await response.json();

        // 渲染回复列表
        renderRepliesList(commentId, data, csrfToken); // 传递 csrfToken 给 renderRepliesList

        // 显示分页
        renderPagination(commentId, data);

        // 显示所有回复容器
        const allRepliesContainer = document.getElementById(`all-replies-${commentId}`);
        allRepliesContainer.style.display = 'block';

        // 隐藏"点击查看回复"按钮
        const viewAllBtn = document.querySelector(`.view-all-replies-btn[data-comment-id="${commentId}"]`);
        if (viewAllBtn) {
            viewAllBtn.style.display = 'none';
        }

    } catch (error) {
        console.error('加载评论回复失败:', error);
    }
}

/**
 * 渲染回复列表
 * @param {number} commentId 评论ID
 * @param {Object} data 回复数据
 * @param {string} csrfToken CSRF Token
 */
function renderRepliesList(commentId, data, csrfToken) {
    const repliesListContainer = document.getElementById(`replies-list-${commentId}`);
    if (!repliesListContainer) {
        console.error(`未找到评论ID为 ${commentId} 的回复列表容器`);
        return;
    }

    // 获取用户信息
    const userInfoElement = document.getElementById('user-info');
    const isAuthenticated = userInfoElement.getAttribute('data-is-authenticated') === 'true';

    repliesListContainer.innerHTML = ''; // 清空现有内容

    if (data.reply_list && data.reply_list.length > 0) {
        data.reply_list.forEach(reply => {
            const replyElement = document.createElement('div');
            replyElement.className = 'reply mt-3';
            replyElement.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <h5 class="mt-0">${reply.author} 回复：</h5>
                    <span class="text-success">点赞: ${reply.like_count || 0}</span>
                </div>
                <div class="markdown-content">
                    ${reply.content}
                </div>
                <meta name="csrf-token" content="${csrfToken}">
                <div class="d-flex justify-content-between align-items-center mt-2">
                    ${isAuthenticated ? `
                        <a href="#" class="btn btn-success btn-sm" onclick="incrementLikeReply('${reply.id}')">
                            <i class="fas fa-thumbs-up"></i> 点赞
                        </a>
                        <a href="#" class="btn btn-warning btn-sm" onclick="reportReply('${reply.id}')">
                            <i class="fas fa-exclamation-triangle"></i> 举报回复
                        </a>
                    ` : ''}
                </div>
            `;
            repliesListContainer.appendChild(replyElement);
        });
    } else {
        repliesListContainer.innerHTML = '<p class="text-muted">暂无回复</p>';
    }
}

/**
 * 渲染分页
 * @param {number} commentId 评论ID
 * @param {Object} data 分页数据
 */
function renderPagination(commentId, data) {
    const paginationContainer = document.getElementById(`pagination-${commentId}`);
    if (!paginationContainer) {
        console.error(`未找到评论ID为 ${commentId} 的分页容器`);
        return;
    }

    paginationContainer.innerHTML = '';

    if (data.pages > 1) {
        const prevLink = data.has_prev ? `
            <a href="javascript:void(0)" class="page-link prev-page-btn" data-comment-id="${commentId}" data-page="${data.prev_num}">
                <i class="fas fa-chevron-left"></i> 上一页
            </a>
        ` : '';

        const nextLink = data.has_next ? `
            <a href="javascript:void(0)" class="page-link next-page-btn" data-comment-id="${commentId}" data-page="${data.next_num}">
                下一页 <i class="fas fa-chevron-right"></i>
            </a>
        ` : '';

        paginationContainer.innerHTML = `
            <div class="pagination">
                ${prevLink}
                <span class="page-info">${data.page} / ${data.pages}</span>
                ${nextLink}
            </div>
        `;

        // 为分页按钮添加点击事件
        const prevBtn = paginationContainer.querySelector('.prev-page-btn');
        if (prevBtn) {
            prevBtn.addEventListener('click', function() {
                loadRepliesByPage(commentId, parseInt(this.getAttribute('data-page')));
            });
        }

        const nextBtn = paginationContainer.querySelector('.next-page-btn');
        if (nextBtn) {
            nextBtn.addEventListener('click', function() {
                loadRepliesByPage(commentId, parseInt(this.getAttribute('data-page')));
            });
        }
    }
}

/**
 * 按页加载回复
 * @param {number} commentId 评论ID
 * @param {number} page 页码
 */
async function loadRepliesByPage(commentId, page) {
    try {
        // 获取CSRF Token
        const csrfToken = await getCSRFToken();

        // 获取指定页的回复数据
        const response = await fetch(`/api/comment/${commentId}/replies?page=${page}`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrfToken
            }
        });

        if (!response.ok) {
            throw new Error('请求失败');
        }

        const data = await response.json();

        // 渲染回复列表
        renderRepliesList(commentId, data);

        // 更新分页
        renderPagination(commentId, data);

    } catch (error) {
        console.error('加载评论回复失败:', error);
    }
}