//温度趋势图
// echarts参数设置函数
var chartOptions = function (time, data, type) {
    var option = {
        title: {
            text: '温度趋势',
        },
        tooltip: {

        },
        legend: {
            data:['current_temp']
        },
        xAxis: {
            data: time
        },
        yAxis: {},
        series: [{
            name: 'current_temp',   // 数据名称
            type: type,           // 图表类型
            data: data,               // 图表数据
        }]
    }
    return option
}

// 基于准备好的dom，初始化echarts实例
var myChart = echarts.init(document.querySelector('#main'));
var time = []
var data = []
var type = {
    line: 'line',
    bar: 'bar',
}
// 指定图表的配置项和数据
var option = chartOptions(time, data, type.line)
// log(option)
// var option = {
//     tooltip: {},
//     legend: {
//         data:['current_temp']
//     },
//     xAxis: {
//         data: []
//     },
//     yAxis: {},
//     series: [{
//         name: 'current_temp',   // 数据名称
//         type: 'line',           // 图表类型
//         data: [],               // 图表数据
//     }]
// }
// 使用刚指定的配置项和数据显示图表。
myChart.setOption(option);

// var time = []
//var time = ["","","","","","","","","",""],
//    current_temp = [0,0,0,0,0,0,0,0,0,0]
// var current_temp = []


    //准备好统一的 callback 函数
var update_mychart = function (res) { //res是json格式的response对象
    // 隐藏加载动画
    myChart.hideLoading();

    // 把当前时间加到温度数组最后
    time.push(res.time);
    var temp = document.querySelector('#current_temp')
    //time.push(res.data[0]);
    //如果获取到的温度不为空，则把温度加到温度数组中，否则把上一次读取的数据加进去
    // 当前的数据,float类型，保留2位小数
    var current_data = parseFloat(res.data).toFixed(2)
    temp.innerHTML = current_data
    // log('current_data', current_data)
    // 上次的数据
    // var last_data = current_temp[current_temp.length - 1]
    // if (res.data.length != 0) {
    //     current_temp.push(current_data);
    //     // 显示当前数据
    //     temp.innerHTML = res.data
    // } else {
    //     current_temp.push(last_data)
    // }
    data.push(current_data)
    //删除数组中的第一个元素
    if (time.length >= 200) {
        time.shift();
        data.shift();
        // log('data', data)
    }
    // 填入数据
    var option1 = {
        xAxis: {
            data: time
        },
        series: [{
            name: 'current_temp', // 根据名字对应到相应的系列
            data: data,
        }],
    }
    // 填入数据
    // if (res.data.length != 0) {
    //     var option1 = {
    //         xAxis: {
    //             data: time
    //         },
    //         series: [{
    //             name: 'current_temp', // 根据名字对应到相应的系列
    //             data: data,
    //         }],
    //     }
    // } else {
    //     var option1 = {
    //         xAxis: {
    //             data: time
    //         },
    //         series: [{
    //             name: 'current_temp', // 根据名字对应到相应的系列
    //             data: data,
    //         }],
    //     }
        // 图1
    myChart.setOption(option1);
}
// 首次显示加载动画
myChart.showLoading();

// 建立socket连接，等待服务器“推送”数据，用回调函数更新图表
$(document).ready(function () {
    // var namespace = '/api/current_temp';
    var socket = io.connect('http://localhost:5000/api/current_temp');
    // log('socket', socket)
    socket.on('server_response', function (res) {
        update_mychart(res);
    });
});



