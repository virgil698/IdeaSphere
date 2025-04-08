/**
 * 搜索功能
 * @Dev virgil698
 * @StructRefactor Jason
 */

const searchInput = document.getElementById("searchInput");
const searchResultsPopup = document.getElementById("searchResultsPopup");
const searchResultsContent = document.getElementById(
    "searchResultsContent"
);

searchInput.addEventListener("input", function () {
    const query = this.value.trim();
    if (!query) {
        searchResultsPopup.style.display = "none";
        return;
    }

    // 发送 AJAX 请求到后端
    fetch(`/search/${encodeURIComponent(query)}`)
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                const results = data.results;
                searchResultsContent.innerHTML = results
                    .map((item) => {
                        // 统一处理两种结果类型
                        const content = item.keyword ? item.keyword : item.content;
                        const similarity = item.similarity.toFixed(2);
                        const source = item.source;
                        const postId = item.postId || '';

                        return `            <div class="search-result-item" data-post-id="${postId}">
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
document.addEventListener("click", function (event) {
    if (!event.target.closest(".search-box")) {
        searchResultsPopup.style.display = "none";
    }
});