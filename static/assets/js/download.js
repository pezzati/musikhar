function openDownload(){
    jQuery('.shadow').show().animate({
        opacity:1,
    });
    jQuery('.download').show().animate({
        opacity:1,
    });
}
function closeDownload(){
    jQuery('.shadow').animate({
        opacity:0,
    });
    jQuery('.download').animate({
        opacity:0,
    }, function(){
        jQuery('.download, .shadow').hide();
    });
}

jQuery(function($){
    $('.download .close, .shadow').click(function(){
        closeDownload();
    });
});