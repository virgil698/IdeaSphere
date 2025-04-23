// drawer.js 完整修改版
let cpuChart = null;
let memoryChart = null;

const commonChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        title: { display: true, font: { size: 16 } },
        legend: { position: 'bottom' }
    }
};

async function initCpuChart() {
    try {
        const ctx = document.getElementById('myChart');

        // 增强型销毁逻辑
        if (cpuChart) {
            cpuChart.destroy();
            cpuChart = null;
            await new Promise(resolve => setTimeout(resolve, 50)); // 确保完全释放
        }

        const cpuValue = await monitor('cpu');

        cpuChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['已使用 CPU', '空闲 CPU'],
                datasets: [{
                    data: [cpuValue, 100 - cpuValue],
                    backgroundColor: ['#ff6384', '#36a2eb']
                }]
            },
            options: {
                ...commonChartOptions,
                plugins: {
                    ...commonChartOptions.plugins,
                    title: {
                        ...commonChartOptions.plugins.title,
                        text: `实时CPU使用率 (${cpuValue}%)`
                    },
                    tooltip: {
                        callbacks: {
                            label: (ctx) => `${ctx.label}: ${ctx.raw}%`
                        }
                    }
                }
            }
        });

    } catch (error) {
        console.error('CPU图表初始化失败:', error);
    }
}

async function initMemoryChart() {
    try {
        const ctx = document.getElementById('myChart2');

        if (memoryChart) {
            memoryChart.destroy();
            memoryChart = null;
            await new Promise(resolve => setTimeout(resolve, 50));
        }

        const memoryValue = await monitor('memory');

        memoryChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['已使用内存', '空闲内存'],
                datasets: [{
                    data: [memoryValue, 100 - memoryValue],
                    backgroundColor: ['#ff6384', '#36a2eb']
                }]
            },
            options: {
                ...commonChartOptions,
                plugins: {
                    ...commonChartOptions.plugins,
                    title: {
                        ...commonChartOptions.plugins.title,
                        text: `实时内存使用率 (${memoryValue}%)`
                    },
                    tooltip: {
                        callbacks: {
                            label: (ctx) => `${ctx.label}: ${ctx.raw}%`
                        }
                    }
                }
            }
        });

    } catch (error) {
        console.error('内存图表初始化失败:', error);
    }
}

// 统一初始化逻辑
document.addEventListener('DOMContentLoaded', () => {
    const updateCharts = async () => {
        try {
            await Promise.allSettled([
                initCpuChart(),
                initMemoryChart()
            ]);
        } catch (error) {
            console.error('图表更新失败:', error);
        }
    };

    // 立即执行并设置统一间隔
    updateCharts();
    setInterval(updateCharts, 5000);
});
