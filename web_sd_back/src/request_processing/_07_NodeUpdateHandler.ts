import { v4 as uuidv4 } from 'uuid';
import { Client } from '../types/types';
import { NodeRepo } from '../stores/NodeRepo';
import { TypedRequestHandler, send_object } from './RequestHandler';

import { ServerNode } from 'web_sd_shared_types/01_node_t';
import { serverRequest } from 'web_sd_shared_types/02_serv_t';
import { FlowOps } from 'web_sd_shared_types/00_flow_t';


export class NodeUpdateHandler extends TypedRequestHandler<ServerNode> {

    constructor() {
        super();
        this.type = 'updateNode';
    }

    public handle_request(cl: Client, req: serverRequest) {
        let node_data = this.unpack_data(req.data);

        if (node_data.db_node.node_op == FlowOps.UPDATE)
            node_data = this.update_node_on_server(cl, node_data);

        req.data = this.pack_data(node_data);
        send_object(cl, req);
    }

    update_node_on_server(cl: Client, node_data: ServerNode): ServerNode {
        let node_repo = NodeRepo.getInstance();
        
        node_data.db_node.timestamp = Date.now();
        let server_curated_node_edit = node_repo.edit_node(node_data);
        
        // console.log('+++ snode updated: ', server_curated_node_edit.db_node.id);
        return server_curated_node_edit;
    }


}
