// javascript for the whole site


// javascript function to acquire CSRF Token (dependent upon jQuery)
// to use: var csrftoken = getCookie('csrftoken');
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


// behavior for claim plus: switch to check and create affirmation
$(document).ready(function(){
	$('.fa-plus').click(function(){
        // $.post('/affirmations/' + $(this).data().id + '/', {});
        $.ajax({
            url : "localhost:8000/api/affirmations/", // the endpoint
            type : "POST", // http method
            data : { claim : 110, user : 3 }, // data sent with the post request

            // handle a successful response
            success : function() {
                $(this).toggleClass('fa-plus fa-check');
            },

            // handle a non-successful response
            error : function() {
                $(this).toggleClass('fa-plus fa-car');
            }
        });
		// $(this).toggleClass('fa-plus fa-check');
	});
});



// switchClass("fa-plus","")
