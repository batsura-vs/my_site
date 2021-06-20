window.onload = function () {
    function clicked(elem, elem2) {
        if (!elem2.getAttribute('data-disabled')) {
            if (elem.getAttribute('value') === '1') {
                elem.style.removeProperty('right')
                elem.setAttribute('value', '0')
                elem2.style.background = elem2.getAttribute('data-pas')
            } else {
                elem.style.right = '0'
                elem.setAttribute('value', '1')
                elem2.style.background = elem2.getAttribute('data-act')
            }
            let event = new Event("click"); // (2)
            elem.dispatchEvent(event);
        }
    }

    let op2 = document.getElementsByClassName('check')
    for (var i2 = 0; i2 < op2.length; i2++) {
        let ch = op2[i2].children;
        ch[0].style.background = ch[0].getAttribute('data-color')
        let elem = ch[0]
        let elem2 = op2[i2]
        let p = document.documentElement.clientWidth / 100 * elem2.getAttribute('data-size')
        elem2.style.height = p / 2 + 'px'
        elem2.style.width = p + 'px'
        if (!elem2.getAttribute('data-disabled')) {
            if (elem.getAttribute('value') !== '1') {
                elem.style.removeProperty('right')
                elem.setAttribute('value', '0')
                elem2.style.background = elem2.getAttribute('data-pas')
            } else {
                elem.style.right = '0'
                elem.setAttribute('value', '1')
                elem2.style.background = elem2.getAttribute('data-act')
            }
        } else {
            elem2.style.background = '#aea7a7'
            elem.style.background = '#756c6c'
        }
        op2[i2].addEventListener('click', clicked.bind(null, ch[0], op2[i2]))
    }

    function select(inp, inp2, opt, elem) {
        inp.value = opt.innerText
        inp2.value = opt.getAttribute('value')
        let event = new Event("oninput"); // (2)
        elem.dispatchEvent(event);
    }

    let op = document.getElementsByClassName('select')
    for (var i = 0; i < op.length; i++) {
        var c1 = "#e66465"
        var c2 = "#9198e5"
        var c = "black"
        if (op[i].getAttribute('color1')) {
            c1 = op[i].getAttribute('color1')
        }
        if (op[i].getAttribute('color2')) {
            c2 = op[i].getAttribute('color2')
        }
        if (op[i].getAttribute('color')) {
            c = op[i].getAttribute('color')
        }
        op[i].style.background = `linear-gradient(to right, ${c1},
             ${c2})`
        op[i].style.color = c
        let ch = op[i].children;
        let inp = ch[0];
        let opt = ch[2].children
        ch[2].style.background = `linear-gradient(to right, ${c1},
             ${c2})`
        for (var x = 0; x < opt.length; x++) {
            opt[x].addEventListener('click', select.bind(null, inp, ch[1], opt[x], op[i]))
        }
    }

    function scrollFunc(x) {
        let m = Math.max(
            document.body.scrollHeight, document.documentElement.scrollHeight,
            document.body.offsetHeight, document.documentElement.offsetHeight,
            document.body.clientHeight, document.documentElement.clientHeight)
        let c = document.documentElement.clientHeight
        let p = (pageYOffset) * 100 / (m - c)
        x.style.width = p + '%'
    }

    function scroll_to(elem) {
        elem.scrollIntoView();
        let coords = elem.getBoundingClientRect();
        if (coords.top > document.documentElement.clientHeight / 100 * 10) {
        } else {
            scrollTo(0, pageYOffset - document.documentElement.clientHeight / 100 * 10)
        }
        elem.animate([
            // keyframes
            {background: '#81ff00', borderRadius: '3rem'}
        ], {
            // timing op3tions
            duration: 1000,

        })
    }

    let op3 = document.getElementsByClassName('fill')
    let m = Math.max(
        document.body.scrollHeight, document.documentElement.scrollHeight,
        document.body.offsetHeight, document.documentElement.offsetHeight,
        document.body.clientHeight, document.documentElement.clientHeight)
    for (var i3 = 0; i3 < op3.length; i3++) {
        let elems = document.getElementsByClassName('punkt');
        for (var z = 0; z < elems.length; z++) {
            let elem = elems[z];
            let coords = elem.getBoundingClientRect();
            let topVisible = coords.top;
            let d = document.createElement('div');
            d.className = 'red-point';
            let p = (topVisible) * 100 / (m)
            d.style.left = p + '%';
            d.title = elem.innerText
            op3[i3].appendChild(d);
            d.addEventListener('click', scroll_to.bind(null, elem));
        }
        window.onscroll = scrollFunc.bind(null, op3[i3]);
        scrollFunc(op3[i3])
    }

    let pages = document.getElementsByClassName('page')
    for (var page = 0; page < pages.length; page++) {
        let page_ = pages[page];
        let coords = page_.getBoundingClientRect();
        let topVisible = coords.bottom;
        page_.style.height = document.documentElement.clientHeight + 'px';
    }


    function getChildClassName(className, elem) {
        for (var i = 0; i < elem.childNodes.length; i++) {
            if (elem.childNodes[i].className === className) {
                return elem.childNodes[i]
            }
        }
    }

    function right(elem) {
        let x = elem.getAttribute('data-page')
        let p = elem.getElementsByClassName('pages')[0]
        if (x < p.children.length - 1) {
            let pg = elem.getElementsByClassName('progress')[0].children
            setNumb(pg[parseInt(x) + 1], elem)
            p.children[parseInt(x)].style.display = 'none'
            elem.setAttribute('data-page', parseInt(x) + 1)
            p.children[parseInt(x) + 1].style.display = 'block'
        }
    }

    function left(elem) {
        let x = elem.getAttribute('data-page')
        let p = elem.getElementsByClassName('pages')[0]
        if (x > 0) {
            let pg = elem.getElementsByClassName('progress')[0].children
            setNumb(pg[x - 1], elem)
            p.children[parseInt(x)].style.display = 'none'
            elem.setAttribute('data-page', x - 1)
            p.children[parseInt(x - 1)].style.display = 'block'
        }
    }

    function setNumb(elem, el) {
        let p = el.getElementsByClassName('pages')[0]
        for (let v = 0; v < p.children.length; v++) {
            let f = p.children[v];
            if (f.style.display !== 'none') {
                f.style.display = 'none'
            }
        }
        el.setAttribute('data-page', parseInt(elem.innerHTML) - 1)
        p.children[parseInt(elem.innerHTML) - 1].style.display = 'block'
        remNumb(el)
        elem.className = 'active numb'
    }

    function remNumb(elem) {
        let f = elem.getElementsByClassName('active')[0]
        f.className = 'numb'
    }

    let pag = document.getElementsByClassName('pages')
    for (var p = 0; p < pag.length; p++) {
        let _page = pag[p]
        let ch01 = _page.children
        ch01[0].style.display = 'block'
    }
    let carrousels = document.getElementsByClassName('carrousel')
    for (var car = 0; car < carrousels.length; car++) {
        let el = carrousels[car]
        el.setAttribute('data-page', '0');
        let right_button = getChildClassName('right', el);
        let left_button = getChildClassName('left', el);
        left_button.addEventListener('click', left.bind(null, el));
        right_button.addEventListener('click', right.bind(null, el));
        for (let but = 0; but < el.getElementsByClassName('pages')[0].children.length; but++) {
            let p = el.getElementsByClassName('progress')[0];
            let numb = document.createElement('div');
            numb.className = 'numb';
            if (but === 0) {
                numb.className = 'active numb'
            }
            numb.innerHTML = but + 1;
            p.appendChild(numb)
            numb.addEventListener('click', setNumb.bind(null, numb, el))
        }
    }
}
