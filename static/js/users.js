function upgradeUser(userId) {
    if (confirm('确定要提升该用户为版主吗？')) {
        window.location.href = '/upgrade_user/' + userId;
    }
}

function downgradeUser(userId) {
    if (confirm('确定要降级该用户为普通用户吗？')) {
        window.location.href = '/downgrade_user/' + userId;
    }
}