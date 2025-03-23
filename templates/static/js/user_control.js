function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

function incrementLike(postId) {
    fetch(`/api/like_post/${postId}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.querySelector('.like-count').textContent = `点赞: ${data.like_count}`;
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}

function incrementLikeComment(commentId) {
    fetch(`/api/like_comment/${commentId}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.querySelector('.comment-like-count').textContent = `点赞: ${data.like_count}`;
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}

function reportPost(postId) {
    const reason = prompt('请输入举报原因：');
    if (reason) {
        fetch(`/api/report_post/${postId}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ reason: reason })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

function reportComment(commentId) {
    const reason = prompt('请输入举报原因：');
    if (reason) {
        fetch(`/api/report_comment/${commentId}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ reason: reason })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

function sendComment(postId) {
    const content = document.getElementById('comment').value;
    if (content.trim() === '') {
        alert('评论内容不能为空');
        return;
    }

    fetch(`/api/create_comment/${postId}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ content: content })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('comment').value = '';
            location.reload(); // 刷新页面以更新评论列表
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}

// 添加缺少的函数
function comment_input_animation() {
    // 这里可以添加评论输入框的动画效果
    console.log('评论输入框鼠标悬停动画');
}

function Rcomment_input_animation() {
    // 这里可以添加评论输入框的动画效果
    console.log('评论输入框鼠标离开动画');
}