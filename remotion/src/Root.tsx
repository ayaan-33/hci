import React from 'react';
import {Composition} from 'remotion';
import {Film,Proof} from './Film';
import {FILM_FRAMES,FPS,HEIGHT,PROOF_FRAMES,WIDTH} from './data/config';
export const Root:React.FC=()=> <><Composition id="Film" component={Film} durationInFrames={FILM_FRAMES} width={WIDTH} height={HEIGHT} fps={FPS}/><Composition id="Proof" component={Proof} durationInFrames={PROOF_FRAMES} width={WIDTH} height={HEIGHT} fps={FPS}/></>;
