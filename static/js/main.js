/**
 * Created by Administrator on 2018/7/1.
 */

var bindEventSetTemp = function(){
    var playButton = e('#id-button-play')
    var stopButton = e('#id-button-stop')
    var pauseButton = e('#id-button-pause')
    //var configButton = e('#id-button-config')
    var submitButton = e('#id-button-submit')
    var intervalInput = e('#id-input-interval')

    playButton.addEventListener('click',function(){
        var setTemp = e('#id-input-settemp')
        var setRamp = e('#id-input-setramp')
        var inputTemp = setTemp.value
        var inputRamp = setRamp.value
        var sv = svCmd(inputTemp)
        var time = timeCmd(inputRamp)
        var act = ':010608000001f0\r\n'
        log('sv', sv)
        var data = {
            'sv': sv,
            'time': time,
            'act': act,
        }
        apiSetTemp(data, function(){
            log('play被点到了')
            // log('inputTemp', inputTemp)
            // log('inputRamp', inputRamp)
        })
    })

    stopButton.addEventListener('click', function(){
        var data = {
            'stop_cmd': ':010608000000f1\r\n',
        }
        stopSetTemp(data, function (r) {
            log('stop被点到了')
        })
    })
    pauseButton.addEventListener('click', function(){
        log('pause被点到了')

    })
    //configButton.addEventListener('click', function(){
    //    log('config被点到了')
    //})
    // submitButton.addEventListener('click', function(){
    //     log('submit被点到了')
    //     intervalValue = intervalInput.value
    //     send_data = {
    //         'intervalValue': intervalValue,
    //     }
    //     log(intervalValue)
    // })
}

var test = function () {
// 建立socket连接，等待服务器“推送”数据，用回调函数更新图表
    $(document).ready(function () {
        namespace = '/api/current_temp';
        var socket = io.connect('http://localhost:5000/api/current_temp');
        log(22222)
        socket.on('server_response', function (res) {
            log(333333)
            update_mychart(res);
        });
    });
}

var __main = function(){
    bindEventSetTemp()
    // var a = "010301000001";
    // data = calLrc(a)
    // log(data)
    // test()
}

__main()