// javascript for the whole site


// javascript function to acquire CSRF Token (dependent upon jQuery)
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// set the header on my AJAX request and protect CSRF token from being sent to other domains
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


// when document is ready...
$(document).ready(function(){
    // security
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // define variables to be used
    // ...

    // affirm claim by clicking on the plus button
    // BUG: doesn't work if you click multiple times
    $('#claim-affirmation').click(function(){
        var affirmation_id = $(this).attr('data-affirmation-id');
        if (affirmation_id === "") {
            $(this).toggleClass('fa-plus fa-check');
            $('#num-affirmations').text($('#num-affirmations').text()*1+1);
            var claim_id = $(this).attr("data-claim-id");
            var data = JSON.stringify({ "claim" : claim_id, "user" : user_id, "csrf_token" : csrftoken });
            $.ajax({
                "type": "POST",
                "dataType": "json",
                "url": "http://localhost:8000/api/affirmations/",
                "data": data,
                "contentType": "application/json",
                "success": function(result) {
                   console.log("Posted!");
                },
            });
        } else if (affirmation_id !== "") {
            $(this).toggleClass('fa-plus fa-check');
            $('#num-affirmations').text($('#num-affirmations').text()*1-1);
            var url = "http://localhost:8000/api/affirmations/".concat(affirmation_id.toString()).concat("/");
            $.ajax( {
                "type": "DELETE",
                "url": url,
                "success": function(result) {
                   console.log("Deleted!");
                },
            });
        } else {
            console.log("ERROR!");
        }
    });

    // Edit the content of a claim
    $('#edit-claim').click(function(){
        var curr_text = $(this).text();
        if (curr_text === "Edit") {
            $('#claim-name, #claim-content').attr("contenteditable", "true");
            $(this).text("Cancel");
            $(this).after('<button type="button" id="save-claim" class="btn btn-primary">Save</button>');
        } else if (curr_text === "Cancel") {
            location.reload();
        }
    });
    // Save the content of a claim
    $('#claim-box').on("click", '#save-claim', function(){
        $('#claim-name, #claim-content').attr("contenteditable", "false");
        $('#edit-claim').text("Edit");
        var claim_id = $('#claim-content').attr("data-claim-id");
        var claim_name = $('#claim-name').text();
        var claim_content = $('#claim-content').text();
        var data = '{ "id" : "'.concat(claim_id).concat('", "name" : "').concat(claim_name.replace(/\s+/g, " ")).concat('", "content" : "').concat(claim_content.replace(/\s+/g, " ")).concat('",  "csrf_token" : "').concat(csrftoken).concat('"}');
        $.ajax({
            "type": "PUT",
            "dataType": "json",
            "url": "http://localhost:8000/api/claims/".concat(claim_id.toString()).concat("/"),
            "data": data,
            "contentType": "application/json",
            "success": function(result) {
               console.log("Posted!");
            },
        });
        $(this).remove();
    });


    // Save the content of a claim
    // $('#save-claim').click(function(){
    //     $('#claim-name, #claim-content').attr("contenteditable", function(index, attr) {
    //         return attr == 'false' ? 'true' : 'false';
    //     });
    //     $(this).text(function(index, text) {
    //         return text == 'Edit' ? 'Done' : 'Edit';
    //     });
    // });

});



// switchClass("fa-plus","")
