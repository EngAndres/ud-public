/*
This is a simple example of a web service for Python into PacketTracer.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
*/

function setup() {
	HTTPServer.route("/healthcheck", function(url, res) {
		Serial.println("Test services");
		res.setContentType("text/plain");
		res.send("This is a verification about javascript services");
	});
	
	// start server on port 80
	HTTPServer.start(80);
}