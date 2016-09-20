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


// behavior for claim plus: switch to check and create affirmation
$(document).ready(function(){
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
	$('.fa-plus').click(function(){
        console.log("About to toggle!");
        $(this).toggleClass('fa-plus fa-check');
        console.log("Toggled!");
        // $.post('/affirmations/' + $(this).data().id + '/', {});
        var data = JSON.stringify({ "claim" : 128, "user" : 4, "csrf_token" : csrftoken });
        console.log(data);
        console.log("About to post!");
        $.ajax({
            "type": "POST",
            "dataType": "json",
            "url": "http://localhost:8000/api/affirmations/",
            "data": data,
            "contentType": "application/json",
            "success": function(result) {
                console.log("YASS!");
            },
        });
        console.log("Posted!");
		// $(this).toggleClass('fa-plus fa-check');
	});
});



// switchClass("fa-plus","")
