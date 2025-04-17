document.addEventListener('DOMContentLoaded', function() {
    const followBtn = document.getElementById('followBtn');
    const followMenu = document.getElementById('followMenu');
    const unfollowBtn = document.getElementById('unfollowBtn');
    let followingUserId = null; // 假设这个变量会被正确设置为目标用户的ID

    // 获取 CSRF Token
    async function getCSRFToken() {
        try {
            const response = await fetch('/api/csrf-token'); // 确保 URL 与后端路由一致
            if (!response.ok) {
                throw new Error(`Failed to get CSRF Token: ${response.status}`);
            }
            const data = await response.json();
            return data.csrf_token;
        } catch (error) {
            console.error('Error getting CSRF Token:', error);
            throw error;
        }
    }

    // 关注用户
    async function followUser() {
        try {
            const csrfToken = await getCSRFToken();
            const response = await fetch(`/user/${followingUserId}/follow`, { // 确保 URL 与后端路由一致
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                credentials: 'include'
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.message === 'User followed successfully') {
                updateUIAfterFollow();
            } else {
                alert(data.message || 'Failed to follow user');
            }
        } catch (error) {
            console.error('Error following user:', error);
            alert('Failed to follow user. Please try again later.');
        }
    }

    // 取消关注用户
    async function unfollowUser() {
        try {
            const csrfToken = await getCSRFToken();
            const response = await fetch(`/user/${followingUserId}/unfollow`, { // 确保 URL 与后端路由一致
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                credentials: 'include'
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.message === 'User unfollowed successfully') {
                updateUIAfterUnfollow();
            } else {
                alert(data.message || 'Failed to unfollow user');
            }
        } catch (error) {
            console.error('Error unfollowing user:', error);
            alert('Failed to unfollow user. Please try again later.');
        }
    }

    // 更新UI为已关注状态
    function updateUIAfterFollow() {
        const followContainer = document.createElement('div');
        followContainer.className = 'follow-container';

        const followedBtn = document.createElement('button');
        followedBtn.id = 'followBtn';
        followedBtn.className = 'followed-btn';
        followedBtn.innerHTML = '<i class="fas fa-check"></i> 已关注';

        const menu = document.createElement('div');
        menu.id = 'followMenu';
        menu.className = 'follow-menu';

        const unfollowBtn = document.createElement('button');
        unfollowBtn.id = 'unfollowBtn';
        unfollowBtn.className = 'unfollow-btn';
        unfollowBtn.textContent = '取消关注';

        menu.appendChild(unfollowBtn);
        followContainer.appendChild(followedBtn);
        followContainer.appendChild(menu);

        followBtn.replaceWith(followContainer);

        document.getElementById('unfollowBtn').addEventListener('click', function() {
            showConfirmDialog();
        });
    }

    // 更新UI为关注状态
    function updateUIAfterUnfollow() {
        const newFollowBtn = document.createElement('button');
        newFollowBtn.id = 'followBtn';
        newFollowBtn.className = 'follow-btn';
        newFollowBtn.innerHTML = '<i class="fas fa-plus"></i> 关注';

        document.querySelector('.follow-container').replaceWith(newFollowBtn);

        newFollowBtn.addEventListener('click', function() {
            followUser();
        });
    }

    // 显示确认对话框
    function showConfirmDialog() {
        const confirmDialog = document.createElement('div');
        confirmDialog.className = 'confirm-dialog';
        confirmDialog.innerHTML = `
            <p>确定要取消关注该用户吗？</p>
            <div class="confirm-buttons">
                <button class="cancel-btn">取消</button>
                <button class="confirm-btn">确定</button>
            </div>
        `;

        document.body.appendChild(confirmDialog);

        confirmDialog.querySelector('.cancel-btn').addEventListener('click', function() {
            confirmDialog.style.display = 'none';
            document.body.removeChild(confirmDialog);
        });

        confirmDialog.querySelector('.confirm-btn').addEventListener('click', function() {
            unfollowUser();
            document.body.removeChild(confirmDialog);
        });
    }

    // 点击关注按钮
    if (followBtn) {
        followBtn.addEventListener('click', function() {
            if (followBtn.classList.contains('followed-btn')) {
                followMenu.style.display = followMenu.style.display === 'block' ? 'none' : 'block';
            } else {
                followUser();
            }
        });
    }

    // 点击取消关注按钮
    if (unfollowBtn) {
        unfollowBtn.addEventListener('click', function() {
            showConfirmDialog();
        });
    }

    // 点击其他地方关闭菜单
    document.addEventListener('click', function(event) {
        if (!followBtn.contains(event.target) && !followMenu.contains(event.target)) {
            followMenu.style.display = 'none';
        }
    });
});