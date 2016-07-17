// javascript for the whole site

// $(document.body).on(function(){
// 	// $('#affirm_plus').fadeOut();
// 	$('div').switchClass("fa-plus","")
// });

$(document).ready(function(){
	// $('#affirm_plus').fadeOut();
	$('.fa-plus').click(function(){
		// $('.fa-plus').fadeOut();
		$(this).toggleClass('fa-plus fa-check');
		// $('.fa-check').switchClass('.fa-check','fa-plus',1000);
	});
});



// switchClass("fa-plus","")