// test read: curl 'localhost:3000/get'
// test update: curl -d devID=wokwipico -d temp=23.5 -d humi=56.2 'localhost:3000'

import { DB } from "https://deno.land/x/sqlite/mod.ts";

// Open a database
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

// get current time in seconds since unix epoch
const now = ()=>Math.floor(Date.now()/1000);

// Server
Deno.serve(
	{	hostname: "0.0.0.0",
		port: 3000,
		onListen({path}) {
			console.log("Listening on: localhost:3000");
		}
	},
	async (req: Request) => {
		if (req.method === "GET") {
			const url = new URL(req.url);
			// endpoints
			if (url.pathname === "/") {
				const file = await Deno.open("./index.html");
				return new Response(file.readable, {
					headers: {"Content-Type" : "text/html"}
				});
			} else if (url.pathname === "/get") {
				const headers = new Headers();
				headers.append("Content-Type", "application/json");
				return new Response( JSON.stringify(db.query(qstr)) + '\n', {headers,status:200} );
			} else
				return new Response( "NOT FOUND", {status:404} );
		}
		else if (req.method === "POST") {
			const params = new URLSearchParams(await req.text());
			// check for sensor id
			if (params.get("devID") === devID) {
				// parse POST parameters and write to DB
				db.query(ustr, [params.get("temp"), params.get("humi"), now()]);
				return new Response("OK", {status:200});
			} else
				return new Response("ERR", {status:400});
		}
	}
);

