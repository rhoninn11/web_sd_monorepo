

import { ProcessorRepository } from './RequestProcessor';

import { AuthRequestProcessor } from './01_AuthRequestProcessor';
import { NodeRequestProcessor } from './02_NodeRequestProcessor';
import { EdgeRequestProcessor } from './03_EdgeRequestProcessor';
import { SyncProcessor } from './04_SyncProcessor';
import { Txt2ImgRequestProcessor } from "./05_Txt2ImgRequestProcessor";
import { ProgressRequestProcessor } from "./05_1_ProgressRequestProcessor";
import { Img2ImgRequestProcessor } from "./06_Img2ImgRequestProcessor";
import { NodeUpdateProcessor } from './07_NodeUpdateProcessor';


export let init_processors = () => {
    ProcessorRepository.getInstance()
        .register_processor(new AuthRequestProcessor())
        .register_processor(new EdgeRequestProcessor())
        .register_processor(new NodeRequestProcessor())
        .register_processor(new SyncProcessor())
        .register_processor(new Txt2ImgRequestProcessor())
        .register_processor(new ProgressRequestProcessor())
        .register_processor(new Img2ImgRequestProcessor())
        .register_processor(new NodeUpdateProcessor());
        
}