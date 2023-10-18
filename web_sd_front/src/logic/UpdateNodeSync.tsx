import { set } from "lodash";
import { editDBNode, getDBNode } from "./db";
import { ClientServerBridge } from "./ClientServerBridge";

import { NodePosition } from "web_sd_shared_types/00_flow_t";
import { DBNode, ImageType } from "web_sd_shared_types/01_node_t";
import { promptConfig } from "web_sd_shared_types/03_sd_t";

class updateStruct {
    id: number;
    update_queue: (() => Promise<void>)[] = [];
    changes_num: number = 0;
    is_spinning: boolean = false;
    is_serv_syncing: boolean = false;

    constructor(id: number) {
        this.id = id;
    }

    sync_barier_on = () => {
        this.is_serv_syncing = true;
        this.changes_num = 0;
    }

    sync_barier_off = () => {
        this.is_serv_syncing = false;
    }

    is_blocking = () => {
        return this.is_spinning || this.is_serv_syncing;
    }
}

export class UpdateNodeSync {
    private static instance: UpdateNodeSync;
    private node_queues: { [key: number]: updateStruct } = {};

    public static getInstance(): UpdateNodeSync {
        if (!UpdateNodeSync.instance) {
            UpdateNodeSync.instance = new UpdateNodeSync();
        }

        return UpdateNodeSync.instance;
    }

    //mechanism
    private get_update_struct_safe = (id: number) => {
        if (!(id in this.node_queues))
            this.node_queues[id] = new updateStruct(id);

        return this.node_queues[id];
    }

    private respin = (up_st: updateStruct) => {
        let next_spin = () => {
            up_st.is_spinning = false;
            this.run_update_and_reduce(up_st.id)
        }

        setTimeout(next_spin, 0);
    }

    private server_sync = (db_node: DBNode) => {
        return new Promise<DBNode>((resolve, reject) => {
            ClientServerBridge.getInstance()
                .update_node(db_node, async (serv_node_out) => resolve(serv_node_out.db_node));
        });
    }


    // main pipeline
    private run_update_and_reduce = (id: number) => {
        let hasKey = id.toString() in this.node_queues;
        if (!hasKey)
            return;

        let up_St = this.node_queues[id];
        if(up_St.is_blocking())
            return;

        up_St.is_spinning = true;
        this.try_to_run_update(up_St)
            .then(() =>this.try_reduce_queue(up_St.id))
            .then((continue_flag) => {
                if (continue_flag)
                    this.respin(up_St)
                else
                    up_St.is_spinning = false;
            });
    }

    
    private try_to_run_update = (up_st: updateStruct) => {
        if (up_st.update_queue.length == 0)
            return new Promise<void>((resolve, reject) => resolve());

        let update_promise = up_st.update_queue.shift();
        if (!update_promise)
            return new Promise<void>((resolve, reject) => resolve());

        up_st.changes_num += 1;
        return update_promise()
            .then(() => console.log('+SYNC+ update for node: ', up_st.id))

    }

    
    private try_reduce_queue = (id: number) => {
        let up_st = this.node_queues[id];
        if (up_st.update_queue.length > 0)
            return new Promise<boolean>((resolve, reject) => resolve(true));

        if (up_st.changes_num == 0) {
            delete this.node_queues[id];
            console.log('+SYNC+ finished: ', id);
            return new Promise<boolean>((resolve, reject) => resolve(false));
        }

        console.log('+SYNC+ server start: ', id);
        up_st.sync_barier_on();
        return getDBNode(id)
            .then(this.server_sync)
            .then((db_node) => editDBNode(id, db_node))
            .then(() => console.log('+SYNC+ server finish: ', id))
            .then(() => up_st.sync_barier_off())
            .then(() => true)
    }


    // interactions
    private _update_position = async (id: number, pos: NodePosition) => {
        return getDBNode(id)
        .then((db_node) => {
            console.log('+SYNC+ new pos: ', pos, " for node: ", id);
            console.log('+SYNC+ db old pos: ', db_node.position);
            return db_node;
        })        
        .then((old_db_node) => {
            old_db_node.position = pos;
            return editDBNode(id, old_db_node);
        })
        .then(async () => {
            let new_db_node = await getDBNode(id)
            console.log('+SYNC+ db new pos: ', new_db_node.position);
            return;
        })
        .then(() => console.log('+SYNC+ sync test'))
    }

    public update_position(id: number, pos: NodePosition) {
        console.log('+SYNC+ update_position: ', id, pos);
        let queue = this.get_update_struct_safe(id)
        queue.update_queue.push(() => this._update_position(id, pos));
        this.run_update_and_reduce(id);
    }

    private _update_result_img = async (id: number, img_id: number, img_type: ImageType) => {
        return getDBNode(id).then(async (db_node) => {
            db_node.result_data.prompt_img_id = img_id;
            db_node.result_data.prompt_img_type = img_type;
            await editDBNode(db_node.id, db_node);
            return;
        });
    }

    public update_result_img(id: number, img_id: number, img_type: ImageType) {
        let queue = this.get_update_struct_safe(id)
        queue.update_queue.push(() => this._update_result_img(id, img_id, img_type));
        this.run_update_and_reduce(id);
    }

    private _update_result_prompt = async (id: number, prompt: promptConfig, finished: boolean) => {
        return getDBNode(id).then(async (db_node) => {
            db_node.result_data.prompt = prompt;
            db_node.result_data.prompt_finished = finished;
            await editDBNode(db_node.id, db_node);
            return;
        });
    }

    public update_result_prompt(id: number, prompt: promptConfig, finished: boolean) {
        let queue = this.get_update_struct_safe(id)
        queue.update_queue.push(() => this._update_result_prompt(id, prompt, finished));
        this.run_update_and_reduce(id);
    }
}