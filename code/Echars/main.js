// 等待DOM内容加载完毕
document.addEventListener("DOMContentLoaded", function() {

    // 初始化所有图表实例
    const chartTrend = echarts.init(document.getElementById('chart-trend'));
    const chartRank = echarts.init(document.getElementById('chart-rank'));
    const chartMap = echarts.init(document.getElementById('chart-map'));
    const chartGrowthRate = echarts.init(document.getElementById('chart-growth-rate'));

    // 加载数据并渲染图表
    async function loadDataAndRenderCharts() {
        try {
            // 并行加载数据和地图JSON
            const [dataResponse, mapResponse] = await Promise.all([
                fetch('data.json'),
                fetch('HK.json')
            ]);
            
            if (!dataResponse.ok) throw new Error('data.json 加载失败');
            if (!mapResponse.ok) throw new Error('HK.json 加载失败');
            
            const allData = await dataResponse.json();
            const hkMapJson = await mapResponse.json();

            // 1. 渲染KPI指标
            updateKpi(allData.trend);

            // 2. 渲染疫情总体趋势图
            renderTrendChart(allData.trend);

            // 3. 渲染各区排名图
            renderRankChart(allData.rank);
            
            // 4. 注册并渲染地图
            echarts.registerMap('HK', hkMapJson);
            renderMapChart(allData.map);

            // 5. 渲染增长率图
            renderGrowthRateChart(allData.trend);

        } catch (error) {
            console.error("加载或渲染数据时出错:", error);
            alert("加载数据失败，请确保 data.json 和 HK.json 文件存在且格式正确。");
        }
    }

    function updateKpi(trendData) {
        document.getElementById('total-cases').textContent = trendData.cumulative_cases.slice(-1)[0].toLocaleString();
        document.getElementById('today-new-cases').textContent = trendData.new_cases.slice(-1)[0].toLocaleString();
        document.getElementById('current-cases').textContent = (trendData.cumulative_cases.slice(-1)[0] - trendData.cumulative_cases.slice(-15)[0]).toLocaleString();
    }

    function renderTrendChart(trendData) {
        const option = {
            title: { text: '疫情总体趋势', textStyle: { color: '#fff' } },
            tooltip: { trigger: 'axis' },
            legend: { data: ['每日新增', '累计确诊'], textStyle: { color: '#ccc' }, top: 'bottom' },
            grid: { left: '3%', right: '4%', bottom: '15%', containLabel: true },
            xAxis: { type: 'category', data: trendData.dates, axisLine: { lineStyle: { color: '#ccc' } } },
            yAxis: [
                { type: 'value', name: '每日新增', axisLine: { lineStyle: { color: '#ccc' } } },
                { type: 'value', name: '累计确诊', position: 'right', axisLine: { lineStyle: { color: '#ccc' } } }
            ],
            series: [
                { name: '每日新增', type: 'bar', data: trendData.new_cases, itemStyle: { color: '#4e8af9' } },
                { name: '累计确诊', type: 'line', yAxisIndex: 1, data: trendData.cumulative_cases, itemStyle: { color: '#ff7f50' } }
            ]
        };
        chartTrend.setOption(option);
    }
    
    function renderRankChart(rankData) {
        const option = {
            title: { text: '各区确诊病例排名', textStyle: { color: '#fff' } },
            tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
            grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
            xAxis: { type: 'value', boundaryGap: [0, 0.01], axisLine: { lineStyle: { color: '#ccc' } } },
            yAxis: { type: 'category', data: rankData.districts.reverse(), axisLine: { lineStyle: { color: '#ccc' } } },
            series: [{
                name: '累计确诊',
                type: 'bar',
                data: rankData.values.reverse(),
                itemStyle: { color: '#2ecc71' }
            }]
        };
        chartRank.setOption(option);
    }
    
    function renderMapChart(mapData) {
        const option = {
            title: { text: '各区确诊病例地理分布', textStyle: { color: '#fff' } },
            tooltip: { trigger: 'item', formatter: '{b}<br/>确诊: {c}' },
            visualMap: {
                min: 0,
                max: Math.max(...mapData.map(item => item.value)),
                left: 'left',
                top: 'bottom',
                text: ['高', '低'],
                calculable: true,
                inRange: { color: ['#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026'] },
                textStyle: { color: '#fff' }
            },
            series: [{
                name: '香港疫情',
                type: 'map',
                map: 'HK',
                data: mapData
            }]
        };
        chartMap.setOption(option);
    }

    function renderGrowthRateChart(trendData) {
        const growthRate = trendData.new_cases.map((val, i) => {
            if (i === 0 || trendData.cumulative_cases[i - 1] === 0) return 0;
            return ((val / trendData.cumulative_cases[i - 1]) * 100).toFixed(2);
        });

        const option = {
            title: { text: '病例增长率趋势 (%)', textStyle: { color: '#fff' } },
            tooltip: { trigger: 'axis' },
            xAxis: { type: 'category', data: trendData.dates, axisLine: { lineStyle: { color: '#ccc' } } },
            yAxis: { type: 'value', axisLine: { lineStyle: { color: '#ccc' } } },
            series: [{
                data: growthRate,
                type: 'line',
                smooth: true,
                itemStyle: { color: '#e74c3c' }
            }]
        };
        chartGrowthRate.setOption(option);
    }
    
    loadDataAndRenderCharts();

    window.addEventListener('resize', function() {
        chartTrend.resize();
        chartRank.resize();
        chartMap.resize();
        chartGrowthRate.resize();
    });
}); 