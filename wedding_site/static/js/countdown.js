var weddingDate = new Date("April 29, 2017 14:30:00");

// padding options
var three_digit_pad = "150px";
var two_digit_pad = "195px";
var one_digit_pad = "240px";

var updateDisplay = function() {
    var diff = weddingDate - new Date();

    if (diff < 0) {
        $(".image-div").attr("title", "It's already happened! We're married!");
        $("#days").text("0");
        $("svg").css("padding-left", one_digit_pad);
        return;
    }

    var days = Math.floor(diff / (1000 * 60 * 60 * 24));
    var hours = Math.floor(diff / (1000 * 60 * 60));
    hours = hours - (days * 24);
    var mins = Math.floor(diff / (1000 * 60));
    mins = mins - (hours * 60) - (days * 24 * 60);

    var addDay = (hours > 12);

    if (hours < 10) {
        hours = "0" + hours;
    }
    if (mins < 10) {
        mins = "0" + mins;
    }

    var countdown = days + " days, " + hours + ":" + mins;
    $(".image-div").attr("title", countdown);

    if (addDay) {
        days = days + 1;
    }
    $("#days").text(days);
    if (days >= 100) {
        $("svg").css("padding-left", three_digit_pad);
    } else if (days >= 10) {
        $("svg").css("padding-left", two_digit_pad);
    } else {
        $("svg").css("padding-left", one_digit_pad);
    }
};

$(function() {
    updateDisplay();

    setInterval(updateDisplay, 1000);
});
