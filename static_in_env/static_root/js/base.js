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
function ajaxAffirmClaim(){
    var claim_box = $(this).closest("[id^='claim_box']");
    var user_id = claim_box.attr("data-user-id");
    var claim_id = claim_box.attr("data-claim-id");
    var data = JSON.stringify({ "claim" : claim_id, "user" : user_id, "csrf_token" : csrftoken });
    $.ajax({
        "type": "POST",
        "dataType": "json",
        "url": "http://localhost:8000/api/affirmations/",
        "data": data,
        "contentType": "application/json",
        // "success": function(result) {
        //    console.log("YASS!");
        // },
    });
}

$(document).ready(function(){
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

// Edit Claims  contenteditable="true"
    $('#edit-claim').click(function(){
        var claim_name_elem = $(this).closest("[id^='claim-name']");
        claim_name_elem.attr("contenteditable", "true");
        var claim_content_elem = $(this).closest("[id^='claim-content']");
        claim_content_elem.attr("contenteditable", "true");
        $(this).text('Done');
    });

// behavior for claim plus: switch to check and create affirmation
// THESE NEED TO BE DRY-ED UP! ONLY DIFFERENCE IS POST VS DELETE
    $('.fa-plus').click(function(){
        var claim_box = $(this).closest("[id^='claim-box']");
        var user_id = claim_box.attr("data-user-id");
        var claim_id = claim_box.attr("data-claim-id");
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
        $(this).toggleClass('fa-plus fa-check');
    });
    $('.fa-check').click(function(){
        var claim_box = $(this).closest("[id^='claim-box']");
        var affirmation_id = claim_box.attr("data-affirmation-id");
        var url = "http://localhost:8000/api/affirmations/".concat(affirmation_id.toString()).concat("/");
        $.ajax( {
            "type": "DELETE",
            "url": url,
            "success": function(result) {
               console.log("Deleted!");
            },
        });
        $(this).toggleClass('fa-plus fa-check');
    });
});



// switchClass("fa-plus","")
