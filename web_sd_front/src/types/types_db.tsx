import { DBNode } from "web_sd_shared_types/01_node_t";
import { progress } from "web_sd_shared_types/02_serv_t";
import { DBImg, txt2img } from "web_sd_shared_types/03_sd_t";
import { DBEdge } from "web_sd_shared_types/04_edge_t";

export type nodeCreateWCb = (db_node: DBNode, cb: () => void | undefined) => Promise<void>;
export type edgeCreateWCb = (db_node: DBEdge, cb: () => void | undefined) => Promise<void>;
export type imgCreateCb = (db_node: DBImg, cb: () => void | undefined) => Promise<void>;

export interface T2iOprionals {
    t2i : txt2img | undefined
    prog : progress | undefined
 }