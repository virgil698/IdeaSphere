document.addEventListener('DOMContentLoaded', function() {
    console.log("Emoji script loaded");
    
    // 确保元素存在再绑定事件
    const emojiButton = document.getElementById('emojiButton');
    const emojiPopup = document.getElementById('emojiPopup');
    const contentTextarea = document.getElementById('content');
    
    if (!emojiButton || !emojiPopup || !contentTextarea) {
        console.error("表情功能初始化失败：找不到必要的DOM元素", { 
            button: !!emojiButton, 
            popup: !!emojiPopup, 
            textarea: !!contentTextarea 
        });
        return;
    }
    
    console.log("表情功能元素已找到");
    const emojis = document.querySelectorAll('.emoji');
    const contentEditor = document.querySelector('.content-editor');

    // 点击表情按钮显示/隐藏表情选择框
    emojiButton.addEventListener('click', function(e) {
        console.log("表情按钮被点击");
        e.preventDefault();
        e.stopPropagation();
        
        if (emojiPopup.style.display === 'none' || emojiPopup.style.display === '') {
            // 显示表情弹窗 - 在content-editor下方
            console.log("显示表情弹窗");
            emojiPopup.style.display = 'block';
            
            // 直接定位在按钮下方
            const buttonRect = emojiButton.getBoundingClientRect();
            const editorRect = contentEditor.getBoundingClientRect();
            
            // 计算相对于编辑器的位置
            const topPosition = buttonRect.bottom - editorRect.top + 10;
            emojiPopup.style.top = topPosition + 'px';
            emojiPopup.style.left = '10px';
            emojiPopup.style.transform = 'none';
            
            // 添加显示动画效果
            setTimeout(() => {
                emojiPopup.style.opacity = '1';
            }, 10);
        } else {
            console.log("隐藏表情弹窗");
            hideEmojiPopup();
        }
    });

    // 隐藏表情弹窗的函数
    function hideEmojiPopup() {
        emojiPopup.style.opacity = '0';
        
        setTimeout(() => {
            emojiPopup.style.display = 'none';
        }, 200);
    }

    // 点击表情将其插入内容中
    emojis.forEach(function(emoji) {
        emoji.addEventListener('click', function(e) {
            console.log("表情被点击:", emoji.innerText);
            e.preventDefault();
            
            // 添加点击效果
            emoji.classList.add('emoji-selected');
            setTimeout(() => {
                emoji.classList.remove('emoji-selected');
            }, 300);
            
            const cursorPos = contentTextarea.selectionStart;
            const textBefore = contentTextarea.value.substring(0, cursorPos);
            const textAfter = contentTextarea.value.substring(cursorPos);

            contentTextarea.value = textBefore + emoji.innerText + textAfter;
            
            // 触发输入事件以激活任何可能的自动保存或验证
            contentTextarea.dispatchEvent(new Event('input'));
            
            // 设置焦点和光标位置
            contentTextarea.focus();
            contentTextarea.selectionStart = cursorPos + emoji.innerText.length;
            contentTextarea.selectionEnd = cursorPos + emoji.innerText.length;

            // 平滑关闭弹窗
            setTimeout(hideEmojiPopup, 100);
        });
    });

    // 点击页面其他地方关闭表情选择框
    document.addEventListener('click', function(event) {
        if (emojiPopup.style.display !== 'none' && 
            !emojiButton.contains(event.target) && 
            !emojiPopup.contains(event.target)) {
            console.log("点击页面其他位置，关闭表情弹窗");
            hideEmojiPopup();
        }
    });
    
    // ESC 键关闭弹窗
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && emojiPopup.style.display !== 'none') {
            console.log("按下ESC键，关闭表情弹窗");
            hideEmojiPopup();
        }
    });
    
    // 添加常用表情到内容区的快捷方式
    contentTextarea.addEventListener('keydown', function(e) {
        // 检测 : 后跟字符的组合
        if (e.key === ':' && e.ctrlKey) {
            console.log("触发表情快捷键");
            e.preventDefault();
            const emojiMap = {
                '1': '👍', '2': '😊', '3': '🎉', '4': '❤️', 
                '5': '🔥', '6': '👏', '7': '🤔', '8': '😎'
            };
            
            // 显示提示
            const notification = document.createElement('div');
            notification.className = 'emoji-shortcut-notification';
            notification.innerHTML = '按下数字键 1-8 可以快速插入常用表情';
            document.body.appendChild(notification);
            
            // 设置定时器移除提示
            setTimeout(() => {
                notification.style.opacity = '0';
                setTimeout(() => {
                    document.body.removeChild(notification);
                }, 500);
            }, 2000);
            
            // 监听数字键
            const keyHandler = function(ke) {
                if (emojiMap[ke.key]) {
                    ke.preventDefault();
                    
                    const cursorPos = contentTextarea.selectionStart;
                    const textBefore = contentTextarea.value.substring(0, cursorPos);
                    const textAfter = contentTextarea.value.substring(cursorPos);
                    
                    contentTextarea.value = textBefore + emojiMap[ke.key] + textAfter;
                    contentTextarea.selectionStart = cursorPos + emojiMap[ke.key].length;
                    contentTextarea.selectionEnd = cursorPos + emojiMap[ke.key].length;
                    
                    // 移除事件监听器
                    document.removeEventListener('keydown', keyHandler);
                } else if (ke.key === 'Escape') {
                    document.removeEventListener('keydown', keyHandler);
                }
            };
            
            document.addEventListener('keydown', keyHandler);
        }
    });
    
    // 给关闭按钮添加点击事件
    const closeButton = document.querySelector('.emoji-close-btn');
    if (closeButton) {
        closeButton.addEventListener('click', function(e) {
            console.log("关闭按钮被点击");
            e.preventDefault();
            e.stopPropagation();
            hideEmojiPopup();
        });
    }
    
    // 导出函数到全局作用域，使其可以从HTML中调用
    window.hideEmojiPopup = hideEmojiPopup;
    console.log("表情功能初始化完成");
});