import { serverRequest, syncSignature } from "web_sd_shared_types/02_serv_t";
import { RequestProcessor, FinishCB } from "./RequestProcessor";


export class SyncProcessor extends RequestProcessor<syncSignature> {
    constructor() {
        super();
        this.type = 'sync';
        this.show_type();
    }

    public to_server(syncData: syncSignature, id?: string) {
        this.input_to_server(syncData, id);
    }

    public from_server(req: serverRequest) {
        let sync_data: syncSignature = JSON.parse(req.data);
        this.execute_fn(req.id, sync_data);
        this.unbind_fn(req.id);
    }
}
