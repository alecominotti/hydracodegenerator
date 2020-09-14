$(document).ready(function(){
	$('[data-bs-tooltip]').attr('data-delay', '{ "show": 200, "hide": 0 }');
	$('.navbar-title').attr('data-delay', '{ "show": 3000, "hide": 0 }');
	$('#generate_code').attr('data-delay', '{ "show": 2000, "hide": 0 }');
	$('#send_code').attr('data-delay', '{ "show": 2000, "hide": 0 }');
	$('[data-bs-tooltip]').tooltip();
	
});