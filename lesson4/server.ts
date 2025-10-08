// test read: curl 'localhost:3000/get'
// test update: curl -d devID=wokwipico -d temp=23.5 -d humi=56.2 'localhost:3000'

import { DB } from "https://deno.land/x/sqlite/mod.ts";

// Database
const db = new DB("iot.db");

db.execute(`
  CREATE TABLE IF NOT EXISTS atmo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperature REAL,
    humidity REAL,
    datetime DATE NOT NULL
  )
`);

const qstr = "SELECT temperature, humidity, datetime FROM atmo";
const ustr = "INSERT INTO atmo (temperature, humidity, datetime) VALUES (?,?,?)";
const devID = "wokwipico";


// Cleanup
globalThis.onunload = (e: Event): void => {
	console.log('unload');
	// Close DB connection
	db.close();
};
Deno.addSignalListener("SIGINT", () => {
	console.log('sigint');
	// Exit cleanly, calls onunload
	Deno.exit();
});


// Server
// get current time in seconds since unix epoch
const now = ()=>Math.floor(Date.now()/1000);
let sockets=[];

Deno.serve({
	port: 3000,
	async handler(req) {
		// WebSocket endpoint
		if (req.headers.get("upgrade") === "websocket") {
			// upgrade to websocket
			const { socket, response } = Deno.upgradeWebSocket(req);
			// add to list of open sockets
			sockets.push(socket);
			console.log(sockets);
 	
			socket.onopen = () => {
				console.log("CONNECTED");
				// send all data
				socket.send(JSON.stringify(db.query(qstr)));
			};
			socket.onclose = () => {
				console.log("DISCONNECTED");
				sockets = sockets.filter(v=> v != socket);
			};
			socket.onerror = (error) => console.error("ERROR:", error);
			return response;
		}
		// POST endpoint
		else if (req.method === "POST") {
			const params = new URLSearchParams(await req.text());
			// check for sensor id
			if (params.get("devID") === devID) {
				// parse POST parameters and write to DB
				const data = [ params.get("temp"), params.get("humi"), now() ];
				db.query(ustr, data);
				// sen new sensordata to all open websockets
				sockets.forEach(v=>
					v.readyState === WebSocket.OPEN
					&& v.send(JSON.stringify(data)) );
				return new Response("OK", {status:200});
			} else
				return new Response("ERR", {status:400});
		}
		// GET endpoints
		else if (req.method === "GET") {
			const url = new URL(req.url);
			if (url.pathname === "/") {
				const file = await Deno.open("./index.html");
				return new Response(file.readable, {
					headers: {"Content-Type" : "text/html"}
				});
			} else if (url.pathname === "/get") {
				return new Response( JSON.stringify(db.query(qstr)) + '\n', {
					headers: {"Content-Type" : "application/json"},
					status: 200 });
			} else
				return new Response( "NOT FOUND", {status:404} );
		}
	}
});
