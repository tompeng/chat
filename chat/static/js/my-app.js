/**
 * Created by Tom on 2016-12-09.
 */

(function (Framework7) {

	$$ = Dom7;

    var socket = new WebSocket("ws://" + window.location.host + "/chat-dev2/");

    var myApp = new Framework7({
		uniqueHistory: true,
		uniqueHistoryIgnoreGetParameters: true,
		cache: false,
        onPageInit: function (app, page) {
            if (page.name === "index") {
                app.messages('.messages').scrollMessages();
            }
        }
	});

	var mainView = myApp.addView('.view-main', {
		// Because we use fixed-through navbar we can enable dynamic navbar
		dynamicNavbar: true,
	});

    var myMessages = myApp.messages('.messages', {
        autoLayout: true
    });

    $$("#button_send").on('click', function() {
        var msg = $$("#input_message").val();
        if(msg === "") {
            myApp.alert("Can't send an empty text.", "Send Error");
        } else {
            myMessages.appendMessage({
                text: msg,
                type: "sent",
                name: "Me"
            });

            var user = $$("#current_user").data("user");
            if (user === "Anonymous") {
                user += "_" + guid();
                $$("#current_user").data("user", user);
            }

            $$("#input_message").val("");

            var json_msg = JSON.stringify({
                text: msg,
                user: user,
            })
            socket.send(json_msg);
        }
    });


    $$("#input_message").keypress(function (e) {
        if (e.which == 13 && !e.shiftKey) {
            $$("#button_send").click();
            e.preventDefault();
            return false;
        }
    });


    socket.onmessage = function (e) {
        var data = JSON.parse(e.data);

        if (data.user === $$("#current_user").data("user")) {
            // the message is from myself
            return;
        } else {
            var sender = data.user.startsWith("Anonymous_") ? "Anonymous" : data.user;

            myMessages.appendMessage({
                text: data.text,
                type: "received",
                name: sender,

            });
        }
    }

    $$('.button-login').on('click', function () {
        myApp.prompt('What is your name?', 'Login',
            function (value) {
                if(value === "") {
                    myApp.alert("No username provided.", "Login Error");
                } else {
                    $$("#current_user").text("Logged in as: " + value);
                    $$("#current_user").data("user", value);
                    $$('.button-login').text("Switch user");
                }
            },
            function (value) {
                return;
            }
        );
    });


}(Framework7));


function guid() {
    function s4() {
        return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1);
    }

    return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
        s4() + '-' + s4() + s4() + s4();
}