$(document).ready(function () {
    // toggle the add task overlay
    $('.add-task-toggle').click(function () {
        if ($('.add-task-toggle-text').text() == 'ADD') {
            $('.add-task-toggle-text').text('BACK');
            $('.add-task-overlay').css({
                visibility: 'visible',
                opacity: 0
            }).animate({
                opacity: 1
            }, 300);
            //$('.map').css('visibility', 'visible');
        } else { // switch from MAP to GAME
            $('.add-task-toggle-text').text('ADD');
            $('.add-task-overlay').css({
                opacity: 1
            }).animate({
                opacity: 0
            }, 300, function () {
                $('.add-task-overlay').css('visibility', 'hidden');
            });
            //$('.map').css('visibility', 'hidden');
        }
    });
});
