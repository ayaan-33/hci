export type Vec3 = readonly [number, number, number];
export type SpeakerId = 'immad'|'raj'|'awais'|'raja';
export type PoseId = 'N'|'H'|'W'|'L'|'R'|'G'|'A';
export type BeatKind = 'question'|'comparison'|'team'|'task'|'criteria'|'disclosure'|'demo'|'metrics'|'timing'|'errors'|'control'|'research'|'coverage'|'limits'|'focus'|'calendar'|'screenreader'|'marketing'|'privacy'|'recommendation'|'hybrid'|'next';
export interface Beat {start:number;end:number;camera:[PoseId,PoseId];sweep:number;kind:BeatKind;headline:string;lines:string[];eyebrow:string;textDelay?:number;linesDelay?:number}
export interface FeatureSet {hopSamples:number;windowSamples:number;bandsHz:number[][];values:number[][];onsets:number[]}
export interface Caption {start:number;end:number;text:string}
export interface Section {id:string;speaker:string;title:string;audioStartSamples:number;audioEndSamples:number;startFrame:number;endFrame:number;features:FeatureSet;captions:Caption[]}
export interface Manifest {schemaVersion:number;fps:number;width:number;height:number;sampleRate:number;durationFrames:number;voiceEndSamples:number;masterSamples:number;narration:string;fingerprint:string;sections:Section[];demos:Record<string,{file:string;frames:number;sha256:string}>}
export interface Camera {eye:Vec3;target:Vec3}
export interface Voice {amplitude:number;low:number;mid:number;high:number;onsets:number[];localFrame:number}
