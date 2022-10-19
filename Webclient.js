// Dummy code snippet to connect server and fetch data

/*
*======	JSON DATA FIELDS ====================
*
* 	data['mode']    =  vehicle mode name
*  	data['roll']    = roll angle 
*       data['pitch']   = pitch angle
*       data['yaw']     = yaw angle
*       data['heading'] = vehicle heading
*       data['long']    = current longitude
*       data['lat']     = current latitude
*       data['alt']     = current altitude
*============================================
*/

var net = require('net');

var client = new net.Socket();
client.connect(5000, '127.0.0.1', function() {
	console.log('Connected');
	client.write('GET'); // send acknowledge to request data
});


// Call this callback to fetch data

client.on('data', function(data) {
	client.write('GET');
	console.log('Received: ' + data);
	var jsondata = JSON.parse(data);
	console.log(jsondata.mode); // "mode" field is parsed
	//client.destroy(); // kill client after server's response
});





client.on('close', function() {
	console.log('Connection closed');
});
