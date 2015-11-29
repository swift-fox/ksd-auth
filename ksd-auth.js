var ksd_auth = (function(input) {
    var press, release, base;
    var ignore = [8, 9, 13];    // BACKSPACE, TAB, ENTER

    press = [];
    release = [];

    function clear() {
        input.value = '';
        press.length = release.length = 0;        
    }

    input.onkeydown = function() {
        if(event.keyCode == 8) {    // If BACKSPACE, clear the input box
            clear();
        } else if (ignore.indexOf(event.keyCode) < 0) {
            if(press.length == 0)
                base = Date.now();
            press.push(Date.now() - base);
        }
    }

    input.onkeyup = function() {
        if(ignore.indexOf(event.keyCode) < 0)
            release.push(Date.now() - base);
    }
    
    return {
        getPattern : function() {return [press, release];},
        getText : function() {return input.value;},
        clear : clear
    };
});