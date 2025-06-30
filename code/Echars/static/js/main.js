document.addEventListener('DOMContentLoaded', function() {
    // 初始化 ECharts 实例
    const chartTrend = echarts.init(document.getElementById('chart-trend'));
    const chartPie = echarts.init(document.getElementById('chart-pie'));
    const chartGrowthRate = echarts.init(document.getElementById('chart-growth-rate'));
    const chartRank = echarts.init(document.getElementById('chart-rank'));

    // 通用的图表配置
    const chartOptionBase = {
        textStyle: { color: '#e0e0e0' },
        grid: { left: '5%', right: '5%', bottom: '10%', containLabel: true },
        tooltip: { trigger: 'axis', axisPointer: { type: 'cross' } }
    };

    async function loadAndRender() {
        try {
            const response = await fetch('/api/data');
            const data = await response.json();

            if (data.error) {
                alert('加载数据出错: ' + data.error);
                return;
            }

            // 1. 更新概览卡片
            document.getElementById('total-cases').textContent = data.overview.total_cases.toLocaleString();
            document.getElementById('latest-new-cases').textContent = data.overview.latest_new_cases.toLocaleString();
            document.getElementById('latest-growth-rate').textContent = data.overview.latest_growth_rate;

            // 2. 渲染趋势图
            chartTrend.setOption({
                ...chartOptionBase,
                title: { text: '每日新增与累计确诊趋势', textStyle: { color: '#fff' } },
                legend: { data: ['每日新增', '累计确诊'], textStyle: { color: '#ccc' } },
                xAxis: { type: 'category', data: data.trend.dates },
                yAxis: [
                    { type: 'value', name: '新增数' },
                    { type: 'value', name: '累计数', position: 'right' }
                ],
                series: [
                    { name: '每日新增', type: 'bar', data: data.trend.new, itemStyle: { color: '#00aaff' } },
                    { name: '累计确诊', type: 'line', yAxisIndex: 1, data: data.trend.cumulative, smooth: true, itemStyle: { color: '#ff4e4e' } }
                ]
            });

            // 3. 渲染区域分布饼图
            chartPie.setOption({
                ...chartOptionBase,
                title: { text: '各区域疫情分布', textStyle: { color: '#fff' } },
                tooltip: { trigger: 'item', formatter: '{b} : {c} ({d}%)' },
                legend: {
                    type: 'scroll',
                    orient: 'horizontal',
                    left: 'center',
                    top: 'bottom',
                    itemWidth: 18,
                    itemHeight: 14,
                    textStyle: { color: '#ccc', fontSize: 14 },
                    data: data.pie.map(p => p.name)
                },
                series: [{
                    name: '确诊病例',
                    type: 'pie',
                    radius: '55%',
                    center: ['50%', '55%'],
                    data: data.pie,
                    emphasis: { itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0, 0, 0, 0.5)' } }
                }]
            });

            // 4. 渲染增长率柱状图
            chartGrowthRate.setOption({
                ...chartOptionBase,
                title: { text: '疫情增长率(%)', textStyle: { color: '#fff' } },
                xAxis: { type: 'category', data: data.growth_rate_chart.dates },
                yAxis: { type: 'value', name: '增长率(%)' },
                series: [{ name: '增长率', type: 'bar', data: data.growth_rate_chart.rates, itemStyle: { color: '#f7b731' } }]
            });

            // 5. 渲染地区排名
            chartRank.setOption({
                ...chartOptionBase,
                title: { text: '地区累计确诊排名', textStyle: { color: '#fff' } },
                yAxis: { type: 'category', data: data.rank.districts },
                xAxis: { type: 'value' },
                series: [{ name: '累计确诊', type: 'bar', data: data.rank.values, itemStyle: { color: '#26de81' } }]
            });

        } catch (error) {
            console.error('获取或渲染图表时出错:', error);
            alert('无法连接到服务器或处理数据出错。');
        }
    }

    loadAndRender();

    // 窗口大小改变时重置图表
    window.addEventListener('resize', () => {
        chartTrend.resize();
        chartPie.resize();
        chartGrowthRate.resize();
        chartRank.resize();
    });
}); 