import { progress, serverRequest } from "web_sd_shared_types/02_serv_t";
import { RequestProcessor } from "./RequestProcessor";

export class ProgressRequestProcessor extends RequestProcessor<progress> {

    constructor() {
        super();
        this.type = 'progress';
        this.show_type();

    }

    public from_server(req: serverRequest) {
        let progr: progress = JSON.parse(req.data);
        this.execute_fn(req.id, progr);
    }
}
