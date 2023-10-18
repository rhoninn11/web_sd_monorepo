import React from 'react';
import { Viewport } from 'reactflow';


export type moveCB = (x: number, y: number, dur: number) => void;

export class MoveObserver{
    private static instance: MoveObserver;
    public static getInstance(): MoveObserver {
        if (!MoveObserver.instance){
            MoveObserver.instance = new MoveObserver();
        }

        return MoveObserver.instance;
    }

    public onMoveStart = (event: MouseEvent | TouchEvent, viewport: Viewport): void => {
        console.log('!!! Move Start')
        console.log(viewport)
    }
    public onMove = (event: MouseEvent | TouchEvent, viewport: Viewport): void => {
        console.log('!!! Move !!!')
    }
    public onMoveEnd = (event: MouseEvent | TouchEvent, viewport: Viewport): void => {
        console.log('!!! Move End')
    }
}
