function cancel_register() {
  $("#myFormRegister").css({
      display: "none"
  });
  $('.form-parent-register').css({
      visibility: "hidden"
  });
}

function cancel_login() {
  $("#myForm").css({
      display: "none"
  });
  $('.form-parent').css({
      visibility: "hidden"
  });

  $('.login_message').remove();
}

function from_angles() {
    $('.c_coordinates').css({
        visibility: "hidden"
    });
    $('.c_angles').css({
        visibility: "visible"
    });
    $('.ct_a').css({
        "background-color": "white",
        "color": "var(--dark-grey)",
        "z-index": 3
    });
    $('.ct_c').css({
        "background-color": "var(--dark-grey)",
        "color": "white",
        "z-index": 2
    });
    $('.ct_c').hover(function() {
        $(this).css({"cursor": "pointer"})
    });
}

function from_coordinates() {
    $('.c_angles').css({
        visibility: "hidden"
    });
    $('.c_coordinates').css({
        visibility: "visible"
    });
    $('.ct_c').css({
        "background-color": "white",
        "color": "var(--dark-grey)",
        "z-index": 3
    });
    $('.ct_a').css({
        "background-color": "var(--dark-grey)",
        "color": "white",
        "z-index": 2
    });
    $('.ct_a').hover(function() {
        $(this).css({"cursor": "pointer"})
    });
}

$(document).ready(function () {

    // log-in form display
    // TEMPORARY login form redirect fix
    // $('.form-container').submit(function(e) {
    //     e.preventDefault();
    //     window.location.href = 'main.html';
    // });

    $('.register_button').click(function () {
        console.log("WORK !!!");
        $("#myFormRegister").css({
            display: "block"
        });
        $('.form-parent-register').css({
            visibility: "visible"
        });
    });

    $('.log_in_button').click(function () {
        console.log("WORK !!!");
        $("#myForm").css({
            display: "block"
        });
        $('.form-parent').css({
            visibility: "visible"
        });
    });

    $('.from_login').click(
      cancel_login
    );

    $('.cancel').click(
      cancel_login
    );

    $('.cancel').click(
      cancel_register
    );


    // upload-file form display
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
        var time_int = 1;
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
    from_angles()
    var controls = "angles";

    $('.ct').click(function () {
        if (controls == "angles") {
            from_coordinates()
            controls = "coordinates"
        } else if (controls == "coordinates") {
            // $('.main_buttons').removeClass('right_buttons').addClass('left_buttons');
            from_angles()
            controls = "angles";
        }
    });

    $('#myForm').validate();

});

// Countdown Timer
// Set the date we're counting down to
var countDownDate = new Date("Jun 5, 2021 15:15:15").getTime();

// Update the count down every 1 second
var x = setInterval(function() {

  // Get today's date and time
  var now = new Date().getTime();

  // Find the distance between now and the count down date
  var distance = countDownDate - now;

  // Time calculations for days, hours, minutes and seconds
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);

  // Output the result in an element with id="demo"
  document.getElementById("demo").innerHTML = minutes + "m " + seconds + "s ";

  // If the count down is over, write some text
  if (distance < 0) {
    clearInterval(x);
    document.getElementById("demo").innerHTML = "EXPIRED";
  }
}, 1000);
