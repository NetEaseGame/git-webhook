//点击添加按钮
function add_update_githook() {
	var repo_name = $('#repo_name').val() || '';
	var githook_sh = $('#githook_sh').val() || '';
	$('#repo_name').attr("disabled", "true");
	$('#githook_sh').attr("disabled", "true");
	if (repo_name == '') {
		$('body').dialogbox({type:"error",title:"Result",message:"repo_name can not be empty."});
		$('#repo_name').removeAttr("disabled");
		$('#githook_sh').removeAttr("disabled");
		return ;
	}
	$('body').dialogbox({type:"text",title:"please input the passwrod.", message:"passwrod needed"}, function($btn, $ans) {
        if($btn == "close") {
        	$('#repo_name').removeAttr("disabled");
    		$('#githook_sh').removeAttr("disabled");
            return;
        }
        else if($btn == "ok") {
		  	if ($ans == null || $ans == "") {
		  		$('body').dialogbox({type:"error",title:"Result",message:"password is empty."});
		  		$('#repo_name').removeAttr("disabled");
				$('#githook_sh').removeAttr("disabled");
		  		return;
		    }
		  	else {
		  		var ajax = $.ajax({
					type: "POST",
					url: '/api/add',
					data: {'repo_name': repo_name, 'githook_sh': githook_sh, 'password': hex_md5($ans)},
					success: function(data) {
						if (data.success == 1) {
							location.reload();
						}
						else {
							$('#repo_name').removeAttr("disabled");
							$('#githook_sh').removeAttr("disabled");
							$('body').dialogbox({type:"error",title:"Result",message: data.data});
						}
					}, 
					dataType: 'json',
					async: false,
				});
		  	}
        }
    });
}

$('.del_btn').click(function() {
	var md5 = $(this).attr('md5');
	$('body').dialogbox({type:"text",title:"please input the passwrod.", message:"passwrod needed"}, function($btn, $ans) {
        if($btn == "close") {
            return;
        }
        else if($btn == "ok") {
		  	if ($ans == null || $ans == "" || $ans == undefined) {
		  		$('body').dialogbox({type:"error",title:"Result",message: 'password is empty.'});
		  		return;
		    }
		  	else {
		  		var ajax = $.ajax({
		  			type: "POST",
		  			url: '/api/del',
		  			data: {'md5': md5, 'password': hex_md5($ans)},
		  			success: function(data) {
		  				if (data.success == 1) {
		  					location.reload();
		  				}
		  				else {
		  					$('body').dialogbox({type:"error",title:"Result",message: data.data});
		  				}
		  			}, 
		  			dataType: 'json',
		  			async: false,
		  		});
		  	}
        }
    });
});