$(document).ready(function () {
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
                visibility: 'hidden'});
            });
        }
    });
});
