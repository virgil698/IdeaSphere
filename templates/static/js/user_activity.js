document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('activityHeatmap').getContext('2d');

    // 模拟活动数据 - 实际应用中应该从API获取
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

    // 获取颜色值函数 - 简洁配色方案
    function getColorForValue(value) {
        // 将活动强度值映射为0-1之间的值
        const normalizedValue = Math.min(Math.max(value / 5, 0), 1);
        
        // 使用主题色#5e72e4的不同透明度
        return `rgba(94, 114, 228, ${normalizedValue * 0.7 + 0.2})`;
    }

    // 创建热图
    const heatmap = new Chart(ctx, {
        type: 'bubble',
        data: {
            datasets: [{
                label: '活动热图',
                data: activityData,
                backgroundColor: function(context) {
                    const count = context.dataset.data[context.dataIndex].count;
                    return getColorForValue(count);
                },
                hoverBackgroundColor: function(context) {
                    const count = context.dataset.data[context.dataIndex].count;
                    return `rgba(94, 114, 228, ${Math.min(count / 5 + 0.2, 1)})`;
                },
                borderColor: 'rgba(255, 255, 255, 0.4)',
                borderWidth: 1,
                pointRadius: function(context) {
                    const count = context.dataset.data[context.dataIndex].count;
                    // 根据活动值动态调整气泡大小
                    return 5 + count * 2;
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
                        text: '日期',
                        color: '#7f8c8d',
                        font: {
                            size: 12,
                            weight: 'normal'
                        }
                    },
                    grid: {
                        color: 'rgba(200, 200, 200, 0.1)',
                        borderColor: 'rgba(200, 200, 200, 0.2)'
                    },
                    ticks: {
                        color: '#95a5a6',
                        font: {
                            size: 10
                        }
                    }
                },
                y: {
                    min: 0,
                    max: 22,
                    title: {
                        display: true,
                        text: '活动强度',
                        color: '#7f8c8d',
                        font: {
                            size: 12,
                            weight: 'normal'
                        }
                    },
                    grid: {
                        color: 'rgba(200, 200, 200, 0.1)',
                        borderColor: 'rgba(200, 200, 200, 0.2)'
                    },
                    ticks: {
                        color: '#95a5a6',
                        font: {
                            size: 10
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(44, 62, 80, 0.8)',
                    titleColor: '#ecf0f1',
                    bodyColor: '#ecf0f1',
                    titleFont: {
                        size: 13,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 12
                    },
                    padding: 8,
                    cornerRadius: 4,
                    displayColors: false,
                    callbacks: {
                        title: function(context) {
                            return `日期 ${context[0].raw.x}`;
                        },
                        label: function(context) {
                            return `活动强度: ${context.raw.count}`;
                        }
                    }
                }
            },
            animation: {
                duration: 0
            },
            hover: {
                mode: 'nearest',
                intersect: true
            }
        }
    });
});