$(document).ready(function(){
	//rSection height adjust
	$(".rSection").height($("#content").innerHeight() - 20);
	//comment hover
	$(".commentCell").hover(function(){
		$(this).children(".commentCell .delete, .commentCell .reply").show();
	},function(){
		$(this).children(".commentCell .delete, .commentCell .reply").hide();
	});
	//comment reply&delete
	$(".commentCell .reply").click(function(){
		var nickname = $(this).prev().children("a").text();
        var area = $(".lSection .commentBox textarea");
        var old = area.val() 
        area.val("@" + nickname + " " + old);
        return false;
	});

	//btn follow&unfollow
	$(".follow, .unfollow").live('click', function(){
        var cur = $(this);
        var url = $(this).attr('href');
        $.getJSON(url, function(data){
            if (data.success){
                if (data.op == 'follow'){
                    cur.attr('class', 'unfollow').html("<span></span>unfollow")
                } else{
                    cur.attr('class', 'follow').html("<span></span>follow")
                }
                $(".rSection .followCount p:first").text(data.follow_num);
            } else {
                if (data.code == 401){
                    window.location = "/login";
                } else{
                    alert(data.error);
                }
            }
        });
        return false;
	});

	//share page add/remove tags
	$("form .myTagCloud a").live("click",function(){
		$(this).parent().remove();
        return false;
	}); 


	$("form .tagInput").keypress(function(event){
		var myTags = $("form .myTagCloud");
		var newTag = $("<div></div>")
		if(event.which == 13 && $(this).val()){
			newTag.append("<span>" + $(this).val() + "</span><a href='#'></a>");
			myTags.append(newTag);
		}
	});

    // up down gist 
    $(function(){
        $(".up").click(function(){
            var cur = $(this);
            var url = cur.attr('href');
            $.getJSON(url, function(data){
                if (data.success) {
                    cur.next("p").text(data.up_num);
                    cur.parent().next().find("p").text(data.down_num);
                } else {
                    if (data.code == 401){
                        window.location = "/login";
                    } else{
                        alert(data.error);
                    }
                }
            });
            return false;
        });

        $(".down").click(function(){
            var cur = $(this);
            var url = cur.attr('href');
            $.getJSON(url, function(data){
                if (data.success){
                    cur.next("p").text(data.down_num);
                    cur.parent().prev().find("p").text(data.up_num);
                } else{
                    if (data.code == 401){
                        window.location = "/login";
                    } else{
                        alert(data.error);
                    }
                }
            });
            return false;
        });
    });
		
})
