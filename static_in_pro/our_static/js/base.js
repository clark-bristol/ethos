// javascript for the whole site

// $(document.body).on(function(){
// 	// $('#affirm_plus').fadeOut();
// 	$('div').switchClass("fa-plus","")
// });

$(document).ready(function(){
	// $('#affirm_plus').fadeOut();
	$('.fa-plus').click(function(){
        $.post('/affirmations/' + $(this).data().id + '/', {});
		$(this).toggleClass('fa-plus fa-check');
	});
});



// switchClass("fa-plus","")
