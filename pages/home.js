$(function(){
    $("#header").load("header.html"); 
    $("#footer").load("footer.html"); 
});
$(".like-btn").on("click", function () {
    var postId = $(this).data("id");
    var likeCount = $(this).siblings(".like-count");
    var likeCountValue = parseInt(likeCount.text());
    $(this).toggleClass("text-success");
    $(this).children().toggleClass("fas");
    if ($(this).hasClass("text-success")) {
        likeCount.text(likeCountValue + 1);
    } else {
        likeCount.text(likeCountValue - 1);
    }
});

$(".dislike-btn").on("click", function () {
    var postId = $(this).data("id");
    var dislikeCount = $(this).siblings(".dislike-count");
    var dislikeCountValue = parseInt(dislikeCount.text());
    $(this).toggleClass("text-danger");
    $(this).children().toggleClass("fas");
    if ($(this).hasClass("text-danger")) {
        dislikeCount.text(dislikeCountValue + 1);
    } else {
        dislikeCount.text(dislikeCountValue - 1);
    }
});