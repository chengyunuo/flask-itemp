/**
 * Created by Administrator on 2018/7/1.
 */

var bindEventSetTemp = function(){
    // var playButton = e('#id-button-play')
    var playButton = $('#id-button-play')
    // var stopButton = e('#id-button-stop')
    var stopButton = $('#id-button-stop')
    // var pauseButton = e('#id-button-pause')
    var pauseButton = $('#id-button-pause')
    //var configButton = e('#id-button-config')
    var submitButton = e('#id-button-submit')
    var intervalInput = e('#id-input-interval')
    //启动按钮事件
    playButton.on('click',function(){
        var setTemp = e('#id-input-settemp')
        var setRamp = e('#id-input-setramp')
        var inputTemp = setTemp.value
        var inputRamp = setRamp.value
        var deact_cmd = ':010608000000f1\r\n'
        //程序段1，time不等于0，out不等于0
        var sv_cmd1 = svCmd('0106000d', inputTemp)
        log('sv_cmd1', sv_cmd1)
        var time_cmd1 = timeCmd(inputRamp)
        var out_cmd1 = svCmd('0106000f', 1)
        log('out_cmd1', out_cmd1)
        //程序段2，time=0，out不等于0
        var sv_cmd2 = svCmd('01060010', inputTemp)
        log('sv_cmd2', sv_cmd2)
        var time_cmd2 = ':010600110000e8\r\n'
        var out_cmd2 = svCmd('01060012', 1)
        log('out_cmd2', out_cmd2)


        var act_cmd = ':010608000001f0\r\n'
        var setCmds = {
            'deact_cmd': deact_cmd,
            'sv_cmd1': sv_cmd1,
            'time_cmd1': time_cmd1,
            'out_cmd1': out_cmd1,
            'act_cmd': act_cmd,
            'sv_cmd2': sv_cmd2,
            'time_cmd2': time_cmd2,
            'out_cmd2': out_cmd2,
        }
        // log('setCmds', setCmds)


        $.ajax({
            url: 'api/set_temp',
            method: 'post',
            data:JSON.stringify(setCmds),  //转变传递的参数为字符串格式
            contentType:'application/json; charset=UTF-8',
            dataType:'json',//希望服务器返回json格式的数据
            success: function (data) {
                log('set_data', data);
            }
        });
    });
    //停止按钮事件
    stopButton.on('click', function(){
        var stopCmds = {
            'fix_cmd': ':010608000000f1\r\n',
        }

        $.ajax({
            url: 'api/stop_temp',
            method: 'post',
            data:JSON.stringify(stopCmds),  //转变传递的参数为字符串格式
            contentType:'application/json; charset=UTF-8',
            dataType:'json',//希望服务器返回json格式的数据
            success: function (data) {
                log('stop_data', data)
            }
        });
    })
    //暂停按钮事件
    pauseButton.on('click', function(){
        var pauseCmds = {
            'fix_cmd': ':010608000000f1\r\n',
            'read_cmd': ':010301000001FA\r\n',
        }

        $.ajax({
            url: 'api/pause_temp',
            method: 'post',
            data:JSON.stringify(pauseCmds),  //转变传递的参数为字符串格式
            contentType:'application/json; charset=UTF-8',
            dataType:'json',//希望服务器返回json格式的数据
            success: function (data) {
                log('pause_data', data)
            }
        });
    })
}


var __main = function(){
    bindEventSetTemp()
}

__main()