
function removeCodeComments() {
    var code = $("#text_area").val();
    var lines = code.split('\n');
    lines.splice(0, 3);
    var finalCode = lines.join('\n');
    $("#text_area").val(finalCode);
}

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
            alert("Error: you are trying to ignore elements selected as exclusive: " + conflictingElements.toString());
        } else if (ignoredList.length == $("#elementslength").val()) {
            console.log($("#elementslength").val());
            alert("Error: you can't ignore all elements");
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


    $("#live_switch").click(function () { // Start or finish live session 
        if ($("#live_session_mode").val() == "1") {
            var r = confirm("Finish Live Session? Connection with the web browser will be closed but its window will remain open");
            if (!r) {
                $("#live_switch").prop('checked', true);
                return;
            }
        }
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
                    if ($("#auto_send_status").val() == "0") {
                        $("#send_code").removeClass("disabled-button");
                        $("#send_code").addClass("glow-hover");
                    }
                } else {
                    $("#live_session_mode").val("0");
                    $("#live_switch").text('Go Live');
                    $("#loadinginfo").text("Live Session Mode ended");
                    $("#custom_url_toggle").prop('disabled', false);
                    $("input:checkbox[name=custom_url_toggle]:checked").each(function () {
                        $("#custom_url").prop('disabled', false);
                    });
                    $("#live_switch_label").removeClass('glow');
                    if ($("#auto_send_status").val() == "0") {
                        $("#send_code").removeClass("disabled-button");
                        $("#send_code").addClass("glow-hover");
                    }
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
                alert("Couldn't open Hydra in: " + url);
            }
        });

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




    $("#send_code").click(function () {
        if (($("#auto_send_status").val() == "0") && ($("#live_session_mode").val() == "1")) {
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
    });

    $("#auto_send_toggle").click(function () {
        if ($("#auto_send_status").val() == "0") {
            $("#auto_send_status").val("1");
            $("#send_code").removeClass("glow-hover");
            $("#send_code").addClass("disabled-button");
        } else {
            $("#auto_send_status").val("0");
            if ($("#live_session_mode").val() == "1") {
                $("#send_code").removeClass("disabled-button");
                $("#send_code").addClass("glow-hover");
            }

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

    function changeText() {
        if ($("#generate_code").text() == ">_ Generate Code") {
            $("#generate_code").text(">_ Generate Code_");
        }
        else {
            $("#generate_code").text(">_ Generate Code");
        }
    }

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

});