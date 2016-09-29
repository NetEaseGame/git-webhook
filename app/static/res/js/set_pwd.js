function add_update_password() {
	var old_password = $('#old_password').val() || '';
	var new_password = $('#new_password').val() || '';
	var re_password = $('#re_password').val() || '';
	
	$('form input').attr("disabled", "true");
	if (new_password == '' || re_password == '' || new_password != re_password) {
		$('body').dialogbox({type:"error",title:"Result",message:"password can not be empty, and two input must match."});
		$('form input').removeAttr("disabled");
		return ;
	}
	var ajax = $.ajax({
		type: "POST",
		url: '/api/set_pwd',
		data: {
			'old_password': hex_md5(old_password), 
			'new_password': hex_md5(new_password),
			're_password': hex_md5(re_password),
		},
		success: function(data) {
			if (data.success == 1) {
				location.href = data.data;
			}
			else {
				$('form input').removeAttr("disabled");
				$('body').dialogbox({type:"error",title:"Result",message:data.data});
			}
		}, 
		dataType: 'json',
		async: true,
	});
}