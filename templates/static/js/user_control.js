/**
 * 用户操作
 */

// 定义点赞函数
function incrementLike(postId) {
    fetch(`/like_post/${postId}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token() }}',
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // 更新点赞计数
                const likeCountElement = document.querySelector('.like-count');
                likeCountElement.textContent = `点赞: ${data.like_count}`;
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Error:', error));
}

// 定义举报帖子函数
function reportPost(postId) {
    const reason = prompt('请输入举报原因');
    if (!reason) {
        alert('举报原因不能为空');
        return;
    }

    fetch(`/report_post/${postId}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token() }}',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ reason })
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

// 定义评论点赞函数
function incrementLikeComment(commentId) {
    fetch(`/like_comment/${commentId}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token() }}',
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // 更新评论的点赞计数
                const likeCountElement = document.querySelector(`.comment-like-count-${commentId}`);
                likeCountElement.textContent = `点赞: ${data.like_count}`;
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Error:', error));
}

// 定义举报评论函数
function reportComment(commentId) {
    const reason = prompt('请输入举报原因');
    if (!reason) {
        alert('举报原因不能为空');
        return;
    }

    fetch(`/report_comment/${commentId}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token() }}',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ reason })
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

let cig_id = document.getElementById("comment-input-group");
let comment_id = document.getElementById("comment");
function comment_input_animation() {
    cig_id.classList.add("a");
    comment_id.classList.add("a");
}

function Rcomment_input_animation() {
    cig_id.classList.remove("a");
    comment_id.classList.remove("a");
}