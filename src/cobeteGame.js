'use strict'


import { join, button, start, posXR, posYR, anguloR, posXB, posYB, anguloB,
motorROn, motorBOn, moveRedOn, moveBlueOn, weaponRedX, weaponRedY,
weaponBlueX, weaponBlueY, waitingAction, continueGame, connectSocket } from "./com.js";

import { createMap } from "./cobeteSetMap.js"

//Game variables
let canvas;
let ctx;
let imageOn;
let gameLoopId;
let timeoutId;
let wait;
let finish;
let player1Points = 0;
let player2Points = 0;

let left = false;
let right = false;
let motor = false;

let joined = false;

let rectangleList = [];


const imgWaiting = new Image();
imgWaiting.src = 'src/images/waiting.jpg';

const imgReadyRed = new Image();
imgReadyRed.src = 'src/images/red_ready.jpg';


const imgReadyBlue = new Image();
imgReadyBlue.src = 'src/images/blue_ready.jpg';

const imgWaitingPress = new Image();
imgWaitingPress.src = 'src/images/waiting_press.jpg';

const cobeteR = new Image();
cobeteR.src = 'src/images/cR.png';

const cobeteRf = new Image();
cobeteRf.src = 'src/images/cRf.png';

const cobeteB = new Image();
cobeteB.src = 'src/images/cA.png';

const cobeteBf = new Image();
cobeteBf.src = 'src/images/cAf.png';

const cobeteRWin1  = new Image();
cobeteRWin1.src = 'src/images/cRg1.png';

const cobeteRWin2  = new Image();
cobeteRWin2.src = 'src/images/cRg2.png';

const cobeteBWin1  = new Image();
cobeteBWin1.src = 'src/images/cAg1.png';

const cobeteBWin2  = new Image();
cobeteBWin2.src = 'src/images/cAg2.png';

const calavera = new Image()
calavera.src = 'src/images/calavera.png';

const redOnePoint = new Image()
redOnePoint.src = 'src/images/red_one_point.jpg';

const blueOnePoint = new Image()
blueOnePoint.src = 'src/images/blue_one_point.jpg';

const redWinner = new Image()
redWinner.src = 'src/images/win_red.jpg';

const blueWinner = new Image()
blueWinner.src = 'src/images/win_blue.jpg';


function handleKeydown(event) {
    if (event.key === 'a' && left === false) {
        button('leftOn');
        left = true;
    }
    if (event.key === 's' && right === false) {
        button('rightOn');
        right = true;
    }
    if (event.key === 'd' && motor === false) {
        button('motorOn');
        motor = true;
    }
    if (event.key === 'f') {
        button('fire');
    }
}

function handleKeyup(event) {
    if (event.key === 'a') {
        button('leftOff');
        left = false;
    }
    if (event.key === 's') {
        button('rightOff');
        right = false;
    }
    if (event.key === 'd') {
        button('motorOff');
        motor = false;
    }
}
export function initializeCobeteGame() {
	canvas = document.getElementById('pongCanvas');
	ctx = canvas.getContext('2d');
	wait = true;
	imageOn = imgWaiting;

	connectSocket();
	join();

	window.addEventListener('keydown', handleKeydown);
    window.addEventListener('keyup', handleKeyup);

	//inializeEventListener();
	// window.addEventListener('keydown', (event) => {
	// 	if (event.key === 'a' && left === false) {
	// 		button('leftOn');
	// 		left = true;
	// 	}
	// 	if (event.key === 's' && right === false) {
	// 		button('rightOn');
	// 		right = true;
	// 	}
	// 	if (event.key === 'd' && motor === false) {
	// 		button('motorOn');
	// 		motor = true;
	// 	}
	// 	if (event.key === 'f') {
	// 		button('fire');
	// 	}
	// });
	
	// window.addEventListener('keyup', (event) => {
	// 	if (event.key === 'a') {
	// 		button('leftOff');
	// 		left = false;
	// 	}
	// 	if (event.key === 's') {
	// 		button('rightOff');
	// 		right = false;
	// 	}
	// 	if (event.key === 'd') {
	// 		button('motorOff');
	// 		motor = false;
	// 	}
	// });

	// const h1Element = document.querySelector('#pong-container h1');
	//   // Cambia el texto del h1
	// h1Element.textContent = 'Online Multiplayer';
    gameLoop();
}

function degreesToRadians(grados) {
    return grados * (Math.PI / 180);
}

export function setMap(recivedMap)
{
	rectangleList = createMap(recivedMap);
	wait = false;
	refresh();
}

export function setImage(mesage)
{
	if (mesage === 'red')
		imageOn = imgReadyRed
	else if (mesage === 'blue')
		imageOn = imgReadyBlue
	else if (mesage == 'ready')
	{
		wait = true
		imageOn = imgWaitingPress
	}
	refresh();
}

async function pressSpace()
{
	await new Promise((resolve) => {
		function onKeyPress(event) {
		  if (event.code === "Space") {
			document.removeEventListener("keydown", onKeyPress); // Elimina el evento después de presionar espacio
			resolve();
		  }
		}
		
		document.addEventListener("keydown", onKeyPress);
	  });
}

async function printImages()
{
	ctx.drawImage(imageOn, 0, 0);
}
export async function waiting()
{
	wait = true;
	//console.log("Estamos en Waiting:", waitingAction );
	if (waitingAction == 'waitForPlayer')
	{
		printImages();
		refresh();
	}
	else if (waitingAction == 'red')
	{
		imageOn = imgReadyRed;
		printImages();
		await pressSpace();
		start();
		//refresh();
	}
	else if (waitingAction == 'blue')
	{
		imageOn = imgReadyBlue;
		printImages();
		await pressSpace();
		start();
		//refresh();
	}
	else if (waitingAction == 'ready')
	{
		imageOn = imgWaitingPress;
		printImages();
		refresh();
	}
	else if (waitingAction == 'redPoint1')
	{
		player1Points =+ 1;
		updateScore();
		ctx.clearRect(posXR - 18, posYR - 25, 40, 50);
		ctx.drawImage(cobeteRWin1, posXR - 13, posYR - 18);
		drawMap();
		//refresh();
	}
	else if (waitingAction == 'redPoint2')
	{
		ctx.clearRect(posXR - 18, posYR - 25, 40, 50);
		ctx.drawImage(cobeteRWin2, posXR - 13, posYR - 18);
		drawMap();
		//refresh();
	}
	else if (waitingAction == 'redPoint3')
	{
		imageOn = redOnePoint;
		printImages();
		await pressSpace();
		continueGame();
		//refresh();
	}
	else if (waitingAction == 'bluePoint1')
	{
		player2Points =+ 1;
		updateScore();
		ctx.clearRect(posXB - 18, posYB - 25, 40, 50);
		ctx.drawImage(cobeteBWin1, posXB - 13, posYB - 18);
		drawMap();
		//refresh();
	}
	else if (waitingAction == 'bluePoint2')
	{
		ctx.clearRect(posXB - 18, posYB - 25, 40, 50);
		ctx.drawImage(cobeteBWin2, posXB - 13, posYB - 18);
		drawMap();
		//refresh();
	}
	else if (waitingAction == 'bluePoint3')
	{
		imageOn = blueOnePoint;
		printImages();
		await pressSpace();
		continueGame();
	}
	else if (waitingAction == 'redWinGame')
	{
		imageOn = redWinner;
		printImages();
		//refresh();
	}
	else if (waitingAction == 'blueWinGame')
	{
		imageOn = blueWinner;
		printImages();
		//refresh();
	}
	else if (waitingAction == 'otherPlayerDisconnect')
	{
		showMessage('Error: The other player has disconnected\n(Maybe dead, maybe tomando cañas)', 'red')
		imageOn = imgWaiting;
		terminateCobeteGame();
		//refresh();
	}
}

function gameLoop() {
	
	cleanCanva();
	drawCanva();
	if (wait == true)
		waiting();
	else
		refresh();
}

export function refresh() {
	gameLoopId = requestAnimationFrame(gameLoop);
}

function cleanCanva()
{
	ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function drawCanva()
{
	if (moveRedOn == false)
		drawCobeteR(calavera);	
	else if (motorROn)
		drawCobeteR(cobeteRf);
	else
		drawCobeteR(cobeteR);

	if (moveBlueOn == false)
		drawCobeteB(calavera);
	else if(motorBOn)
		drawCobeteB(cobeteBf);
	else
		drawCobeteB(cobeteB);7
	
	drawMap();
	
	if (weaponRedX  != 0)
		drawWeaponRed();
	if (weaponBlueY  != 0)
		drawWeaponBlue();
}

function drawWeaponBlue()
{
	ctx.fillStyle = "white"; 
    ctx.fillRect(weaponBlueX,weaponBlueY, 4, 4);
}

function drawWeaponRed()
{
	ctx.fillStyle = "white"; 
    ctx.fillRect(weaponRedX,weaponRedY, 4, 4);
}

export function drawCobeteB(img) {
    ctx.save();
    ctx.translate(posXB, posYB);
    ctx.rotate(degreesToRadians(anguloB));
    ctx.drawImage(img, -cobeteB.width / 2, -cobeteB.height / 2);
    ctx.restore();
}

export function drawCobeteR(img) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.save();
    ctx.translate(posXR, posYR);
    ctx.rotate(degreesToRadians(anguloR));
    ctx.drawImage(img, -cobeteR.width / 2, -cobeteR.height / 2);
    ctx.restore();
}

function drawMap()
{
	for (let i = 0; i < rectangleList.length; i++)
	{
		ctx.fillStyle = rectangleList[i].color; 
        ctx.fillRect(rectangleList[i].x, rectangleList[i].y, rectangleList[i].width, rectangleList[i].height);
    }
	ctx.fillStyle = 'deepskyblue';
	ctx.fillRect(250, 590, 70, 10);
	ctx.fillStyle = 'red';
	ctx.fillRect(380, 590, 70, 10);
}
function updateScore()
{
	document.getElementById('player1-score').textContent = 'Red Cobete: ' + player1Points;
	document.getElementById('player2-score').textContent = 'Blue Cobete: ' + player2Points;
}

export function terminateCobeteGame() {
	
	//console.log("-----TERMINATE GAME--------")

	document.removeEventListener('keydown', gameLoop);

	// window.removeEventListener('keydown', handleKeydown);
    // window.removeEventListener('keyup', handleKeyup);
	// window.addEventListener('keydown', handleKeydown);
	// window.addEventListener('keyup', handleKeyup);
	
	if (gameLoopId)
		cancelAnimationFrame(gameLoopId);
	if (timeoutId)
		clearTimeout(timeoutId);
}

function showMessage(message, color) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = color;
    ctx.font = '20px Arial';
    ctx.textAlign = 'center';

    // Dividimos el mensaje en líneas, usando "\n" como separador
    const lines = message.split('\n');
    
    // Para centrar cada línea verticalmente, ajustamos la posición Y para cada línea
    lines.forEach((line, index) => {
        ctx.fillText(line, canvas.width / 2, canvas.height / 2 + (index * 40)); // Ajusta el valor 40 para el espaciado entre líneas
    });
}


