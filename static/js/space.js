/**
 * Created by Administrator on 2018/7/2.
 */

//document.onkeydown = function(event){
//        var e = event || window.event || arguments.callee.caller.arguments[0]
//        if(e && e.keyCode==13){ // 按enter
//            //要做的事情
//            log('空格键被按下了')
//            log('当前温度', current_temp[0])
//          }
//    }

// 通过监听按钮来启动命令
window.addEventListener("keydown", function(e) {
    // enter键开始
    if (e.keyCode == 13)
        log('enter键按下了')
}, false)
