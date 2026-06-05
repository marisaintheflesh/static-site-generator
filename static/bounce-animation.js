var canvas = null;
var ctx = null;
var cw = 320;
var ch = 180;
var w = 120;
var h = 27;
var x = getRandom(1, cw - w - 1);
var y = getRandom(1, ch - h - 1);
var xDelta = 1;
var yDelta = 1;
var m = new Image(w, h);
m.src = "/m.png";

function getRandom(min, max)
{
    var minCeiled = Math.ceil(min);
    var maxFloored = Math.floor(max);
    return Math.floor(Math.random() * (maxFloored - minCeiled + 1) + minCeiled);
}

function DOMLoaded()
{
    var canvasWrapper = document.getElementById("canvas-wrapper");
    if (canvasWrapper)
    {
        var staticLogo = document.getElementById("static-logo");
        if (staticLogo)
        {
            staticLogo.remove();
        }
    }
}

function main()
{
    canvas = document.createElement("canvas");
    if (canvas)
    {
        var canvasWrapper = document.getElementById("canvas-wrapper");
        if (canvasWrapper)
        {
            canvas.id = "canvas";
            canvas.width = cw;
            canvas.height = ch;
            canvasWrapper.appendChild(canvas);
            ctx = canvas.getContext("2d");
            if (ctx)
            {
                requestAnimationFrame(draw);
            }
        }
    }

}

function clear()
{
    ctx.fillStyle = "#121212";
    ctx.fillRect(0, 0, cw, ch);
}

function draw()
{
    clear();
    x += xDelta;
    y += yDelta;
    if (x + w >= cw || x <= 0)
    {
        xDelta *= -1;
    }

    if (y + h >= ch || y <= 0)
    {
        yDelta *= -1;
    }
    ctx.drawImage(m, x, y);
    requestAnimationFrame(draw);
}

addEventListener("load", function()
{
    main();
});
addEventListener("DOMContentLoaded", function()
{
    DOMLoaded();
});
/*
function resize()
{

}
addEventListener("resize", function() { resize(); });
*/
