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
        var data = {
            'inputTemp': inputTemp,
            'inputRamp': inputRamp,
        }
        apiSetTemp(data, function(r){
            log('play被点到了')
            log('inputTemp', inputTemp)
            log('inputRamp', inputRamp)
        })
    })
    stopButton.addEventListener('click', function(){
        log('stop被点到了')
        stopSetTemp()
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

var __main = function(){
    bindEventSetTemp()
}

__main()