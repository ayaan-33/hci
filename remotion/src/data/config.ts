import script from './script.json';
import rawBoard from './storyboard.json';
import proof from './proof-clips.json';
import type {Beat, SpeakerId} from '../types';
export const FPS=30, WIDTH=3840, HEIGHT=1920, SAMPLE_RATE=48000, OPENING_FRAMES=540;
export const FILM_FRAMES=Math.round((18+script.reduce((n,s)=>n+s.samples/SAMPLE_RATE,0)+8)*FPS);
export const PROOF_CLIPS=proof;
export const PROOF_FRAMES=proof.reduce((n,s)=>n+s.frames,0);
export const STORYBOARD=rawBoard as unknown as Record<string,Beat[]>;
export const SPEAKERS:Record<SpeakerId,{name:string;accent:string;label:string}>={
 immad:{name:'Muhammad Immad',accent:'#d6ab69',label:'INTRODUCTION / RECOMMENDATION'},
 raj:{name:'Raj Lakhani',accent:'#82a9e7',label:'PROTOTYPE DEMONSTRATION'},
 awais:{name:'Awais Basheer',accent:'#baa3db',label:'COMPARISON / EVIDENCE'},
 raja:{name:'Raja Suleman',accent:'#86b49a',label:'ACCESSIBILITY / LIMITATIONS'},
};
export const speakerId=(section:string):SpeakerId=>section.startsWith('Immad')?'immad':section.startsWith('Raj-')?'raj':section.startsWith('Awais')?'awais':'raja';
export const REFERENCES=[
 ['JMIR Human Factors (2021)','doi:10.2196/25787'],
 ['Soni et al. (2022) · Frontiers in Digital Health','doi:10.3389/fdgth.2022.954069'],
 ['Xiao et al. (2020) · ACM TOCHI','doi:10.1145/3381804'],
 ['Wei et al. · preprint reference','arxiv.org/abs/2301.05843'],
 ['Amershi et al. (2019) · CHI','Guidelines for Human–AI Interaction'],
 ['W3C · WCAG 2.2','SC 4.1.3 · ARIA23 conversation log technique'],
 ['Typeform via tinycommand.com (2025)','Secondhand vendor claim · not tested by this team'],
];
