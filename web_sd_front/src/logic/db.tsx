import { DBSchema, openDB } from "idb";
import { DBNode } from "web_sd_shared_types/01_node_t";
import { DBEdge } from "web_sd_shared_types/04_edge_t";
import { DBImg } from "web_sd_shared_types/03_sd_t";

const IMG_FIELD = "img";
const NODE_FIELD = "node";
const EDGE_FIELD = "edge";

interface Wb_Sd_Db extends DBSchema {
    img: {
        key: number;
        value: DBImg;
    };
    node: {
        key: number;
        value: DBNode;
    };
    edge: {
        key: number;
        value: DBEdge;
    };
}

export let initDB = async () => {
    let db = await openDB<Wb_Sd_Db>('web_sd_db', 1, {
        upgrade(db) {
            db.createObjectStore(IMG_FIELD, { keyPath: 'id' });
            db.createObjectStore(NODE_FIELD, { keyPath: 'id' });
            db.createObjectStore(EDGE_FIELD, { keyPath: 'id' });
        },
    });
    return db;
}

export let getDB = async () => {
    return await openDB<Wb_Sd_Db>('web_sd_db', 1)
}

const _get_store = async (store_name: any) => {
    const db = await getDB();
    const tx = db.transaction(store_name, 'readwrite');
    const store = tx.objectStore(store_name);
    return store;
}

export let getAllDBNodes = async () => {
    const db = await initDB();
    const all_nodes: DBNode[] = await db.getAll(NODE_FIELD);
    return all_nodes;
}

export let getDBNode = async (id: number) => {
    let job = _get_store(NODE_FIELD)
        .then((store) => store.get(id) as Promise<DBNode>)

    return await job;
}

export let addDBNode = async (new_node: DBNode) => {
    let job = _get_store(NODE_FIELD)
        .then((store) => store.add(new_node))
    return await job
}


export let editDBNode = async (id: number, updated_value: DBNode) => {
    let store = await _get_store(NODE_FIELD)
    let prev = await store.get(id) as DBNode
    if (prev)
        await store.put(updated_value);

    return prev;
}

export let getAllDBEdges = async () => {
    const db = await initDB();
    const all_edges: DBEdge[] = await db.getAll(EDGE_FIELD);
    return all_edges;
}

export let getDBEdge = async (id: number) => {
    let job = _get_store(EDGE_FIELD)
        .then((store) => store.get(id) as Promise<DBEdge>)
    return await job
}

export let addDBEdge = async (new_edge: DBEdge) => {
    let job = _get_store(EDGE_FIELD)
        .then((store) => store.add(new_edge))
    return await job
}

export let editDBEdge = async (id: number, updated_value: DBEdge) => {
    let store = await _get_store(EDGE_FIELD)
    let edge = await store.get(id)
    if (edge) {
        await store.put(updated_value);
    }
}

export let getDBImg = async (id: number) => {
    let job = _get_store(IMG_FIELD)
        .then((store) => store.get(id) as Promise<DBImg>)

    return await job;
}

export let addDBImg = async (new_node: DBImg) => {
    let job = _get_store(IMG_FIELD)
        .then((store) => store.add(new_node))
    return await job
}

// get all img ids from img store
export let getAllDBImgIds = async () => {
    const db = await initDB();
    const all_img_ids: number[] = await db.getAllKeys(IMG_FIELD);
    return all_img_ids;
}