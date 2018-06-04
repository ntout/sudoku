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


function generate_blank_puzzle () {
    for (let i = 0; i < 9; i++) {
        $('#input-puzzle').append("<tr class='row'></tr>")
    }
    for(let i = 0; i < 9; i++){
        $('#input-puzzle .row').append("<td class='input-container'><input class='box' style='border:none' maxlength='1'></td>")
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
}};


function clear_puzzle(table){
    let boxes = $(table);
    for(let i=0; i < boxes.length; i++){
        boxes[i].value = '';
    }
}

let formdata = new FormData();
function readURL(instance) {
    if (instance.files && instance.files[0]) {
        let reader = new FileReader();

        reader.onload = function (e) {
            $('#blah')
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




$('#img-file').on('change', function (e) {
    readURL(this);
   let fd = new FormData();
   fd.append('image', this.files[0]);
    $.ajax({
        url: '/api/whatever/',
        type: 'POST',
        data: fd,
        // async: false,
        contentType: false,
        processData: false,
        success: function(response){
            console.log(response);
            import_solved_string(response['puzzle'], '#input-puzzle .box')
        }
    })

});


$('#btn-solve').on('click', function (){
    console.log(extract_string());
    $.ajax({
        url: '/api/solver/',
        type: 'POST',
        data: {
            str: extract_string(),
        },
        success: function(response){
            console.log(response);
            import_solved_string(response['puzzle'], '#output-puzzle .box');
            console.log('solved')

        }
    })
});


// $('#btn-learn').on('click', function (){
//     console.log('Learn was clicked');
//     $.ajax({
//         url: '/api/learner/',
//         type: 'POST',
//         data: {
//             str: '000000000000000000000000000000000000000000000000000000000000000000000000000000000',
//             iterations: $('#num_to_add').value,
//         },
//         success: function(response){
//             console.log(response['puzzle']);
//             // import_solved_string(response['puzzle'])
//         }
//     })
// });


$('#btn-generate').on('click', function () {
   console.log('make was clicked');
   clear_puzzle('#input-puzzle .box');
   $.ajax({
       url: '/api/generate/',
       type: 'POST',
       data:{},
       success: function(response){
           console.log(response);
           import_solved_string(response['puzzle'], '#input-puzzle .box');
       }
   })
});


$('#btn-clear').on('click', function(){
    console.log('clear clicked');
    clear_puzzle('#input-puzzle .box');
    clear_puzzle('#output-puzzle .box')
});


$('#btn-count').on('click', function clue_count() {
    console.log('count clicked');
    let string = extract_string();
    $('#clue-count').value = 81 - string.split("0").length-1;
    console.log(81 - (string.split("0").length-1));
});


// $('#btn-extract').on('click', function () {
//    console.log('extract was clicked');
//    clear_puzzle('#input-puzzle .box');
//    $.ajax({
//        url: '/api/extract/',
//        type: 'POST',
//        data:{},
//        success: function(response){
//            console.log(response);
//            import_solved_string(response['puzzle'], '#input-puzzle .box');
//        }
//    })
// });


generate_blank_puzzle();
generate_filled_solution();