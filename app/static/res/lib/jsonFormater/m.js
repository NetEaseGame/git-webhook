function calcCanvasHeight() {
    //計算格式化代碼顯示的高度
    var windowHeight = $(window).height();
    var canvasHeight = windowHeight - 145 - 45;
    var canvas = $("#Canvas");
    canvas.css("height", canvasHeight + "px");
}
function onLoad() {
    calcCanvasHeight();

    //每次窗口大小發生變化時都沖洗計算Canvas Div的高度
    $(window).resize(function(){
        calcCanvasHeight();
    });
}

onLoad();