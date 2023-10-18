import { ClientServerBridge } from "../logic/ClientServerBridge";
import { DBNode, ServerNode } from "web_sd_shared_types/01_node_t";
import { DBEdge, ServerEdge } from "web_sd_shared_types/04_edge_t";

// const send_nodes_to_serv = (db_nodes: DBNode[]) => {
//     let initial = new Promise<void>((resolve, reject) => resolve());

//     db_nodes.forEach((db_node) => {
//         initial = initial.then(() => {
//             return new Promise<void>((resolve, reject) => {
//                 let on_serv_accept = (serv_node: ServerNode) => {
//                     resolve();
//                 }
//                 ClientServerBridge.getInstance()
//                     .sync_node(db_node, on_serv_accept);
//             });
//         });
//     });

//     return initial;
// }

// const send_edges_to_serv = (db_edges: DBEdge[]) => {
//     let initial = new Promise<void>((resolve, reject) => resolve());

//     db_edges.forEach((db_edge) => {
//         initial = initial.then(() => {
//             return new Promise<void>((resolve, reject) => {
//                 let on_serv_accept = (serv_edge: ServerEdge) => {
//                     resolve();
//                 }
//                 ClientServerBridge.getInstance()
//                     .sync_edge(db_edge, on_serv_accept);
//             });
//         });
//     });

//     return initial;
// }

// export const send_client_data_to_serveer = (db_nodes: DBNode[], db_edges: DBEdge[]) => {
//     send_nodes_to_serv(db_nodes)
//         .then(() => send_edges_to_serv(db_edges))
//         .then(() => console.log('+++ server synced'));
// }