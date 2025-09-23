// curl localhost:8000/u

const get_data = ()=> ({
	temperature: 22.5,
	humidity: 55,
	status: "OK"
});

Deno.serve(
	{	hostname: "0.0.0.0",
		port: 8000,
		onListen({path}) {
			console.log("Listening on: localhost:8000");
		}
	},
	async (req: Request) => {
		if (req.method == "GET") {
			//const body = await req.text();
			const url = new URL(req.url);
			console.log("Query params: ", url.searchParams);
			// endpoints
			const res = url.pathname == "/u" ? get_data() : {status: "err"};
			// respond
			return new Response( JSON.stringify(res) + '\n' );
		}
	}
);
