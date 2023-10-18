import { cloneDeep, flow } from "lodash";
import { DBNode, FlowNode } from "web_sd_shared_types/01_node_t";
import { DBEdge, EdgeStyle, FlowEdge } from "web_sd_shared_types/04_edge_t";

export const node_db2flow = (db_node: DBNode): FlowNode => {

    let flow_node: FlowNode = {
        id: db_node.id.toString(),
        type: 'prompt',
        draggable: false,
        position: db_node.position,
        data: {
            node_data: {
                id: db_node.id.toString(),
                user_id: db_node.user_id,
                initial_node_id: db_node.initial_node_id,
                result_data: cloneDeep(db_node.result_data),
                counter: 0,
            },
            node_callback: {
                on_update_result_img: () => { },
                on_update_result_prompt: () => { },
            },
        }
    }
    return flow_node;
}

export const edge_db2flow = (db_edge: DBEdge): FlowEdge => {

    let edge_style = new EdgeStyle();
    edge_style.set_color(db_edge.user_id)

    let flow_edge: FlowEdge = {
        id: db_edge.id.toString(),
        source: db_edge.source,
        target: db_edge.target,
        style: edge_style,
        type: 'prompt'
    }
    return flow_edge;
}

