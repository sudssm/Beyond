#require "IFTTT.class.nut:1.0.0"

const SECRET_KEY = "YOUR SECRET KEY";
ifttt <- IFTTT(SECRET_KEY);


device.on("update", function(data) {
	ifttt.sendEvent("ir_led", function(err, response) {
	    if (err) {
	        server.error(err);
	        return;
	    }

	    server.log("Success!");
	});
}