import { ServerNode } from "web_sd_shared_types/01_node_t";
import { serverRequest } from "web_sd_shared_types/02_serv_t";
import { RequestProcessor, FinishCB } from "./RequestProcessor";

export class NodeRequestProcessor extends RequestProcessor<ServerNode> {
    constructor() {
        super();
        this.type = 'serverNode';
        this.show_type();
    }

    public to_server(server_node: ServerNode, id?: string) {
        this.input_to_server(server_node, id);
    }

    public from_server(req: serverRequest) {
        let server_node: ServerNode = JSON.parse(req.data);
        this.execute_fn(req.id, server_node);
        this.unbind_fn(req.id);
    }
}


