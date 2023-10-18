import _  from 'lodash';
import styles from './flow_hub.module.scss';

import React, { useCallback, useEffect, useRef, useState, MouseEvent } from 'react';
import ReactFlow, {
	useNodesState,
	useEdgesState,
	addEdge,
	useReactFlow,
	ReactFlowProvider,
	MiniMap,
	Controls,
	Background,
	OnMove,
	Viewport,
	Panel,
} from 'reactflow';
import 'reactflow/dist/style.css';

import { PromptNode } from './prompt_node';
import { PromptEdge } from './prompt_edge';


import { addDBNode, addDBEdge, getAllDBEdges, getAllDBNodes, getDBNode, editDBNode, getAllDBImgIds, addDBImg, getDBEdge, getDBImg } from '../logic/db';
import { edge_db2flow, node_db2flow } from '../logic/convert_utils';
import { ClientServerBridge } from '../logic/ClientServerBridge';

// types
import { moveCB } from '../tests/canvas_move_test';

import { MoveObserver } from '../tests/canvas_move_test';

import { DBNode, FlowNode, PromptReference} from 'web_sd_shared_types/01_node_t';
import { syncOps, syncSignature } from 'web_sd_shared_types/02_serv_t';
import { DBImg } from 'web_sd_shared_types/03_sd_t';
import { DBEdge } from 'web_sd_shared_types/04_edge_t';

import { UpdateNodeSync } from '../logic/UpdateNodeSync';
import { sync_client_nodes_with_server, sync_client_edges_with_server, sync_client_img_with_server } from '../logic/ServerSyncREalated';
import { edgeCreateWCb, imgCreateCb, nodeCreateWCb } from '../types/types_db';
import { UserModule } from '../logic/UserModule';
import { InfoPanel } from './info_panel';
import { start_chain } from '../logic/dono_utils';
import { useServerContext } from './SocketProvider';

const nodeTypes = {
	prompt: PromptNode,
}

const edgeTypes = {
	prompt: PromptEdge,
}

interface AllData {
	nodes: DBNode[],
	edges: DBEdge[],
	imgs: DBImg[]
}

const fitViewOptions = {
	padding: 3,
};

interface NodeTracker {
	node_id: string;
	prompt_ref: PromptReference;
}

const AddNodeOnEdgeDrop = () => {
	const reactFlowWrapper = useRef<HTMLDivElement>(null);
	const nodeConnectSource = useRef<NodeTracker>({ node_id: '', prompt_ref: new PromptReference() });
	// const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
	const [nodes, setNodes, onNodesChange] = useNodesState([]);
	const [edges, setEdges, onEdgesChange] = useEdgesState([]);
	const { project } = useReactFlow();
	const [allowCreate, setAllowCreate] = useState(false);

	const [validUser, setValidUser] = useState(false);
	const [userId, setUserId] = useState(-1);

	const {isConnected, isAuthenticated, isSynced, setSynced, setSyncing} = useServerContext();

	const onConnect = useCallback((params) => setEdges((eds) => addEdge(params, eds)), []);

	const get_prompt_ref = (id: string) => {
		let this_node = nodes.find((node) => node.id === id)
		if (this_node) {
			let legit_node = this_node as FlowNode
			return legit_node.data.node_data.result_data;
		}
		return new PromptReference()
	}

	const onConnectStart = useCallback((eventInfo, nodeInfo) => {
		let nodeId = nodeInfo?.nodeId;
		nodeConnectSource.current.node_id = nodeId;
		nodeConnectSource.current.prompt_ref = get_prompt_ref(nodeId);

	}, [nodes]);

	const onNodeDragFinished = useCallback((_0, node, _1) => {
		let flow_node: FlowNode = node;
		let id: number = parseInt(flow_node.id);
		let position = flow_node.position;
		if (validUser) {
			UpdateNodeSync.getInstance().update_position(id, position);
		}

	}, [validUser])

	// node


	let add_node: nodeCreateWCb = async (db_node: DBNode, cb: () => void | undefined) => {
		let _flow_node = node_db2flow(db_node);
		if (userId >= 0 && db_node.user_id == userId) {
			_flow_node.draggable = true;
		}
		setNodes((nds) => nds.concat(_flow_node));
		await addDBNode(db_node);
		if (cb) cb();
	}

	let edit_flow_node = (db_node: DBNode) => {
		// Wniosek:	 	edycja tego nie resetuje noda, ale nie odświeżają się też dane w nodzie
		// 				dopiero jak nastąpi jakaś interakcja z nodem to się odświeża
		setNodes((nds) => nds.map((node) => {
			if (node.id == db_node.id.toString()) {
				let _flow_node = node_db2flow(db_node);
				_flow_node.data = { ..._flow_node.data }
				return _flow_node;
			}
			return node;
		}))
	}

	let edit_node: nodeCreateWCb = async (db_node_edit: DBNode, cb: () => void | undefined) => {
		console.log("!!! node edit")
		let prev_node = await getDBNode(db_node_edit.id);
		if (!prev_node)
			return await add_node(db_node_edit, cb);

		if (prev_node.timestamp >= db_node_edit.timestamp) {
			if (cb) cb();
			return;
		}

		await editDBNode(db_node_edit.id, db_node_edit);
		edit_flow_node(db_node_edit)
		if (cb) cb();
	}

	//edge
	let add_edge: edgeCreateWCb = async (db_edge: DBEdge, cb: () => void | undefined) => {
		console.log("!!! node edit")
		let existing_edge = await getDBEdge(db_edge.id);
		if (!existing_edge)
			return await _add_edge(db_edge, cb);
	}

	let _add_edge: edgeCreateWCb = async (db_edge: DBEdge, cb: () => void | undefined) => {
		console.log("!!!add_edge", db_edge)
		let _flow_edge = edge_db2flow(db_edge);
		setEdges((eds) => eds.concat(_flow_edge));
		await addDBEdge(db_edge);
		if (cb) cb();
	}


	//img
	let add_img: imgCreateCb = async (db_img: DBImg, cb: () => void | undefined) => {
		let existing_img = await getDBImg(db_img.id)
		if (!existing_img)
			return await _add_img(db_img, cb);
	}

	let _add_img: imgCreateCb = async (db_img: DBImg, cb: () => void | undefined) => {
		await addDBImg(db_img);
		if (cb) cb();
	}


	// create
	let ask_serv_to_create_node = (db_node: DBNode) => {
		return new Promise<DBNode>((resolve, reject) => {
			ClientServerBridge.getInstance()
				.create_node(db_node, (serv_node) => add_node(serv_node.db_node, () => resolve(serv_node.db_node)));
		});

	}

	let ask_serv_to_create_edge = (db_edge: DBEdge) => {
		return new Promise<DBEdge>((resolve, reject) => {
			ClientServerBridge.getInstance()
				.create_edge(db_edge, (serv_edge) => add_edge(serv_edge.db_edge, () => resolve(serv_edge.db_edge)));
		});

	}

	let asign_edge_target = (db_edge: DBEdge, db_node: DBNode) => {
		return new Promise<DBEdge>((resolve, reject) => {
			db_edge.target = db_node.id.toString();
			resolve(db_edge);
		});
	}

	const create_first_node = () => {
		setAllowCreate(false);

		const xy_pos = { x: 0, y: 0 }

		let db_node = new DBNode();
		db_node.position = project(xy_pos);

		ask_serv_to_create_node(db_node)
			.then(() => {
				setAllowCreate(true)
				console.log('!!! first node created !!!')
			})
	}

	const create_next_node = async (event: any, div: HTMLDivElement, sourceNodeData: NodeTracker) => {
		setAllowCreate(false);
		let prompt_data = sourceNodeData.prompt_ref

		const { top, left } = div.getBoundingClientRect();
		const xy_pos = { x: event.clientX - left - 75, y: event.clientY - top }

		let db_node = new DBNode();
		db_node.position = project(xy_pos);
		db_node.initial_node_id = parseInt(sourceNodeData.node_id);


		let lul = new DBEdge();
		lul.source = nodeConnectSource.current.node_id;

		ask_serv_to_create_node(db_node)
			.then((serv_db_node) => asign_edge_target(lul, serv_db_node))
			.then((proccessed_db_edge) => ask_serv_to_create_edge(proccessed_db_edge))
			.then(() => setAllowCreate(true))
	}

	// placing
	const place_node = (event: any) => {
		const targetIsPane = event.target.classList.contains('react-flow__pane');

		if (targetIsPane && allowCreate)
			if (reactFlowWrapper && reactFlowWrapper.current)
				create_next_node(event, reactFlowWrapper.current, nodeConnectSource.current);
	}

	const onConnectEnd = useCallback(place_node, [project, allowCreate]);


	// init step 1 
	const fetchData = async () => {
		let db_nodes = await getAllDBNodes()
		let db_edges = await getAllDBEdges()

		

		// just id fetch, meaby faser then all bulk data fetch idono
		let imgIds = (await getAllDBImgIds()).map((id) => {
			let db_img_shell = new DBImg();
			db_img_shell.id = id;
			return db_img_shell;
		});

		let all_data = {
			nodes: db_nodes,
			edges: db_edges,
			imgs: imgIds
		}

		return all_data;
	};

	const setFlow = (allData: AllData) => {
		const {nodes, edges} = allData;
		const flow_nodes = nodes.map(node_db2flow)
		const flow_edges = edges.map(edge_db2flow)
		setNodes(flow_nodes);
		setEdges(flow_edges);
	}

	// init step 2
	const auth_check_async_loop = (on_auth: () => void, retry_time: number) => {
		if (UserModule.getInstance().isAuthenticated()) {
			on_auth();
		}
		else
			setTimeout(() => auth_check_async_loop(on_auth, retry_time), retry_time);
	}

	const checkAuth = () => {
		let auth_loop = new Promise<void>((resolve, reject) => {
			auth_check_async_loop(resolve, 100);
		})

		let auth_chain = auth_loop
			.then(() => console.log('+INFO+ user authenticated'))
			.then(() => {
				let usr_id = UserModule.getInstance().getUserId();
				setValidUser(true);
				setUserId(usr_id);
				return usr_id;
			})

		return auth_chain;
	}

	// init step 3
	const initialServerSync = (local_data: AllData) => {
		let sync_data_in = new syncSignature()
		sync_data_in.sync_op = syncOps.INFO;

		const { nodes, edges, imgs } = local_data;
		sync_data_in.fill_ids(nodes, edges, imgs);

		const chain = new Promise<number>((resolve, reject) => {
			ClientServerBridge.getInstance()
				.sync_with_server(sync_data_in, (sync_data_out) => {
					console.log("+HUB+ serv returned TS_INFO")
					if (sync_data_out.sync_op != syncOps.INFO)
						return;

					// server just returned id list
					const node_num = nodes.length + sync_data_out.node_id_arr.length;
					sync_client_with_server(sync_data_out)
						.then(() => resolve(node_num));
				});
		});

		return chain;
	}

	const inialTimestepServerSync = async () => {
		const sync_op = syncOps.INFO_TS;
		let sync_data_in = new syncSignature()
		sync_data_in.sync_op = sync_op;

		let nodes = await getAllDBNodes();
		let simple_nodes = nodes.map((node) => {
			let simple_node = new DBNode();
			simple_node.id = node.id;
			simple_node.timestamp = node.timestamp;
			return simple_node;
		})
		sync_data_in.fill_data(simple_nodes, [], []);

		let chain = new Promise<number>((resolve, reject) => {
			ClientServerBridge.getInstance()
				.sync_timestump_with_server(sync_data_in, (sync_data_out) => {
					console.log("+HUB+ serv returned TS_INFO")
					if (sync_data_out.sync_op != sync_op)
						return;

					// server just returned id list
					sync_client_ts_with_server(sync_data_out)
						.then(() => resolve(nodes.length));
				});
		});

		return chain;
	}

	let sync_sygn_empty = (s_sygn :syncSignature): boolean => {
		let cond = s_sygn.node_id_arr.length == 0 && s_sygn.edge_id_arr.length == 0 && s_sygn.img_id_arr.length == 0;
		return cond
	}

	const RtServerSync = async () => {
		const sync_op = syncOps.RT_SYNC;
		let sync_data_in = new syncSignature()
		sync_data_in.sync_op = sync_op;

		const chain = new Promise<number>((resolve, reject) => {
			ClientServerBridge.getInstance()
				.sync_with_server(sync_data_in, (sync_data_out) => {
					// console.log("+HUB+ serv returned RT_SYNC")
					if (sync_data_out.sync_op != sync_op)
						return;

					// console.log(" +ISYNC+ node_id_arr", sync_data_out);
					if(sync_sygn_empty(sync_data_out)){
						resolve(0);
						return;
					}
					// server just returned id list
					let node_num = nodes.length + sync_data_out.node_id_arr.length;
					sync_client_with_server(sync_data_out)
						.then(() => resolve(node_num));
				});
		});

		return chain;
	}

	// chains
	const sync_client_with_server = (s_sygn: syncSignature) => {
		let { node_id_arr, edge_id_arr, img_id_arr } = s_sygn;
		// console.log(" +ISYNC+ node_id_arr", node_id_arr);
		// console.log(" +ISYNC+ edge_id_arr", edge_id_arr);
		// console.log(" +ISYNC+ img_id_arr", img_id_arr);

		let sync_chain = start_chain()
			.then(() => sync_client_img_with_server(img_id_arr, add_img))
			.then(() => sync_client_edges_with_server(edge_id_arr, add_edge))
			.then(() => sync_client_nodes_with_server(node_id_arr, edit_node))
			.then(() => console.log('+INFO+ server synced'))

		return sync_chain;
	}

	const sync_client_ts_with_server = (s_sygn: syncSignature) => {
		let { node_id_arr } = s_sygn;
		// console.log(" +ITSSYNC+ node_data_arr", node_id_arr);
		let sync_chain = start_chain()
			.then(() => sync_client_nodes_with_server(node_id_arr, edit_node))
			.then(() => console.log('+INFO+ timpestump server synced'))

		return sync_chain;
	}

	const releaseUserNodes = (user_id: number) => {
		setNodes((nds) => nds.map((node) => {
			let flow_node = node as FlowNode;
			if (flow_node.data.node_data.user_id == user_id)
				flow_node.draggable = true;
			return flow_node;
		}))
	}

	useEffect(() => {
		let local_data: AllData = { nodes: [], edges: [], imgs: [] };
		let node_num_data = 0;
		let user_id_data = -1;
		start_chain()
			.then(() => fetchData())
			.then((data) => local_data = data)
			.then(() => setFlow(local_data))
			.then(checkAuth)
			.then((user_id) => user_id_data = user_id)
			.then(() => setSyncing(true))
			.then(() => initialServerSync(local_data))
			.then((node_num) => node_num_data = node_num)
			.then(() => inialTimestepServerSync())
			.then(() => releaseUserNodes(user_id_data))
			.then(() => {
				setAllowCreate(true)
				if (node_num_data == 0)
					create_first_node();
			}).then(() => setSynced(true))

	}, []);


	useEffect(() => {
		if(isConnected) {
			console.log("+++ from flow_hub: connected")
		}
	}, [isAuthenticated, isConnected])

	const rt_sync_loop = () => {

		// console.log("!!! RT SYNC (loop started)!!!")
		RtServerSync().then((node_num) => {
			// console.log("!!! RT SYNC (loop finished)!!!")
			let update_time = 1000;
			if (node_num > 0)
				update_time = 0;
			setTimeout(() => rt_sync_loop(), update_time);
		})
	}

	useEffect(() => {
		if(isSynced){
			setTimeout(rt_sync_loop, 0);
		}
	}, [isSynced])


	const move_obs = MoveObserver.getInstance();
	return (
		<div className={styles.full_screan_wrapper} ref={reactFlowWrapper}>

			<ReactFlow
				nodes={nodes}
				edges={edges}
				onNodesChange={onNodesChange}
				onEdgesChange={onEdgesChange}
				onConnect={onConnect}
				onConnectStart={onConnectStart}
				onConnectEnd={onConnectEnd}
				onNodeDragStop={onNodeDragFinished}
				fitView
				fitViewOptions={fitViewOptions}
				nodeTypes={nodeTypes}
				// edgeTypes={edgeTypes}
				onMoveStart={move_obs.onMoveStart}
				onMove={move_obs.onMove}
				onMoveEnd={move_obs.onMoveEnd}

				minZoom={0.125}
				maxZoom={4}
				deleteKeyCode={null}
			>
				<Panel position="top-left"><InfoPanel /></Panel>
				<MiniMap />
				<Controls />
				<Background />
			</ReactFlow>


		</div>
	);
};


export const Flow = () => {
	return (
		<ReactFlowProvider>
			<AddNodeOnEdgeDrop />
		</ReactFlowProvider>
	)
};
