import { serverRequest } from "web_sd_shared_types/02_serv_t";
import { ServerEdge } from "web_sd_shared_types/04_edge_t";
import { RequestProcessor, FinishCB } from "./RequestProcessor";

export class EdgeRequestProcessor extends RequestProcessor<ServerEdge> {
    constructor() {
        super();
        this.type = 'serverEdge';
        this.show_type();
    }

    public to_server(server_node: ServerEdge, id?: string) {
        this.input_to_server(server_node, id);
    }

    public from_server(req: serverRequest) {
        let server_edge: ServerEdge = JSON.parse(req.data);
        this.execute_fn(req.id, server_edge);
        this.unbind_fn(req.id);
    }
}


