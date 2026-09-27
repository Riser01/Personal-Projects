    var mysql = require('mysql');

    var monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];


    var a = ['', 'First ', 'Secound ', 'third ', 'fourth ', 'fifth  ', 'sixth ', 'seventh ', 'eighth ', 'ninth ', 'tenth ', 'eleveth ', 'twelfth ', 'thirteenth ', 'fourteenth ', 'fifteenth ', 'sixteenth ', 'seventeenth ', 'eighteenth ', 'nineteenth '];
    var b = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'];


    // var con = mysql.createConnection({
    //     host: "52.88.238.28",
    //     user: "test",
    //     password: "9874123650"
    // });
     var con = mysql.createConnection({
        host: process.env.DBhost,
        user: process.env.User,
        password: String(process.env.Password)
    });
    exports.handler = function(event, context) {
        try {
            console.log("famous lives");
            console.log("event.session.application.applicationId=" + event.session.application.applicationId);
            console.log(event);
            console.log(context);
            console.log(event.request.type);

            if (event.request.type === "LaunchRequest") {
                onLaunch(event.request,
                    event.session,
                    function callback(sessionAttributes, speechletResponse) {
                        context.succeed(buildResponse(sessionAttributes, speechletResponse));
                    });
            } else if (event.request.type === "IntentRequest") {
                onIntent(event.request,
                    event.session,
                    function callback(sessionAttributes, speechletResponse) {
                        context.succeed(buildResponse(sessionAttributes, speechletResponse));
                    });
            } else if (event.request.type === "SessionEndedRequest") {
                onSessionEnded(event.request, event.session);
                context.succeed();
            }
        } catch (e) {
            try {

                getdata(event.request.intent, event.session, function callback(sessionAttributes, speechletResponse) {
                    context.succeed(buildResponse(sessionAttributes, speechletResponse));
                });
            } catch (r) {
                End(event.request.intent, event.session, function callback(sessionAttributes, speechletResponse) {
                    context.succeed(buildResponse(sessionAttributes, speechletResponse));
                });


            }
        }
    };

    /**
     * Called when the session starts.
     */
    function onSessionStarted(sessionStartedRequest, session) {
        console.log("onSessionStarted requestId=" + sessionStartedRequest.requestId +
            ", sessionId=" + session.sessionId);
    }

    /**
     * Called when the user launches the skill without specifying what they want.
     */
    function onLaunch(launchRequest, session, callback) {
        // Dispatch to your skill's launch.
        conform(callback);
    }

    /**
     * Called when the user specifies an intent for this skill.
     */
    function onIntent(intentRequest, session, callback) {

        var intent = intentRequest.intent,
            intentName = intentRequest.intent.name;

        // Dispatch to your skill's intent handlers
        switch (intentName) {
            case "conform":
                //getdata(intent, session, callback);
                getdataCountry(intent, session, callback);
                break;
            case "getdataCountry":
                getdataCountry(intent, session, callback);
                break;

            case "AMAZON.CancelIntent":
                Wrong(intent, session, callback);
                break;

            case "AMAZON.StopIntent":
                End(intent, session, callback);
                break
            case "AMAZON.FallbackIntent":

            default:
                Wrongagain(intent, session, callback);
                break;

        }
    }

    /**
     * Called when the user ends the session.
     * Is not called when the skill returns shouldEndSession=true.
     */
    function onSessionEnded(sessionEndedRequest, session) {
        console.log("onSessionEnded requestId=" + sessionEndedRequest.requestId +
            ", sessionId=" + session.sessionId);
        // Add cleanup logic here
    }

    // --------------- Functions that control the skill's behavior -----------------------

    function conform(callback) {
        // If we wanted to initialize the session to have some attributes we could add those here.
        var sessionAttributes = {};
        var cardTitle = "Welcome to Famous Lives";
        var speechOutput = "Welcome. would u like to know the famous people who were born today";
        // If the user either does not reply to the welcome message or says something that is not
        // understood, they will be prompted again with this text.
        var repromptText = "would u like to know the famous people who were born today";
        var shouldEndSession = false;

        callback(sessionAttributes,
            buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
    }


    function End(intent, session, callback) {

        var cardTitle = "Thank You";
        var repromptText = null;
        var sessionAttributes = {};
        var shouldEndSession = true;
        var speechOutput = "Thank Your for using Famous Lives";



        // Setting repromptText to null signifies that we do not want to reprompt the user.
        // If the user does not respond or says something that is not understood, the session
        // will end.
        callback(sessionAttributes,
            buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
    }



    function Wrong(intent, session, callback) {

        var cardTitle = "Paused";
        var speechOutput = "Please tell me when u want to continue";
        var sessionAttributes = {};
        var shouldEndSession = false;
        var repromptText = "waiting to continue";


        // Setting repromptText to null signifies that we do not want to reprompt the user.
        // If the user does not respond or says something that is not understood, the session
        // will end.
        callback(sessionAttributes,
            buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
    }

    function Wrongagain(intent, session, callback) {

        var cardTitle = intent.name;
        var speechOutput = "Please try again";
        var sessionAttributes = {};
        var shouldEndSession = false;
        var repromptText = "waiting to continue";


        // Setting repromptText to null signifies that we do not want to reprompt the user.
        // If the user does not respond or says something that is not understood, the session
        // will end.
        callback(sessionAttributes,
            buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
    }

    function NoEntry(intent, session, callback) {

        var cardTitle = intent.name;
        var speechOutput = "Sorry No one found ,try again later ";
        var sessionAttributes = {};
        var shouldEndSession = false;
        var repromptText = "Sorry No one found ,try again later ";


        // Setting repromptText to null signifies that we do not want to reprompt the user.
        // If the user does not respond or says something that is not understood, the session
        // will end.
        callback(sessionAttributes,
            buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
    }



    // --------------- Helpers that build all of the responses -----------------------

    function buildSpeechletResponse(title1, output, repromptText, shouldEndSession) {
        return {
            outputSpeech: {
                type: "SSML",
                ssml: "<speak>" + output + "</speak>"
            },
            card: {
                type: "Standard",
                title: "Famous Lives",
                content: "Famous  Birthdays",
                text: title1,
                image: {
                    smallImageUrl: "https://i.pinimg.com/236x/5e/8a/e6/5e8ae61b292c4d956e18345b17338fea--letter-l-logo-ideas.jpg",
                    largeImageUrl: "https://i.pinimg.com/236x/5e/8a/e6/5e8ae61b292c4d956e18345b17338fea--letter-l-logo-ideas.jpg"
                }
            },
            reprompt: {
                outputSpeech: {
                    type: "PlainText",
                    text: repromptText
                }
            },
            shouldEndSession: shouldEndSession
        }
    }

    function buildResponse(sessionAttributes, speechletResponse) {
        return {
            version: "1.0",
            sessionAttributes: sessionAttributes,
            response: speechletResponse
        }
    }

    //db function
    function getdata(intent, session, callback) {
        console.log("get data start");
        var datetime = new Date();
        try {
            console.log(intent.name);
            con.query("SELECT Name,COUNTRY,TAGS FROM Famous_Lives.bdays_v1 WHERE DAY=" + (parseInt(datetime.getDate())) + " AND MONTH=" + (parseInt(datetime.getMonth()) + 1) + " ORDER BY RAND() LIMIT 5;", function(err, result, fields) {
                if (err != null || err == "")
                    console.log("err:" + err);
                console.log("get data quired");

                buildSpeechletResponsequrey(result, intent, session, callback);


            });
        } catch (e) {
            Wrongagain(intent, session, callback);
        }
    }

    function getdataCountry(intent, session, callback) {
        console.log("start getdata country");
        try {
            var c = intent.slots.Country.value != null ? toTitleCase(intent.slots.Country.value) : "";
        } catch (e) {
            var c = "";
            console.log("error" + e);
        }
        try {
            var t = intent.slots.Tag.value != null ? toTitleCase(intent.slots.Tag.value) : "";
        } catch (e) {
            var t = "";
            console.log("error" + e);
        }
        try {
            var n = intent.slots.Name.value != null ? toTitleCase(intent.slots.Name.value) : "";
        } catch (e) {
            var n = "";
            console.log("error" + e);
        }
        try {
            var d = intent.slots.Date.value != null ? datecon(intent.slots.Date.value) : ["", ""];
        } catch (e) {
            var d = ["", ""];
            console.log(e);
            console.log("error" + e);
        }
        var datetime = new Date();
        //console.log("date before:"+intent.slots.Date.value);
        console.log("country=" + t);
        if (d[0] == "")
            d[0] = datetime.getDate();
        if (d[1] == "")
            d[1] = (parseInt(datetime.getMonth()) + 1).toString();
        //console.log(d[0]+" dsd "+d[1]);
        //optimisation required here
        if (n == "") {
            try {
                console.log("here sql: " + "SELECT Name,COUNTRY,TAGS FROM Famous_Lives.bdays_v1 WHERE DAY=" + (parseInt(d[0])) + " AND MONTH=" + (parseInt(d[1])) + " AND COUNTRY LIKE '%" + c + "%' AND upper(TAGS) LIKE '%" + t.toUpperCase() + "%' AND upper(Name) LIKE '%" + n.toUpperCase() + "%' ORDER BY RAND() LIMIT 5;");
                con.query("SELECT Name,COUNTRY,TAGS FROM Famous_Lives.bdays_v1 WHERE DAY=" + (parseInt(d[0])) + " AND MONTH=" + (parseInt(d[1])) + " AND COUNTRY LIKE '%" + c + "%' AND TAGS LIKE '%" + t + "%' AND Name LIKE '%" + n + "%' ORDER BY RAND() LIMIT 5;", function(err, result, fields) {
                    if (err != null || err == "")
                        console.log("err:" + err);

                    buildSpeechletResponsequreyAll(result, intent, session, callback, d);


                });
            } catch (e) {
                console.log("error" + e);
                Wrongagain(intent, session, callback);
            }
        } else {
            try {
                console.log("here sql: " + "SELECT Name,COUNTRY,TAGS,DAY,MONTH FROM Famous_Lives.bdays_v1 WHERE  COUNTRY LIKE '%" + c + "%' AND upper(TAGS) LIKE '%" + t.toUpperCase() + "%' AND upper(Name) LIKE '%" + n.toUpperCase() + "%' ORDER BY RAND() LIMIT 5;");
                con.query("SELECT Name,COUNTRY,TAGS,DAY,MONTH FROM Famous_Lives.bdays_v1 WHERE COUNTRY LIKE '%" + c + "%' AND TAGS LIKE '%" + t + "%' AND Name LIKE '%" + n + "%' ORDER BY RAND() LIMIT 5;", function(err, result, fields) {
                    if (err != null || err == "")
                        console.log("err:" + err);

                    buildSpeechletResponsequreyAllDate(result, intent, session, callback, d);


                });
            } catch (e) {
                console.log("error" + e);
                Wrongagain(intent, session, callback);
            }

        }
    }


    function buildSpeechletResponsequrey(result, intent, session, callback) {
        var output = "";
        var text = "";
        if (result == null)
            NoEntry(intent, session, callback);

        for (var i = 0; i < 5; i++) {
            var value = result[i];
            //var name1=(value.Name+"");
            //output=output+name1+"";
            var name = (value.Name + "").split(",");
            var Country = (value.COUNTRY + "");
            //output=output+Country+"";
            var lastcom = Country.lastIndexOf(",");
            if (lastcom > 0)
                Country = setCharAt(Country, lastcom, " and ");
            var Tags = (value.TAGS + "");
            //output=output+Tags+"";
            lastcom = Tags.lastIndexOf(",");
            if (lastcom > 0)
                Tags = setCharAt(Tags, lastcom, " and ");
            output = output + "<p><emphasis level=\"moderate\">" + name[0] + "</emphasis>," + Country + " was born today . was a famous " + Tags + " , was " + Country + " .<break time=\"1s\"/></p>";
            text = text + (i + 1).toString() + ". " + name[0] + "\n" + Tags + "\n";
        }

        var cardTitle = "Famous Lives";
        var speechOutput = output;
        var sessionAttributes = {};
        var shouldEndSession = false;
        var repromptText = "would u like to know more";


        // Setting repromptText to null signifies that we do not want to reprompt the user.
        // If the user does not respond or says something that is not understood, the session
        // will end.

        callback(sessionAttributes, buildSpeechletResponse(text, speechOutput, repromptText, shouldEndSession));


    }


    function buildSpeechletResponsequreyAll(result, intent, session, callback, date = null) {
        console.log("buildSpeechletResponsequreyAll"+process.env.User);
        var output = "";
        var text = "";
        if (result == null || result.length == 0)
            NoEntry(intent, session, callback);
        var datewords = "on " + inWords(date[0]) + " " + monthNames[parseInt(date[1]) - 1]; // here
        console.log(result.length);

        for (var i = 0; i < result.length; i++) {
            var value = result[i];
            //var name1=(value.Name+"");
            //output=output+name1+"";
            var Country = (value.COUNTRY + "");
            var name = (value.Name + "").split(",");

            //output=output+Country+"";
            var lastcom = Country.lastIndexOf(",");
            if (lastcom > 0)
                Country = setCharAt(Country, lastcom, " and ");
            var Tags = (value.TAGS + "");
            //output=output+Tags+"";
            lastcom = Tags.lastIndexOf(",");
            if (lastcom > 0)
                Tags = setCharAt(Tags, lastcom, " and ");
            output = output + "<p><emphasis level=\"moderate\">" + name[0] + "</emphasis>," + Country + " was born " + datewords + " , was a famous " + Tags + " .<break time=\"1s\"/></p>";
            text = text + (i + 1).toString() + ". " + name[0] + "\n" + Tags + "\n";
        }

        var cardTitle = "Famous Lives";
        var speechOutput = output;
        var sessionAttributes = {};
        var shouldEndSession = false;
        var repromptText = "would u like to know more";


        // Setting repromptText to null signifies that we do not want to reprompt the user.
        // If the user does not respond or says something that is not understood, the session
        // will end.

        callback(sessionAttributes, buildSpeechletResponse(text, speechOutput, repromptText, shouldEndSession));


    }


    function buildSpeechletResponsequreyAllDate(result, intent, session, callback, date = null) {
        console.log("buildSpeechletResponsequreyAllDate");
        var output = "";
        var text = "";
        if (result == null || result.length == 0)
            NoEntry(intent, session, callback);
        //var datewords = "on " + inWords(date[0]) + " " + monthNames[parseInt(date[1])-1];// here

        console.log(result.length);
        console.log(result);

        for (var i = 0; i < result.length; i++) {

            var value = result[i];
            date = [value.DAY, value.MONTH];
            //var name1=(value.Name+"");
            //output=output+name1+"";
            var Country = (value.COUNTRY + "");
            var name = (value.Name + "").split(",");

            //output=output+Country+"";
            var lastcom = Country.lastIndexOf(",");
            if (lastcom > 0)
                Country = setCharAt(Country, lastcom, " and ");
            var Tags = (value.TAGS + "");
            //output=output+Tags+"";
            lastcom = Tags.lastIndexOf(",");
            if (lastcom > 0)
                Tags = setCharAt(Tags, lastcom, " and ");
            output = output + "<p><emphasis level=\"moderate\">" + name[0] + "</emphasis>," + Country + " was born on " + inWords(date[0]) + "" + monthNames[parseInt(date[1]) - 1] + " , was a famous " + Tags + " .<break time=\"1s\"/></p>";
            text = text + (i + 1).toString() + ". " + name[0] + "\n" + Tags + "\n";
        }

        var cardTitle = "Famous Lives";
        var speechOutput = output;
        var sessionAttributes = {};
        var shouldEndSession = false;
        var repromptText = "would u like to know more";


        // Setting repromptText to null signifies that we do not want to reprompt the user.
        // If the user does not respond or says something that is not understood, the session
        // will end.

        callback(sessionAttributes, buildSpeechletResponse(text, speechOutput, repromptText, shouldEndSession));


    }


    function setCharAt(str, index, chr) {
        if (index > str.length - 1) return str;
        return str.substr(0, index) + chr + str.substr(index + 1);
    }

    function toTitleCase(str) {
        //console.log("TileCase"+str);
        return str.replace(
            /\w\S*/g,
            function(txt) {
                return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
            }
        );
    }

    function datecon(str) {
        var splitstr = (str + "").split("-");
        //console.log("date con start"+splitstr);
        if (splitstr.length == 2) {
            switch (splitstr[1]) {
                case "WI":
                    return ["", "12"];
                case "SP":
                    return ["", "3"];
                case "SU":
                    return ["", "6"];
                case "FA":
                    return ["", "9"];
                default:
                    if (splitstr[1].isNaN()) {
                        splitstr[1] = splitstr[1].substr(1, splitstr[1].length);
                        return ["", String(Math.round(parseInt(splitstr[1]) / 4.3))];
                    } else
                        return ["", splitstr[1]];
            }
        } else if (splitstr.length == 3) {
            if (!splitstr[1].isNaN()) {
                //console.log("date con start"+splitstr[2]+","+ splitstr[1]);
                var test = [splitstr[2], splitstr[1]];
                //console.log("date con test"+test);
                return test;
            } else {
                splitstr[1] = splitstr[1].substr(1, splitstr[1].length);
                var test = ["", String(Math.round(parseInt(splitstr[1]) / 4.3))];
                //console.log("date con test"+test);
                return test;
            }
        }
        return ["", ""];
    }

    function inWords(num) {
        if ((num = num.toString()).length > 9) return 'overflow';
        var n = ('000000000' + num).substr(-9).match(/^(\d{2})(\d{2})(\d{2})(\d{1})(\d{2})$/);
        if (!n) return;
        var str = (n[5] != 0) ? (a[Number(n[5])] || b[n[5][0]] + ' ' + a[n[5][1]]) + '' : '';
        return str;
    }