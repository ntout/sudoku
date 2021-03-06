// using jQuery
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
let csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


function validate(evt) {
  let theEvent = evt || window.event;
  let key = theEvent.keyCode || theEvent.which;
  key = String.fromCharCode( key );
  let regex = /[1-9]/;
  if( !regex.test(key) ) {
    theEvent.returnValue = false;
    if(theEvent.preventDefault) theEvent.preventDefault();
  }
}


function generate_blank_puzzle () {
    for (let i = 0; i < 9; i++) {
        $('#input-puzzle').append("<tr class='row'></tr>")
    }
    for(let i = 0; i < 9; i++){
        $('#input-puzzle .row').append("<td class='input-container'><input class='box' style='border:none' maxlength='1' onkeypress='validate(event)'></td>")
    }
}


function generate_filled_solution () {
    for (let i = 0; i < 9; i++) {
        $('#output-puzzle').append("<tr class='row'></tr>")
    }
    for(let i = 0; i < 9; i++){
        $('#output-puzzle .row').append("<td class='input-container'><input class='box' style='border:none' maxlength='1'></td>")
    }
}


function extract_string() {
    let boxes = $('#input-puzzle .box');
    let string = '';
    for(let i=0; i < boxes.length; i++){
        if(boxes[i].value.length === 0){
            string += '0'
        }
        else{
            string += boxes[i].value
        }
    }
    return string
}


function import_solved_string(str, table){
    let boxes = $(table);
    for(let i=0; i < boxes.length; i++){
        if(str[i] !== '0'){
            boxes[i].value = str[i];
        }
}}


function clear_puzzle(table){
    let boxes = $(table);
    for(let i=0; i < boxes.length; i++){
        boxes[i].value = '';
    }
    for (let i = 0; i < 81; i++) {
        $('#input-puzzle .box')[i].style.color = '#000000';
        $('#output-puzzle .box')[i].style.color = '#000000';
    }
}

let formdata = new FormData();
function readURL(instance) {
    if (instance.files && instance.files[0]) {
        let reader = new FileReader();

        reader.onload = function (e) {
            $('#image-upload')
                .attr('src', e.target.result)
                .width(300)
                .height(300);
        };

        reader.readAsDataURL(instance.files[0]);

        }
}

function imageToBase64(img) {
    let canvas, ctx, dataURL, base64;
    canvas = document.createElement("canvas");
    ctx = canvas.getContext("2d");
    canvas.width = img.width;
    canvas.height = img.height;
    ctx.drawImage(img, 0, 0);
    dataURL = canvas.toDataURL("image/png");
    base64 = dataURL.replace(/^data:image\/png;base64,/, "");
    return base64;
}


function change_color() {
    for (let i = 0; i < 81; i++) {
        if ($('#input-puzzle .box')[i].value.length === 1) {
            $('#output-puzzle .box')[i].style.color = '#00ff00';
        }
    }}


$('#img-file').on('change', function (e) {
    $('#input-puzzle').toggleClass('loading');
    clear_puzzle('#output-puzzle .box');
    readURL(this);
    let fd = new FormData();
    fd.append('image', this.files[0]);
    $.ajax({
        url: '/api/upload/',
        type: 'POST',
        data: fd,
        // async: false,
        contentType: false,
        processData: false,
        success: function(response){
            clear_puzzle('#input-puzzle .box');
            console.log(response);
            import_solved_string(response['puzzle'], '#input-puzzle .box');
            $('#input-puzzle').toggleClass('loading');
        },
    })

});


$('#btn-solve').on('click', function (){
    $('#output-puzzle').toggleClass('loading');
    $('#solution-container').show(1000);
    console.log(extract_string());
    change_color();
    $.ajax({
        url: '/api/solver/',
        type: 'POST',
        data: {
            str: extract_string(),
        },
        success: function(response){
            console.log(response);
            import_solved_string(response['puzzle'], '#output-puzzle .box');
            console.log('solved');
            // $('#solution-container').toggle(1000);
            $('#output-puzzle').toggleClass('loading');

        }
    })
});


$('#btn-generate').on('click', function () {
    $('#solution-container').hide(1000);
    if( $('#input-puzzle').attr('class') !== 'loading'){
        $('#input-puzzle').toggleClass('loading');
    }
    console.log('make was clicked');
    clear_puzzle('#input-puzzle .box');
    clear_puzzle('#output-puzzle .box');
    $.ajax({
        url: '/api/generate/',
        type: 'POST',
        data:{},
        success: function(response){
           console.log(response);
           import_solved_string(response['puzzle'], '#input-puzzle .box');
           $('#input-puzzle').toggleClass('loading');

       }
    });
});


$('#btn-clear').on('click', function(){
    $('#solution-container').hide(1000);
    console.log('clear clicked');
    clear_puzzle('#input-puzzle .box');
    clear_puzzle('#output-puzzle .box');
    if( $('#input-puzzle').attr('class') == 'loading'){
        $('#input-puzzle').toggleClass('loading');
    }
    if( $('#output-puzzle').attr('class') == 'loading'){
        $('#output-puzzle').toggleClass('loading');
    }

});



$('#input-puzzle').keyup(function () {
    $.ajax({
        url: '/api/validate/',
        type: 'POST',
        data: {
            'str': extract_string()
        },
        success: function (response) {
            for (let i = 0; i < 81; i++) {
                $('#input-puzzle .box')[i].style.color = '#000000';
            }
            let data = $('#input-puzzle .box');
            let invalid_sudoku = response['invalid'];
            Object.keys(invalid_sudoku).forEach(function(key) {
                console.log(invalid_sudoku[key]['box']);
                data[invalid_sudoku[key]['box']].style.color = '#ff0000'


            });
        }
    });
});







generate_blank_puzzle();
generate_filled_solution();

















