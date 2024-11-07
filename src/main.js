'use strict'

//import { initializeGame, terminateGame } from "./LocalMultiplayer.js"
//import { initializeGameIA, terminateGameIA } from "./SinglePlayerIA.js"
import { initializeCobeteGame, terminateCobeteGame } from "./cobeteGame.js"

const DEFAULT_PAGE_TITLE = "JS SPA Router";

const ROUTES = {
	404: {
		template: "../templates/404.html",
		title: "404 | " + DEFAULT_PAGE_TITLE,
		description: "Page not found",
	},
	"/": {
		template: "../templates/NoLogHome.html",
		title: "Home | " + DEFAULT_PAGE_TITLE,
		description: "This is the home page",
	},
	"/Logged": {
		template: "../templates/home.html",
		title: "Home logged | " + DEFAULT_PAGE_TITLE,
		description: "This is the logged home page",
	},
	"/Profile": {
		template: "../templates/Profile.html",
		title: "Profile | " + DEFAULT_PAGE_TITLE,
		description: "This is the Profile page",
	},
	"/SignOut": {
		template: "../templates/SignOut.html",
		title: "Sign Out | " + DEFAULT_PAGE_TITLE,
		description: "This is the Sign Out page",
	},
	"/Login": {
		template: "../templates/Login.html",
		title: "Sign In | " + DEFAULT_PAGE_TITLE,
		description: "This is the Sign In page",
	},
	"/Register": {
		template: "../templates/Register.html",
		title: "Sign Up | " + DEFAULT_PAGE_TITLE,
		description: "This is the Sign Up page",
	},
	"/LocalMultiplayer": {
		template: "../templates/localGame.html",
		title: "Local Game | " + DEFAULT_PAGE_TITLE,
		description: "This is the Pong Local Multiplayer Game",
	},
	"/Tournament": {
		template: "../templates/Tournament.html",
		title: "Tournament | " + DEFAULT_PAGE_TITLE,
		description: "This is the Tournament page for the Pong Game",
	},
	"/TournamentInterface": {
		template: "../templates/TournamentInterface.html",
		title: "Tournaments | " + DEFAULT_PAGE_TITLE,
		description: "This is the Tournaments page for the Pong Game",
	},
	"/SinglePlayerIA": {
		template: "../templates/localGame.html",
		title: "Single Game | " + DEFAULT_PAGE_TITLE,
		description: "This is the Single Game page for the Pong Game",
	},
	"/cobeteGame": {
		template: "../templates/cobeteGame.html",
		title: "Cobete Game | " + DEFAULT_PAGE_TITLE,
		description: "This is the Amazing Cobete Game",
	},
};

window.onpopstate = loadWindowLocation; // Event listener for url changes
window.onload = loadWindowLocation; // Handle the initial url

// Custom navigation event for links with the class spa-route
document.addEventListener("click", (event) => {
	if (!event.target.matches(".spa-route"))
		return;
	navigationEventHandler(event);
});


// Handles navigation events by setting the new window location and calling loadWindowLocation
function navigationEventHandler(event) {
	event.preventDefault();
	const path = event.target.dataset.path || event.target.href;
	window.history.pushState({}, "", /*event.target.href*/ path); // Set window location
	loadWindowLocation();
}

// Load the template html for the current window location
async function loadWindowLocation() {
	const location = window.location;
	const locationPath = (location.length === 0) ? "/" : location.pathname;
	const route = ROUTES[locationPath] || ROUTES["404"];
	
	try {
		const response = await fetch(route.template);
		if (!response.ok) throw new Error('Network response was not ok');
		const html = await response.text();
	
		document.getElementById("spa-template-content").innerHTML = html;
		document.title = route.title;
		document.querySelector('meta[name="description"]').setAttribute("content", route.description);
	
		// Manejo de scripts

		//terminateGame();
		//terminateGameIA();
		terminateCobeteGame();
		
		if (locationPath === "/LocalMultiplayer") {
			initializeGame();
		}
		if (locationPath === "/Register") {
            const script = document.createElement('script');
            script.src = './src/Register.js'; // Ruta a tu archivo Register.js
            document.body.appendChild(script);
        }
		if (locationPath === "/SinglePlayerIA") {
			initializeGameIA();
			//añadido para arrancar la IA
			//startAI();
		}
		if (locationPath === "/cobeteGame") {
			initializeCobeteGame();
			//console.log("EEEEEEEEEEEEEEEE");
		}
	} catch (error) {
	  	console.error('Error fetching template:', error);
	}
}
