/**
 * Created by Administrator on 2018/7/1.
 */
/*
1, 给 add button 绑定事件
2, 在事件处理函数中, 获取 input 的值
3, 用获取的值 组装一个 todo-cell HTML 字符串
4, 插入 todo-list 中
*/

var log = function() {
    console.log.apply(console, arguments)
}

var e = function(sel) {
    return document.querySelector(sel)
}

/*
 ajax 函数
*/
var ajax = function(method, path, data, reseponseCallback) {
    var r = new XMLHttpRequest()
    // 设置请求方法和请求地址
    r.open(method, path, true)
    // 设置发送的数据的格式为 application/json
    // 这个不是必须的
    r.setRequestHeader('Content-Type', 'application/json')
    // 注册响应函数
    r.onreadystatechange = function() {
        if(r.readyState === 4) {
            // r.response 存的就是服务器发过来的放在 HTTP BODY 中的数据
            reseponseCallback(r.response)
            log(r.response)
        }
    }
    // 把数据转换为 json 格式字符串
    data = JSON.stringify(data)
    // 发送请求
    r.send(data)
}

// TEMP API
// 程序段模式set温度
var apiSetTemp = function(form, callback) {
    var path = '/api/set_temp'
    ajax('POST', path, form, callback)
}

// 程序段模式stop温度
var stopSetTemp = function(stop_cmd, callback) {
    var path = '/api/stop_temp'

    ajax('POST', path, stop_cmd, callback)
}

// 设置配置文件
//var apiSetConfig = function(form, callback) {
//    var path = '/api/set_config'
//    ajax('POST', path, form, callback)
//}

//// 增加一个 todo
//var apiTodoAdd = function(form, callback) {
//    var path = '/api/todo/add'
//    ajax('POST', path, form, callback)
//}

//字符转换
var Hexstring2btye = function (str) {
    var pos = 0;
    var len = str.length;
    if (len % 2 != 0) {
        return null;
    }
    len /= 2;
    var hexA = new Array();
    for (var i = 0; i < len; i++) {
        var s = str.substr(pos, 2);
        var v = parseInt(s, 16);
        hexA.push(v);
        pos += 2;
    }
    return hexA;
}


var Bytes2HexString = function (b) {
    var hexs = "";
    for (var i = 0; i < b.length; i++) {
        var hex = b[i].toString(16);
        if (hex.length == 1) {
            hex = '0' + hex;
        }
        hexs += hex.toUpperCase();
    }
    return hexs;
}


var fill = function (num, n) {
    var len = num.toString().length;
    while (len < n) {
        num = "0" + num;
        len++;
    }
    return num;
}

//解析input数据
var dataParse = function (data) {
    //把字符串转换为number，并且取两位小数，再*100
    data = parseFloat(data).toFixed(2)*100
    //转换为16进制字符串
    data = data.toString(16)
    //字符串不足4位，前面补零
    data = fill(data, 4)

    return data
}

//LRC校验计算
var calLrc = function (e) {
    var data = Hexstring2btye(e);
    var b = 0;
    for (var i of data) {
        b += i
        // console.log(data)
    }
    var c = ~b + 1
    var d = c & 0xff
    data.push(d)
    // console.log(data)

    var dataLrc = Bytes2HexString(data);
    // log('dataLrc', dataLrc)

    return dataLrc
}

var svCmd = function (segment, inputvalue) {
    var setData = dataParse(inputvalue)
    var data = segment + setData
    data = calLrc(data)
    data = ':' + data + '\r\n'

    return data
}

var timeCmd = function (inputvalue) {
    var setData = dataParse(inputvalue)
    var data = '0106000e' + setData
    data = calLrc(data)
    data = ':' + data + '\r\n'

    return data
}