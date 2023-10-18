import { syncOps, syncSignature } from "web_sd_shared_types/02_serv_t";
import { edgeCreateWCb, imgCreateCb, nodeCreateWCb } from "../types/types_db";
import { ClientServerBridge } from "./ClientServerBridge";

// ===== nodes =====
export const sync_client_nodes_with_server = (nodes_ids: string[], add_node_cb: nodeCreateWCb) => {
    let initial = new Promise<void>((resolve, reject) => resolve());
    nodes_ids.forEach((node_id) => {
        initial = initial.then(() => single_node_sync_promise(node_id, add_node_cb));  
    });

    return initial;
}

const single_node_sync_promise = (node_id: string, add_node_cb: nodeCreateWCb) => {
    return new Promise<void>((resolve, reject) => {
        let sync_data_in = syncSignatureForSingle_Node(node_id)
        syncFor_Node(sync_data_in, add_node_cb, () => resolve())
    });    
}

const syncSignatureForSingle_Node = (node_id: string) => {
    let sync_data_in = new syncSignature()
    sync_data_in.sync_op = syncOps.TRANSFER;
    sync_data_in._set_ids([node_id], [], []);
    return sync_data_in;
}

const syncFor_Node = (sync_data_in: syncSignature, add_node_cb: nodeCreateWCb, synced: () => void) => {
    ClientServerBridge.getInstance()
        .sync_with_server(sync_data_in, (sync_data_out) => {
            if (sync_data_out.sync_op == syncOps.TRANSFER) {
                if (sync_data_out.node_data_arr.length > 0) {
                    add_node_cb(sync_data_out.node_data_arr[0], synced)
                }
            }
        });
}

// ===== edges =====
export const sync_client_edges_with_server = (edge_id_arr: string[], add_edge_cb: edgeCreateWCb) => {
    let initial = new Promise<void>((resolve, reject) => resolve());
    edge_id_arr.forEach((edge_id) => {
        initial = initial.then(() => single_edge_sync_promise(edge_id, add_edge_cb));
    });

    return initial;
}

const single_edge_sync_promise = (edge_id: string, add_edge_cb: edgeCreateWCb) => {
    return new Promise<void>((resolve, reject) => {
        let sync_data_in = syncSignatureForSingle_Edge(edge_id)
        syncFor_Edge(sync_data_in, add_edge_cb, () => resolve())
    });
}

const syncSignatureForSingle_Edge = (edge_id: string) => {
    let sync_data_in = new syncSignature()
    sync_data_in.sync_op = syncOps.TRANSFER;
    sync_data_in._set_ids([], [edge_id], []);
    return sync_data_in;
}

const syncFor_Edge = (sync_data_in: syncSignature, add_edge_cb: edgeCreateWCb, synced: () => void) => {
    ClientServerBridge.getInstance()
        .sync_with_server(sync_data_in, (sync_data_out) => {
            if (sync_data_out.sync_op == syncOps.TRANSFER) {
                if (sync_data_out.edge_data_arr.length > 0) {
                    add_edge_cb(sync_data_out.edge_data_arr[0], synced);
                }
            }
        });
}

// ==== Images ====
export const sync_client_img_with_server = (img_id_arr: string[], add_img_cb: imgCreateCb) => {
    let initial = new Promise<void>((resolve, reject) => resolve());

    img_id_arr.forEach((img_id) => {
        initial = initial.then(() => single_img_sync_promise(img_id, add_img_cb));
    });

    return initial;
}

const single_img_sync_promise = (img_id: string, add_img_cb: imgCreateCb) => {
    return new Promise<void>((resolve, reject) => {
        let sync_data_in = syncSignatureForSingle_Img(img_id)
        syncFor_Img(sync_data_in, add_img_cb, () => resolve())
    });
}

const syncSignatureForSingle_Img = (img_id: string) => {
    let sync_data_in = new syncSignature()
    sync_data_in.sync_op = syncOps.TRANSFER;
    sync_data_in._set_ids([], [], [img_id]);
    return sync_data_in;
}

const syncFor_Img = (sync_data_in: syncSignature, add_img_cb: imgCreateCb,  synced: () => void) => {
    ClientServerBridge.getInstance()
        .sync_with_server(sync_data_in, (sync_data_out) => {
            console.log(`+++sync signature from server`)
            console.log(sync_data_out)
            if (sync_data_out.sync_op == syncOps.TRANSFER) {
                if (sync_data_out.img_data_arr.length > 0) {
                    add_img_cb(sync_data_out.img_data_arr[0], synced)
                }
            }
        });
}
