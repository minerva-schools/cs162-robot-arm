$(document).ready(function () {
    // log-in form display
    $('.log_in_button').click(function () {
        console.log("WORK !!!");
        $("#myForm").css({display: "block"});
        $('.form-parent').css({visibility: "visible"});
    });
    $('.cancel').click(function () {
        $("#myForm").css({display: "none"});
        $('.form-parent').css({visibility: "hidden"});
    });

    // toggle the settings dropdown
    $('.settings_button').click(function () {
        console.log("FUNCTION CALLED!");
        if ($('.settings_dropdown').css("visibility") == "hidden") {
            console.log("SHOWING");
            $('.settings_dropdown').css({
                visibility: 'visible',
                opacity: 0
            }).animate({
                opacity: 1
            }, 300);
        } else {
            console.log("HIDING!");
            $('.settings_dropdown').css({
                opacity: 1
            }).animate({
                opacity: 0
            }, 300, function () {
                $('.settings_dropdown').css({
                    visibility: 'hidden'
                });
            });
        }
    });
});
