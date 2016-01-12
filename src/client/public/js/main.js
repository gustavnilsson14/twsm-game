$(document).ready(function(){

    if ("WebSocket" in window)
    {
        var ws = new WebSocket("ws://localhost:8888/ws");
        var keys = {}

        ws.onopen = function()
        {
            // Web Socket is connected, send data using send()
            ws.send("Message to send");
        };
        jQuery(document).keydown(function( e ) {
            if ( keys[e.which] != true ){
                data = {'kd':e.which}
                ws.send(JSON.stringify(data))
                keys[e.which] = true
            }
        });

        jQuery(document).keyup(function( e ) {
            if ( keys[e.which] != false ){
                data = {'ku':e.which}
                ws.send(JSON.stringify(data))
                keys[e.which] = false
            }
        });

        ws.onmessage = function (e)
        {
            var data = JSON.parse(e.data);
            console.log( e.data );
            for (var i = 0; i < data.d.length; i++) {
                for (key in data.d[i]) {
                    if ( $('#' + key).length == 0 ){
                        $('body').append('<p style="position:absolute;left:0px;top:0px;" id="'+key+'">O</p>')
                    }
                    $('#' + key).css('left', data.d[i][key].pos[0]).css('top', data.d[i][key].pos[1])
                }
            }
        };

        ws.onclose = function()
        {
            // websocket is closed.
            console.log("Connection is closed...");
        }
    }
    else
    {
        alert("WebSocket NOT supported by your Browser!");
    }
});
