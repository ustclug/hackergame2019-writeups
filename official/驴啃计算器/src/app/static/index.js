var value = 0;
var poweron = false;

function display() {
    if (poweron) {
        var screen = document.querySelector('#screen');
        screen.innerHTML = value;
    }
}

function click(btn) {
    if (btn == 'ON') {
        value = 0.0;
        poweron = true;
    }

    if (!poweron) {
        return false;
    }

    switch (btn) {
        case 'C':
            value = 0;
            break;

        case 'D2R':
            value = value * (Math.PI / 180.0);
            break;

        case 'R2D':
            value = value * (180.0 / Math.PI);
            break;

        case '-x':
            value = -value;
            break;

        case 'x^2':
            value = Math.pow(value, 2);
            break;

        case '1/x':
            value = 1.0 / value;
            break;

        default:
            var allowed = ['sin', 'cos', 'tan',
                           'asin', 'acos', 'atan',
                           'sinh', 'cosh', 'tanh',
                           'asinh', 'acosh', 'atanh',
                           'exp', 'log', 'sqrt'
                        ];
            if (allowed.includes(btn)) {
                var fn = Math[btn];
                value = fn(value);
            }
            break;
    }

    display();
}

function load() {
    var btns = document.querySelectorAll('#calculator span');
    for(var i=0; i< btns.length; i++) {
        btns[i].addEventListener('click', function () {
            btn = this.innerHTML;
            click(btn);
        });
    }
}