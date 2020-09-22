
function removeCodeComments() {
    var code = $("#text_area").val();
    var lines = code.split('\n');
    lines.splice(0, 3);
    var finalCode = lines.join('\n');
    $("#text_area").val(finalCode);
}

function printError(message) {
    $.alert({
        title: 'Error',
        content: message,
        type: 'dark',
        escapeKey: true,
        backgroundDismiss: true,
    });
}

function printMessage(title, message) {
    $.alert({
        title: title,
        content: message,
        type: 'dark',
        escapeKey: true,
        backgroundDismiss: true,
    });
}

function printConfirm(title, message) {
    var self = this;
    self.dfd = $.Deferred();
    $.confirm({
        title: title,
        content: message,
        type: 'dark',
        escapeKey: true,
        backgroundDismiss: true,
        buttons: {
            confirm: {
                btnClass: 'btn-danger',
                action: function () { self.dfd.resolve(true); }
            },
            cancel: function () {
                self.dfd.resolve(false);
            }
        }
    });
    return self.dfd.promise();
}


includesAll = (arr, target) => target.every(v => arr.includes(v));

function on() {
    document.getElementById("overlay").style.display = "block";
    document.getElementById("loader").style.display = "block";
}

function off() {
    document.getElementById("overlay").style.display = "none";
    document.getElementById("loader").style.display = "none";
}

$(document).ready(function () {

    removeCodeComments()

    var allSources = []
    var allFunctions = []
    $('#exclusivesources option').each(function () {
        allSources.push($(this).val());
    });
    $('#exclusivefunctions option').each(function () {
        allFunctions.push($(this).val());
    });

    $("#generate_code").click(function () { // start live session or send new code to one
        var ignoredList = []
        var exclusiveSourcesList = []
        var exclusiveFunctionsList = []
        $('#ignorelist option:selected').each(function () {
            ignoredList.push($(this).val());
        });
        $('#exclusivesources option:selected').each(function () {
            exclusiveSourcesList.push($(this).val());
        });
        $('#exclusivefunctions option:selected').each(function () {
            exclusiveFunctionsList.push($(this).val());
        });

        var conflictingElements = [];
        for (var i = 0; i < ignoredList.length; i++) {
            if (exclusiveSourcesList.includes(ignoredList[i]) || exclusiveFunctionsList.includes(ignoredList[i])) {
                conflictingElements.push(ignoredList[i]);
            }
        }
        if (conflictingElements.length > 0) {
            printError("You are trying to ignore elements selected as exclusive: " + conflictingElements.toString());
        } else if (ignoredList.length == $("#elementslength").val()) {
            printError("You can't ignore all elements");
        } else if (allSources.every(i => ignoredList.includes(i))) {
            printError("You can't ignore all sources");
        } else if (allFunctions.every(i => ignoredList.includes(i))) {
            printError("You can't ignore all functions");
        } else {
            on()
            var url = $("#defaulturl").val()
            $("input:checkbox[name=custom_url_toggle]:checked").each(function () {
                url = $("#custom_url").text();
            });

            $.ajax({
                url: '',
                type: "POST",
                data: {
                    csrfmiddlewaretoken: $("#csrf").val(),
                    generate_code: true,
                    live_session_mode: $("#live_session_mode").val(),
                    auto_send_status: $("#auto_send_status").val(),
                    code: $('#text_area').val(),
                    fmin: $("#fmin").val(),
                    fmax: $("#fmax").val(),
                    amin: $("#amin").val(),
                    amax: $("#amax").val(),
                    arrowprob: $("#arrowprob").val(),
                    mouseprob: $("#mouseprob").val(),
                    modulateitselfprob: $("#modulateitselfprob").val(),
                    ignored: ignoredList.toString(),
                    exclusivesources: exclusiveSourcesList.toString(),
                    exclusivefunctions: exclusiveFunctionsList.toString(),
                    hidecodestatus: $("#hide_code_status").val(),

                },
                dataType: 'json',
                complete: function (data) {
                    $("#text_area").html(data['responseJSON']['code']);
                    $('#text_area').val(data['responseJSON']['code']);
                    removeCodeComments()
                    $("#loadinginfo").addClass('text-success').removeClass('text-primary');
                    $("#loadinginfo").text("Code generated");
                    $("#loadinginfo").fadeOut(2000);
                    off()
                }
            });
        }
    });

    function live_switch_handler() {
        url = $("#defaulturl").val()
        if ($("#live_session_mode").val() == "0") {
            $("#custom_url_toggle").prop('disabled', true);
            $("input:checkbox[name=custom_url_toggle]:checked").each(function () {
                $("#custom_url").prop('disabled', true);
                url = $("#custom_url").val();
            });
            $("#loadinginfo").text("Starting Live Session Mode...");
        } else {
            $("#loadinginfo").text("Ending Live Session Mode...");
        }
        on()
        $("#loadinginfo").addClass('text-primary').removeClass('text-success');
        $("#loadinginfo").show();
        $.ajax({
            url: '',
            type: "POST",
            data: {
                csrfmiddlewaretoken: $("#csrf").val(),
                live_switch: true,
                code: $(".code").text(),
                live_session_mode: $("#live_session_mode").val(),
                hidecodestatus: $("#hide_code_status").val(),
                hydraurl: url,

            },
            dataType: 'json',
            success: function (data) {
                if ($("#live_session_mode").val() == "0") {
                    $("#live_session_mode").val("1");
                    $("#live_switch").text('Stop Live');
                    $("#loadinginfo").text("Live Session Mode started!");
                    $("#live_switch_label").addClass('glow');
                    $("#send_code").removeClass("disabled-button");
                    $("#send_code").addClass("glow-hover");
                } else {
                    $("#live_session_mode").val("0");
                    $("#live_switch").text('Go Live');
                    $("#loadinginfo").text("Live Session Mode ended");
                    $("#custom_url_toggle").prop('disabled', false);
                    $("input:checkbox[name=custom_url_toggle]:checked").each(function () {
                        $("#custom_url").prop('disabled', false);
                    });
                    $("#live_switch_label").removeClass('glow');                
                    $("#send_code").removeClass("glow-hover");
                    $("#send_code").addClass("disabled-button");
                }
                $("#loadinginfo").addClass('text-success').removeClass('text-primary');
                $("#loadinginfo").fadeOut(2000);
                off()
            },
            error: function () {
                $("#live_session_mode").val("0");
                $("#live_switch").text('Go Live');
                $("#loadinginfo").text("Live Session Mode ended");
                $("#custom_url_toggle").prop('disabled', false);
                $("input:checkbox[name=custom_url_toggle]:checked").each(function () {
                    $("#custom_url").prop('disabled', false);
                });
                printError("Couldn't open Hydra in: " + url);
            }
        });
    }

    $("#live_switch").click(function () { // Start or finish live session 
        if ($("#live_session_mode").val() == "1") {
            $("#live_switch").prop('checked', true);
            printConfirm("Finish Live Session?", "Hydra window will be closed")
                .then(function (status) {
                    if (!status) {
                        return;
                    } else {
                        $("#live_switch").prop('checked', false);
                        live_switch_handler()
                        printMessage("Finished", "Live Session was finished");
                    }
                });
        } else {
            live_switch_handler()
        }
    });

    $("#hide_code_toggle").click(function () {
        if ($("#hide_code_status").val() == "0") {
            $("#hide_code_status").val("1");
        } else {
            $("#hide_code_status").val("0");
        }
        if ($("#live_session_mode").val() == "1") {
            on()
            $.ajax({
                url: 'hide_code',
                type: "POST",
                data: {
                    csrfmiddlewaretoken: $("#csrf").val(),
                },
                dataType: 'json',
                complete: function (data) {
                    off()
                }
            });
        }
    });


    function send_code_handler() {
        if ($("#live_session_mode").val() == "1") {
            on()
            $('#text_area').keyup(function () {
                $('#text_area').html($(this).val());
                $('#text_area').val($(this).val());
            });
            $.ajax({
                url: '',
                type: "POST",
                data: {
                    csrfmiddlewaretoken: $("#csrf").val(),
                    send_code: true,
                    live_session_mode: $("#live_session_mode").val(),
                    hidecodestatus: $("#hide_code_status").val(),
                    code: $("#text_area").text(),
                },
                dataType: 'json',
                complete: function (data) {
                    off()
                }
            });
        }

    }

    $("#send_code").click(function () {
        send_code_handler();
    });

    $(document).keydown(function (e) { // ctrl + shift + enter
        if (e.ctrlKey && e.shiftKey && e.which == 13) {
            send_code_handler();
        }
    });

    $("#auto_send_toggle").click(function () {
        if ($("#auto_send_status").val() == "0") {
            $("#auto_send_status").val("1");
        } else {
            $("#auto_send_status").val("0");
        }
    });


    $(".custom-url-div").click(function () {
        if ($("#live_session_mode").val() == "1") {
            printError("You can't change URL while a Live Session is active.");
        }
    });

    $("#custom_url_toggle").click(function () {
        $("#custom_url").prop('disabled', function () { this.disabled = !this.disabled; });
        if ($("#custom_url").hasClass("text-secondary")) {
            $("#custom_url").removeClass("text-secondary")
            $("#custom_url").addClass("text-white")
        } else {
            $("#custom_url").removeClass("text-white")
            $("#custom_url").addClass("text-secondary")
        }

    });

    var interval;

    $('#generate_code').mouseenter(function () {
        interval = setInterval(function () {
            if ($("#generate_code").text() == ">_ Generate Code") {
                $("#generate_code").text("<_ Generate Code");
            }
            else {
                $("#generate_code").text(">_ Generate Code");
            }
        }, 2000);
    });

    $('#generate_code').mouseleave(function () {
        clearInterval(interval);
        $("#generate_code").text(">_ Generate Code");
    }
    ).mouseleave();

    $('#text_area').keyup(function () {
        $('#text_area').html($(this).val());
        $('#text_area').val($(this).val());
    });


    $("#help_button").click(function () {
        $("#help_modal").show()
    });

    $(".close").click(function () {
        $("#help_modal").hide()
    });

    window.onclick = function (event) {
        if (event.target == document.getElementById("help_modal")) {
            $("#help_modal").hide();
        }
    }

    $(document).keyup(function (e) {
        if (e.key === "Escape") {
            $("#help_modal").hide()
        }
    });

    $(".language_button").click(function () {
        $(".help_english").prop('hidden', function () { this.hidden = !this.hidden; });
        $(".help_spanish").prop('hidden', function () { this.hidden = !this.hidden; });

    });

    $(".logo-info").click(function () {
        min = Math.ceil(0);
        max = Math.floor(999999999);
        n = Math.floor(Math.random() * (max - min + 1)) + min;
        text = "Random number for you: " + n
        $(".logo-info").attr('data-original-title', text).tooltip('show');
    });

    $(".logo-info").mouseout(function () {
        $(".logo-info").tooltip('hide');
    });

    /*$(".logo-icon").mouseover(function () { //spin faster on hover
        $(".logo-icon").removeClass('logo')
        $(".logo-icon").addClass('logo-fast')
    });

    $(".logo-icon").mouseout(function () {
        $(".logo-icon").removeClass('logo-fast')
        $(".logo-icon").addClass('logo')
    });*/


});

