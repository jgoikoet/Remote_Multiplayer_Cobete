'use strict'

let rectangleList = [];


//function

export function createMap(map)
{
    const keys = Object.keys(map);

    rectangleList = []
    // let x;
    // let y;
    // let width;
    // let height;
    // let color;

    for (let i = 1; i < keys.length; i++)
    {
        //console.log(map[keys[i]][0]);
        let rectangle = {
            x: map[keys[i]][0],
            y: map[keys[i]][1],
            width: map[keys[i]][2],
            height: map[keys[i]][3],
            color: map[keys[i]][4]
        }
        rectangleList.push(rectangle);
    }
    //console.log(rectangleList[0].x);
    return rectangleList;
}