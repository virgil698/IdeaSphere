/**
 * 搜索功能
 * @Dev virgil698
 * @StructRefactor Jason
 */

const searchInput = document.getElementById("searchInput");
const searchResultsPopup = document.getElementById("searchResultsPopup");
const searchResultsContent = document.getElementById("searchResultsContent");

searchInput.addEventListener("input", function () {
    const query = this.value.trim();
    if (!query) {
        searchResultsPopup.style.display = "none";
        return;
    }

    // 发送 AJAX 请求到后端
    fetch(`/api/search?keyword=${encodeURIComponent(query)}`)
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                const results = data.results;
                searchResultsContent.innerHTML = results
                    .map((item) => {
                        const content = item.content;
                        const similarity = item.similarity.toFixed(2);
                        const source = item.source;
                        const postId = item.postId || '';
                        return `
                            <div class="search-result-item" data-post-id="${postId}">
                                <strong>${source}</strong><br>
                                ${content} (${similarity} 相似度)
                            </div>
                        `;
                    })
                    .join('');
                searchResultsPopup.style.display = "block";
            } else {
                searchResultsContent.innerHTML = "<div>未找到相关结果</div>";
                searchResultsPopup.style.display = "block";
            }
        })
        .catch((error) => {
            console.error("搜索失败:", error);
            searchResultsContent.innerHTML = "<div>搜索失败，请稍后重试</div>";
            searchResultsPopup.style.display = "block";
        });
});

// 点击搜索结果项
searchResultsContent.addEventListener("click", function (event) {
    const target = event.target.closest(".search-result-item");
    if (target) {
        const postId = target.dataset.postId;
        if (postId) {
            // 跳转到帖子页面
            window.location.href = `/post/${postId}`;
        }
    }
});

// 点击外部关闭弹窗
document.addEventListener('DOMContentLoaded', function() {
    // 检查是否是第一次访问
    const hasVisited = sessionStorage.getItem('hasVisited');

    if (!hasVisited) {
        // 如果是第一次访问，显示加载动画
        const loaderWrapper = document.getElementById('loaderWrapper');
        loaderWrapper.classList.add('visible');

        // 页面加载完成后2秒后隐藏加载动画
        window.addEventListener('load', function() {
            setTimeout(function() {
                loaderWrapper.classList.remove('visible');
                // 标记为已访问
                sessionStorage.setItem('hasVisited', 'true');
            }, 2000);
        });
    } else {
        // 如果不是第一次访问，直接隐藏加载动画
        const loaderWrapper = document.getElementById('loaderWrapper');
        loaderWrapper.classList.remove('visible');
    }

    // 获取按钮元素
    const backToTopButton = document.getElementById('backToTop');

    // 检测滚动事件
    window.addEventListener('scroll', () => {
        // 如果页面滚动超过100px，显示按钮
        if (window.pageYOffset > 100) {
            backToTopButton.classList.add('visible');
        } else {
            backToTopButton.classList.remove('visible');
        }
    });

    // 点击按钮返回顶部
    backToTopButton.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // 点击搜索按钮跳转到搜索结果页面
    document.getElementById('searchButton').addEventListener('click', function() {
        const query = document.getElementById('searchInput').value.trim();
        if (query) {
            window.location.href = `/search?keyword=${encodeURIComponent(query)}`;
        }
    });
});