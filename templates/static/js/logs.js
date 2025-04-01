/*
前端日志接口
@DEV JASON 2024.4.1
 */

// 向后端发送一个写入请求
export function send_log_data(message, mode) {
    fetch(`/front_end_log_interface/${message}/${mode}`, {
        method: 'GET',
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log(message);
            } else {
                console.log('CALL THE INTERFACE FAILED!');
            }
        })
        .catch(error => console.error('Error:', error));
}

