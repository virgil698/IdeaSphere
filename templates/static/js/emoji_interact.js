/**
 * 表情交互功能
 * @Dev virgil698
 * @StructRefactor Jason
 */

document.addEventListener('DOMContentLoaded', () => {
    // 表情按钮交互
    const emojiBtn = document.getElementById('emojiButton');
    const emojiPopup = document.getElementById('emojiPopup');
    const textarea = document.getElementById('content');

    // 修改按钮点击处理
    emojiBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        emojiPopup.style.display = emojiPopup.style.display === 'block' ? 'none' : 'block';
        textarea.focus();
    });

    // 全局点击关闭
    document.addEventListener('click', (e) => {
        if (!emojiPopup.contains(e.target) && e.target !== emojiBtn) {
            emojiPopup.style.display = 'none';
        }
    });

    // 表情插入逻辑
    document.querySelectorAll('#emojiPopup .emoji').forEach(emoji => {
        emoji.addEventListener('click', (e) => {
            e.stopPropagation();
            const symbol = e.target.textContent;

            // 使用现代文本操作API
            textarea.setRangeText(
                symbol,
                textarea.selectionStart,
                textarea.selectionEnd,
                'end'
            );

            // 触发输入事件以兼容自动保存等功能
            const event = new Event('input', {bubbles: true});
            textarea.dispatchEvent(event);
        });
    });

    // 键盘交互增强
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && emojiPopup.style.display === 'block') {
            emojiPopup.style.display = 'none';
        }
    });
});