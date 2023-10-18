import { serverRequest } from "web_sd_shared_types/02_serv_t";
import { txt2img } from "web_sd_shared_types/03_sd_t";
import { RequestProcessor } from "./RequestProcessor";



export class Img2ImgRequestProcessor extends RequestProcessor<txt2img> {
    constructor() {
        super();
        this.type = 'img2img';
        this.show_type();
    }

    public to_server(t2i: txt2img, id?: string) {
        console.log("+++ Img2ImgRequestProcessor::to_server", t2i)
        this.input_to_server(t2i, id);
    }

    public from_server(req: serverRequest) {
        let txt2img_data: txt2img = JSON.parse(req.data);
        this.execute_fn(req.id, txt2img_data);
        this.unbind_fn(req.id);
    }
}
