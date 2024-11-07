'use strict'

import { setImage, setMap, refresh, waiting } from "./cobeteGame.js";

export let socket //= new WebSocket('ws://10.14.2.1:50002/ws/game/');
//const socket = new WebSocket('ws://127.0.0.1:50002/ws/game/');

// const campoUserId = document.getElementById('user_id_txt_field');

export let posXR;
export let posYR;
export let anguloR;
export let posXB;
export let posYB;
export let anguloB;
export let weaponRedX;
export let weaponRedY;
export let weaponBlueX;
export let weaponBlueY;
export let motorROn = false;
export let motorBOn = false;
export let moveRedOn = true;
export let moveBlueOn = true;
export let waitingAction = 'waitForPlayer';



window.addEventListener('popstate', function(event) {
    console.log('Se ha navegado hacia atrás o adelante en el historial.');
    socket.close();
});

export function connectSocket()
{
    socket = new WebSocket('ws://10.14.2.1:50002/ws/game/');

	socket.onopen = function(e) {
        console.log("Conectado al WebSocket");
    };
    
    socket.onmessage = function(event) {
    
        const mensaje = JSON.parse(event.data);
        if (mensaje.type != 'refresh')
            {
                console.log("Mensaje del servidor:");
                console.log("Type: ", mensaje.type);
                if (mensaje.type == 'waiting')
                    console.log("Action: ", mensaje.action);
            }
    
            if (mensaje.type == 'refresh')
            {
                posXR = mensaje.player1X;
                posYR = mensaje.player1Y;
                anguloR = mensaje.player1Angle;
                posXB = mensaje.player2X;
                posYB = mensaje.player2Y;
                anguloB = mensaje.player2Angle;
                motorROn = mensaje.player1Motor;
                motorBOn = mensaje.player2Motor;
                moveRedOn = mensaje.player1Move;
                moveBlueOn = mensaje.player2Move;
                weaponRedX = mensaje.player1WeaponX;
                weaponRedY = mensaje.player1WeaponY;
                weaponBlueX = mensaje.player2WeaponX;
                weaponBlueY = mensaje.player2WeaponY;
            }
        else if(mensaje.type == 'waiting')
        {
            waitingAction = mensaje.action;
            waiting();
        }
        else if(mensaje.type == 'press_to_start')
        {
            console.log("color: ", mensaje.color)
            setImage(mensaje.color)
        }
        else if (mensaje.type == 'map')
            setMap(mensaje);
    };
    
    socket.onclose = function(event) {
        if (event.wasClean) {
            console.log(`Conexión cerrada limpiamente, código: ${event.code}, motivo: ${event.reason}`);
        } else {
            console.log("Conexión terminada");
        }
    };
    
    socket.onerror = function(error) {
        console.log("Error en el WebSocket", error);
    };
	
}

// socket.onopen = function(e) {
//     console.log("Conectado al WebSocket");
// };

// socket.onmessage = function(event) {

//     const mensaje = JSON.parse(event.data);
//     if (mensaje.type != 'refresh')
//     {
//         console.log("Mensaje del servidor:");
//         console.log("Type: ", mensaje.type);
//         if (mensaje.type == 'waiting')
//             console.log("Action: ", mensaje.action);
//     }
        

//     if (mensaje.type == 'refresh')
//     {
//         posXR = mensaje.player1X;
//         posYR = mensaje.player1Y;
//         anguloR = mensaje.player1Angle;
//         posXB = mensaje.player2X;
//         posYB = mensaje.player2Y;
//         anguloB = mensaje.player2Angle;
//         motorROn = mensaje.player1Motor;
//         motorBOn = mensaje.player2Motor;
//         moveRedOn = mensaje.player1Move;
//         moveBlueOn = mensaje.player2Move;
//         weaponRedX = mensaje.player1WeaponX;
//         weaponRedY = mensaje.player1WeaponY;
//         weaponBlueX = mensaje.player2WeaponX;
//         weaponBlueY = mensaje.player2WeaponY;
//     }
//     else if(mensaje.type == 'waiting')
//     {
//         waitingAction = mensaje.action;
//         waiting();
//     }
//     else if(mensaje.type == 'press_to_start')
//     {
//         console.log("color: ", mensaje.color)
//         setImage(mensaje.color)
//     }
//     else if (mensaje.type == 'map')
//         setMap(mensaje);
// };

// socket.onclose = function(event) {
//     if (event.wasClean) {
//         console.log(`Conexión cerrada limpiamente, código: ${event.code}, motivo: ${event.reason}`);
//     } else {
//         console.log("Conexión terminada");
//     }
// };

// socket.onerror = function(error) {
//     console.log("Error en el WebSocket", error);
// };

export async function button(b)
{
    socket.send(JSON.stringify({
        type: 'move',
        action: b
    }));

}

export async function start()
{
    console.log("ENVIA start");
    socket.send(JSON.stringify({
        type: 'start',
    }));
}

export async function continueGame()
{
    console.log("ContinueGAme function")
    socket.send(JSON.stringify({
        type: 'continueGame',
    }));
}

export function join() {
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            type: "join_game",
            user_id: "12"
        }));
    } else {
        console.log("Esperando a que el socket se conecte...");
        setTimeout(join, 100);  // Reintenta la función después de 100ms
    }
}


/* export function join()
{
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
                            type: "join_game",
                            user_id: "12"
                        }));
    }
} */
