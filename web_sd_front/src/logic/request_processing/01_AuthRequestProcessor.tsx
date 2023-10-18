import { authData, serverRequest } from "web_sd_shared_types/02_serv_t";
import { RequestProcessor, FinishCB } from "./RequestProcessor";


export class AuthRequestProcessor extends RequestProcessor<authData> {
    constructor() {
        super();
        this.type = 'auth';
        this.show_type();
    }

    public to_server(auth_data: authData, id?: string) {
        this.input_to_server(auth_data, id);
        console.log('+++ auth request');
    }

    public from_server(req: serverRequest) {
        console.log('+++ auth from server', req);
        let auth_data: authData = JSON.parse(req.data);
        this.execute_fn(req.id, auth_data);
        this.unbind_fn(req.id);
    }
}