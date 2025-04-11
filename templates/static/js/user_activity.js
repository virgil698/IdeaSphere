document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('activityHeatmap').getContext('2d');

    // 模拟活动数据
    const activityData = [
        { x: 1, y: 2, count: 1 },
        { x: 2, y: 3, count: 2 },
        { x: 3, y: 4, count: 3 },
        { x: 4, y: 5, count: 4 },
        { x: 5, y: 6, count: 5 },
        { x: 6, y: 7, count: 4 },
        { x: 7, y: 8, count: 3 },
        { x: 8, y: 9, count: 2 },
        { x: 9, y: 10, count: 1 },
        { x: 10, y: 11, count: 2 },
        { x: 11, y: 12, count: 3 },
        { x: 12, y: 13, count: 4 },
        { x: 13, y: 14, count: 5 },
        { x: 14, y: 15, count: 4 },
        { x: 15, y: 16, count: 3 },
        { x: 16, y: 17, count: 2 },
        { x: 17, y: 18, count: 1 },
        { x: 18, y: 19, count: 2 },
        { x: 19, y: 20, count: 3 },
        { x: 20, y: 21, count: 4 },
        { x: 21, y: 22, count: 5 }
    ];

    // 创建热图
    const heatmap = new Chart(ctx, {
        type: 'bubble',
        data: {
            datasets: [{
                label: '活动热图',
                data: activityData,
                backgroundColor: function(context) {
                    const count = context.dataset.data[context.dataIndex].count;
                    return `rgba(0, 255, 0, ${count * 0.2})`;
                },
                hoverBackgroundColor: function(context) {
                    const count = context.dataset.data[context.dataIndex].count;
                    return `rgba(0, 255, 0, ${count * 0.3})`;
                }
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    min: 0,
                    max: 22,
                    title: {
                        display: true,
                        text: '日期'
                    }
                },
                y: {
                    min: 0,
                    max: 22,
                    title: {
                        display: true,
                        text: '活动强度'
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `活动强度: ${context.raw.count}`;
                        }
                    }
                }
            }
        }
    });
});