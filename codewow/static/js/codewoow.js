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
                    cur.attr('class', 'unfollow').html("<span></span>"+data.msg)
                } else{
                    cur.attr('class', 'follow').html("<span></span>"+data.msg)
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

    $(function(){
        $("form div.tagCloud1 a").click(function(){
            var tag = $(this).text()
            var old = $(".tagInput").val();
            if (old.trim() == ""){
                newtags = tag; 
            } else{
                newtags = old + " " + tag;
            }
            $(".tagInput").val(newtags);
            return false;
        });
    });

// message effect
     $(function() {
         function disappear() {
             $('#flashed').fadeTo('slow', 0.8).fadeTo('slow', 0.4).fadeTo('slow', 0.2).fadeOut('fast');
         }
 
         setTimeout(disappear, 1300);
     });

// share code select

   // $(function(){
        var btnDrop = $('#dorpDown .dorpDownFire');
        var dorpMenu = $('#dorpDown .dorpDownList');
        var userInput = $('#dorpDown .searchMenu input');
        var searchResult = $('#dorpDown .searchResult');

        var optionGroup = $('#code_type option');
        var len = optionGroup.length;
        var arrOption = [];
        var lcArr = [];

        var resultArr = [];

        for(var i = 0;i<len;i++){
             var tmp = optionGroup.eq(i).text();
             arrOption.push(tmp);
             lcArr.push(tmp.toLowerCase());
             searchResult.append('<li>'+ tmp + '</li>');
        }
       // alert(typeof arrOption[1]);
        btnDrop.click(function(){
            btnDrop.children('div').toggleClass('up');
            dorpMenu.toggle();
        });

        //pick value
        $('li',searchResult).live('click',function(){  
            var txt = $(this).text();
            btnDrop.children('p').text(txt);
            for(var i =0;i<len;i++){
                if(arrOption[i] == txt){
                    optionGroup.eq(i).attr('selected',true);
                }
            }
            dorpMenu.hide();
            userInput.val('');
            searchResult.children().remove();
        });
        
        userInput.keyup(function(){
            searchResult.children().remove();
            if(userInput.val()!=''){
               var txt = userInput.val().toLowerCase();
            } 
            for(var i = 0; i <len; i++){
                if(lcArr[i].indexOf(txt) == 0){
                   searchResult.append('<li>'+ arrOption[i]+ '</li>');
                }
            }

        });
   // });
		
})
