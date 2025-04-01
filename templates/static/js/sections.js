 function confirmDeleteSection(sectionId, sectionName) {
        if (confirm(`确定要删除版块"${sectionName}"吗？此操作不可恢复。`)) {
            // 创建一个表单并提交
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = `/admin/delete_section/${sectionId}`;

            // 添加CSRF令牌
            const csrfToken = document.createElement('input');
            csrfToken.type = 'hidden';
            csrfToken.name = 'csrf_token';
            csrfToken.value = '{{ csrf_token() }}';
            form.appendChild(csrfToken);

            document.body.appendChild(form);
            form.submit();
        }
    }