$(document).ready(function(){
	//rSection height adjust
	$(".rSection").height($("#content").innerHeight() - 20);
	//comment hover
	$(".commentCell").hover(function(){
		$(this).children("div:last").show();
	},function(){
		$(this).children("div:last").hide();
	})
	//comment reply&delete
	$(".commentCell div:last-child").click(function(event){
		event.preventDefault();
		var userID = $(this).prev().children("a").text();
		if($(this).hasClass("reply")){
			$(".lSection .commentBox textarea").val("@" + userID + ":");
		}else{
			$(this).parent().remove();
		}
	})

	//btn follow&unfollow
	$(".listCell>div:last-child>a, .articleHeader>a").click(function(event){
		event.preventDefault;
		if($(this).hasClass("unfollow")){
			$(this).text("follow").append("<span></span>").attr("class","follow");
		}else{
			$(this).children().remove();
			$(this).text("unfollow").attr("class","unfollow");
		}
	})

	//share page add/remove tags
	$("form .myTagCloud a").live("click",function(event){
		event.preventDefault;
		$(this).parent().remove();
	}) 


	$("form .tagInput").keypress(function(event){
		var myTags = $("form .myTagCloud");
		var newTag = $("<div></div>")
		if(event.which == 13 && $(this).val()){
			newTag.append("<span>" + $(this).val() + "</span><a href='#'></a>");
			myTags.append(newTag);
		}
	})
		
})