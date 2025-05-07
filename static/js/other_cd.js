document.addEventListener('DOMContentLoaded', function() {
    const hamburgerMenu = document.querySelector('.hamburger-menu');
    const sidebar = document.querySelector('.sidebar');

    hamburgerMenu.addEventListener('click', function() {
        sidebar.classList.toggle('active');
    });

    // 点击页面其他区域时关闭侧边菜单
    document.addEventListener('click', function(event) {
        if (!sidebar.contains(event.target) && !hamburgerMenu.contains(event.target)) {
            sidebar.classList.remove('active');
        }
    });
});