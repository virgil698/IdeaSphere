    document.addEventListener('DOMContentLoaded', function() {
        const emojiButton = document.getElementById('emojiButton');
        const emojiPopup = document.getElementById('emojiPopup');
        const contentTextarea = document.getElementById('content');
        const emojis = document.querySelectorAll('.emoji');

        // 点击表情按钮显示/隐藏表情选择框
        emojiButton.addEventListener('click', function() {
            if (emojiPopup.style.display === 'none' || emojiPopup.style.display === '') {
                const buttonRect = emojiButton.getBoundingClientRect();
                emojiPopup.style.display = 'block';
                emojiPopup.style.top = buttonRect.top + 'px';
                emojiPopup.style.left = buttonRect.left - 250 + 'px';
            } else {
                emojiPopup.style.display = 'none';
            }
        });

        // 点击表情将其插入内容中
        emojis.forEach(function(emoji) {
            emoji.addEventListener('click', function() {
                const cursorPos = contentTextarea.selectionStart;
                const textBefore = contentTextarea.value.substring(0, cursorPos);
                const textAfter = contentTextarea.value.substring(cursorPos);

                contentTextarea.value = textBefore + emoji.innerText + textAfter;
                contentTextarea.focus();
                contentTextarea.selectionStart = cursorPos + emoji.innerText.length;
                contentTextarea.selectionEnd = cursorPos + emoji.innerText.length;

                emojiPopup.style.display = 'none';
            });
        });

        // 点击页面其他地方关闭表情选择框
        document.addEventListener('click', function(event) {
            if (!emojiButton.contains(event.target) && !emojiPopup.contains(event.target)) {
                emojiPopup.style.display = 'none';
            }
        });
    });