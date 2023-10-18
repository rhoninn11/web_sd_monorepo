import { v4 as uuidv4 } from 'uuid';
import { Client } from '../types/types';
import { EdgeRepo } from '../stores/EdgeRepo';
import { ServerEdge } from 'web_sd_shared_types/04_edge_t';
import { serverRequest } from 'web_sd_shared_types/02_serv_t';
import { FlowOps } from 'web_sd_shared_types/00_flow_t';
import { TypedRequestHandler, send_object } from './RequestHandler';


export class EdgeCrateHandler extends TypedRequestHandler<ServerEdge> {
    constructor() {
        super();
        this.type = 'serverEdge';
    }

    public handle_request(cl: Client, req: serverRequest) {
        let edge_data = this.unpack_data(req.data);

        if (edge_data.node_op == FlowOps.CREATE){
            edge_data = this.create_edge_on_server(cl, edge_data);
            console.log('!!! edge_data', edge_data);
        }

        req.data = this.pack_data(edge_data);
        send_object(cl, req);
    }

    create_edge_on_server = (cl: Client, edge_data: ServerEdge) => {
        let edge_repo = EdgeRepo.getInstance();
        edge_data.user_id = cl.auth_id
        edge_data.db_edge.user_id = cl.auth_id
        let server_curated_edge_data = edge_repo.insert_edge(edge_data);

        let new_edge_id = server_curated_edge_data.db_edge.id;
        console.log('+++ new edge_id', new_edge_id);

        return server_curated_edge_data;
    };
}
