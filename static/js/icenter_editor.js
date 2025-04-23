/**
 * ICENTER编辑器
 * @DEV JASON
 */

async function getCSRFToken() {
    const response = await fetch('/api/csrf-token');
    const data = await response.json();
    return data.csrf_token;
}

/**
 * 构建可视化目录树
 */
function build_tree(tree_object) {
    // 清空现有内容
    const container = document.getElementById('file-tree-container');
    container.innerHTML = '';

    // 递归创建树节点（修复缩进问题）
    const createTreeElement = (node, depth = 0) => {
        const nodeDiv = document.createElement('div');
        nodeDiv.style.marginLeft = depth * 15 + 'px'; // 根据层级动态缩进

        // 图标和名称
        const icon = document.createElement('span');
        icon.innerHTML = node.type === 'directory' ? '📁' : '📄';
        icon.style.cursor = 'pointer';
        icon.className = 'file-tree-icon';

        const nameSpan = document.createElement('span');
        nameSpan.textContent = node.name;
        nameSpan.className = `file-tree-node ${node.type}`;
        nameSpan.style.marginLeft = '5px';
        nameSpan.style.userSelect = 'none';

        // 目录样式
        if (node.type === 'directory') {
            const arrow = document.createElement('span');
            arrow.className = 'file-tree-arrow';
            arrow.textContent = '▼';
            nameSpan.insertAdjacentElement('afterbegin', arrow);
        }

        if (node.type === 'file') {
            nameSpan.style.cursor = 'pointer';
            nameSpan.addEventListener('click', async (e) => {
                e.stopPropagation(); // 阻止事件冒泡
                handleFileClick(node); // 执行自定义文件处理
            });
        }

        nodeDiv.append(icon, nameSpan);

        // 处理子节点
        if (node.children?.length) {
            const childList = document.createElement('ul');
            childList.style.listStyle = 'none';
            childList.style.paddingLeft = '0'; // 移除固定缩进

            node.children.sort((a, b) => {
                if (a.type === b.type) {
                    return a.name.localeCompare(b.name)
                }
                return a.type === 'directory' ? -1 : 1
            })
                .forEach(child => {
                    const li = document.createElement('li')
                    li.appendChild(createTreeElement(child, depth + 1))
                    childList.appendChild(li)
                })

            nodeDiv.appendChild(childList);
        }

        return nodeDiv;
    };

    container.appendChild(createTreeElement(tree_object));

    // 展开/折叠功能（修复选择器）
    container.addEventListener('click', (e) => {
        const arrow = e.target.closest('.file-tree-node.directory')?.querySelector('.file-tree-arrow');
        if (arrow) {
            const ul = arrow.closest('div').querySelector('ul');
            if (ul) {
                const isCollapsed = ul.style.display === 'none';
                ul.style.display = isCollapsed ? 'block' : 'none';
                arrow.textContent = isCollapsed ? '▼' : '▶';
            }
        }
    });
}


async function handleFileClick(fileNode) {
    try {
        const csrfToken = await getCSRFToken();
        const response = await fetch('/get_file_content', {
            method: 'POST',
            headers: {
                'X-CSRF-Token': csrfToken,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                filename: fileNode.name,
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const ext = fileNode.name.split('.').pop();
                    buildEditor(data.content, ext, fileNode.name); // 传递文件扩展名
                }
            })
    } catch (e) {
        showError(`网络请求失败: ${e.message}`)
        throw e
    }
}

/**
 * 初始化编辑器
 */
document.addEventListener('DOMContentLoaded', async () => {
    // 动态添加样式
    const style = document.createElement('style');
    style.textContent = `
        #file-tree {
            font-family: 'Consolas', monospace;
            font-size: 14px;
        }
        #file-tree span.directory {
            cursor: pointer;
            transition: background 0.2s;
        }
        #file-tree span.directory:hover {
            background: #f5f5f5;
        }
        #file-tree span.file {
            color: #666;
        }
        .arrow {
            display: inline-block;
            width: 15px;
        }
    `;
    document.head.appendChild(style);

    // 获取目录数据
    try {
        const csrfToken = await getCSRFToken();
        const response = await fetch('/directory_tree_api', {
            method: 'GET',
            headers: {
                'X-CSRF-Token': csrfToken,
                'Content-Type': 'application/json',
            }
        });

        const data = await response.json();
        if (data.success) {
            build_tree(data.tree);
        } else {
            showError(data.error || '未知错误');
        }
    } catch (error) {
        showError(`网络请求失败: ${error.message}`);
    }
});

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.style.color = '#ff4444';
    errorDiv.style.padding = '10px';
    errorDiv.textContent = `错误：${message}`;
    document.body.prepend(errorDiv);
    console.error('Error:', message);
}


async function buildEditor(code, fileExt, fileName) {
    if (!fileName) {
        fileName = prompt('请输入文件名') || `newfile.${lang}`;
    }
    const pos_to_editor_main = document.getElementById('editor-main');
    pos_to_editor_main.innerHTML = '';
    // 根据扩展名设置语言
    const languages = {
        js: 'javascript',
        py: 'python',
        html: 'html',
        css: 'css'
    };
    const lang = languages[fileExt] || 'plaintext';
    // 创建容器和工具栏
    const container = document.createElement('div');
    container.className = 'editor-container';

    // 添加工具栏
    const toolbar = document.createElement('div');
    toolbar.className = 'editor-toolbar';
    const saveBtn = document.createElement('button');
    saveBtn.textContent = '💾 保存';
    toolbar.appendChild(saveBtn);
    container.appendChild(toolbar);

    // 创建编辑区域
    const editorWrapper = document.createElement('div');
    editorWrapper.className = 'editor-wrapper';

    // 初始化数据
    let allLines = code ? code.split(/\r?\n/) : [];
    let modifiedLines = [...allLines];
    const pageSize = 100;
    let isLoading = false;
    let loadedLines = new Set(); // 新增：记录已加载行号
    let lastScrollPos = 0; // 新增：记录上次滚动位置

    // 创建编辑元素（添加行标识）
    const createEditorLine = (index, content) => {
        const lineDiv = document.createElement('div');
        lineDiv.className = 'editor-line';

        // 行号保持不变
        const lineNumber = document.createElement('span');
        lineNumber.className = 'line-number';
        lineNumber.textContent = index + 1;

        // 替换为支持高亮的代码块
        const codeContainer = document.createElement('div');
        codeContainer.className = 'code-container';

        const pre = document.createElement('pre');
        const codeElem = document.createElement('code');
        codeElem.className = `language-${lang}`;
        codeElem.textContent = content;
        codeElem.contentEditable = true; // 保持可编辑

        // 添加高亮
        hljs.highlightElement(codeElem);

        // 输入事件处理
        codeElem.addEventListener('input', (e) => {
            modifiedLines[index] = e.target.textContent;
            // 输入后重新高亮
            hljs.highlightElement(codeElem);
        });

        pre.appendChild(codeElem);
        codeContainer.appendChild(pre);
        lineDiv.append(lineNumber, codeContainer);

        return lineDiv;
    };

    // 添加CSS样式（追加到已有样式中）
    const highlightStyle = `        .hljs{background:#f8f8f8;padding:0.3em}
        .code-container {flex-grow:1}
        .editor-line {
            display: flex;
            margin: 2px 0;
            align-items: start;
        }
        pre {
            margin:0;
            padding:0;
            background:none !important;
        }
        code {
            white-space: pre-wrap;
            display: block;
            padding-left: 5px;
        }
    `;
    document.head.querySelector('style').textContent += highlightStyle;

    // 改进的加载函数（增量加载）
    const loadLines = (start, end) => {
        const fragment = document.createDocumentFragment();
        for (let i = start; i < end; i++) {
            if (i >= modifiedLines.length) break;
            if (!loadedLines.has(i)) {
                fragment.appendChild(createEditorLine(i, modifiedLines[i]));
                loadedLines.add(i);
            }
        }
        editorWrapper.appendChild(fragment);
    };

    // 保存功能（保持不变）
    saveBtn.addEventListener('click', async () => {
        try {
            const csrfToken = await getCSRFToken();
            const response = await fetch('/save_file', {
                method: 'POST',
                headers: {
                    'X-CSRF-Token': csrfToken,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    content: modifiedLines.join('\n'),
                    filename: fileName || 'untitled'
                })
            });
            // console.log(modifiedLines.join('\n'))
            // console.log(fileName)
            const result = await response.json();
            if (result.success) {
                alert('保存成功');
                allLines = [...modifiedLines];
            }
        } catch (e) {
            showError(`保存失败: ${e.message}`);
        }
    });

    // 改进的滚动处理逻辑
    let currentStart = 0;
    const handleScroll = () => {
        if (isLoading) return;

        const {scrollTop, scrollHeight, clientHeight} = editorWrapper;
        const scrollDirection = scrollTop > lastScrollPos ? 'down' : 'up';
        lastScrollPos = scrollTop;

        // 向下滚动加载
        if (scrollDirection === 'down' && (scrollTop + clientHeight >= scrollHeight - 100)) {
            isLoading = true;
            const newEnd = Math.min(currentStart + pageSize, allLines.length);
            loadLines(currentStart, newEnd);
            currentStart = newEnd;
            isLoading = false;
        }
        // 向上滚动加载
        else if (scrollDirection === 'up' && scrollTop <= 100) {
            isLoading = true;
            const newStart = Math.max(0, currentStart - pageSize * 2);
            loadLines(newStart, currentStart);
            currentStart = newStart;
            isLoading = false;
        }
    };

    // 初始化加载
    loadLines(0, pageSize);
    currentStart = pageSize;

    // 添加滚动事件
    editorWrapper.addEventListener('scroll', handleScroll);
    container.appendChild(editorWrapper);
    pos_to_editor_main.appendChild(container);
}
