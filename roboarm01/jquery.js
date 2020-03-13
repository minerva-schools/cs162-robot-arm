$(document).ready(function () {

    // log-in form display
    $('.log_in_button').click(function () {
        console.log("WORK !!!");
        $("#myForm").css({
            display: "block"
        });
        $('.form-parent').css({
            visibility: "visible"
        });
    });
    $('.cancel').click(function () {
        $("#myForm").css({
            display: "none"
        });
        $('.form-parent').css({
            visibility: "hidden"
        });
    });


    // log-in form display
    $('.upload_button').click(function () {
        console.log("WORK !!!");
        $("#UploadFile").css({
            display: "block"
        });
        $('.form-parent').css({
            visibility: "visible"
        });
    });
    $('.cancel').click(function () {
        $("#UploadFile").css({
            display: "none"
        });
        $('.form-parent').css({
            visibility: "hidden"
        });
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

    // loading animation
    $('.loader').ready(function () {
        var time_int = 60;
        loader = setInterval(progress, time_int);
        console.log("LOADING - STEP 1");
    });

    function progress() {
        var p_current = parseInt($('.loader_bar').attr("value")),
            p_new = p_current + 1;
        $('.loader_bar').attr("value", p_new);
        console.log(p_new);
        switch (p_new) {
            case 15:
                $('.loader_text').text("Loading...");
                break;
            case 25:
                $('.loader_text').text("Looking for a free robot arm...");
                break;
            case 60:
                $('.loader_text').text("Connecting you to your robot arm...");
                break;
            case 90:
                $('.loader_text').text("Just a sec...");
                break;
            case 100:
                clearInterval(loader);
                $('.loader').css({
                    visibility: "hidden"
                });
                break;
        }
    }

    // change of controls
    $('.main_button').ready(function () {
        $('.main_button').css({
            visibility: "hidden"
        });
    });
    var controls = "sliders";

    $('.change_controls').click(function () {
        if (controls == "sliders") {
            $('.main_button').css({
                visibility: "visible"
            });
            $('.slider').css({
                visibility: "hidden"
            });
            $('.slider1').css({
                visibility: "hidden"
            });
            controls = "buttons";
        } else {
            $('.main_button').css({
                visibility: "hidden"
            });
            $('.slider').css({
                visibility: "visible"
            });
            $('.slider1').css({
                visibility: "visible"
            });
            controls = "sliders";
        }
    });

    $('#myForm').validate();


});
