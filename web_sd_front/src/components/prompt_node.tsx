import styles from './prompt_node.module.scss';
import styles_shered from "./shered_styles.module.scss"

import React, { memo, useEffect, useState } from 'react';
import { Handle, NodeProps, Position } from 'reactflow';

import { Button, Intent, ProgressBar } from '@blueprintjs/core';
import { useServerContext } from './SocketProvider';


import { ImageType, NodeConnData, PromptReference } from 'web_sd_shared_types/01_node_t';
import { DBImg, img64, promptConfig} from 'web_sd_shared_types/03_sd_t';

import { addDBImg, getDBImg, getDBNode } from '../logic/db';
import { MenuTest } from './menu_test';
import { UpdateNodeSync } from '../logic/UpdateNodeSync';
import { generic_prompt, is_prompt_empty, start_chain } from '../logic/dono_utils';
import classNames from 'classnames';
import { NotificationToster } from './info_panel';
import { RecipeOverlayWrapper } from './prompt_overlay_wrapper';
import { MySdImg } from './Img_wrapper';


const _PromptNode = ({ data }: NodeProps<NodeConnData>) => {
	const { isAuthenticated, userId } = useServerContext();

	const [inited, setInited] = useState(false);

	const [initPrompt, setInitPrompt] = useState(new promptConfig());
	const [resultPrompt, setResultPrompt] = useState(new promptConfig());
	const [resultPromptFinished, setResultPromptFinished] = useState(false);

	const [showOoverlay, setShowOverlay] = useState(false);
	const [progress, setProgress] = useState(0.0);

	const [initImg, setInitImg] = useState(new img64());
	const [resultImg, setResultImg] = useState(new img64());
	const [resultImgFinished, setResultImgFinished] = useState(false);

	const [resultImgType, setResultImgType] = useState(ImageType.NONE);

	let is_owner = data.node_data.user_id == userId
	let edit_cond = isAuthenticated && is_owner;


	const result_img_save2db = async (web_img64: img64, user_id: number, img_type: ImageType) => {
		let new_db_img = new DBImg().from(web_img64);
		new_db_img.user_id = user_id;
		await addDBImg(new_db_img);
		let db_id = parseInt(data.node_data.id);
		UpdateNodeSync.getInstance().update_result_img(db_id, web_img64.id, img_type);
	}

	const result_prompt_save2db = async (prompt: promptConfig) => {
		let node_db_id = parseInt(data.node_data.id);
		UpdateNodeSync.getInstance().update_result_prompt(node_db_id, prompt, true);
		return node_db_id;
	}


	// result data
	const set_result_img = (img: img64, img_type: ImageType) => {

		setResultImgFinished(true);
		setResultImg(img);
		setResultImgType(img_type)
	}

	const try_fetch_result_img = async (img_id: number, img_type: ImageType) => {
		if (img_id == -1)
			return new Promise<void>((resolve, reject) => resolve());

		return getDBImg(img_id).then((db_img) => set_result_img(db_img.img, img_type));
	}

	const set_result_prompt = (prompt: promptConfig, finished: boolean) => {
		setResultPrompt(prompt);
		setResultPromptFinished(finished);
	}

	const try_fetch_result_data = (prompt_ref: PromptReference) : Promise<void> => {
		set_result_prompt(prompt_ref.prompt, prompt_ref.prompt_finished);
		let result_img_id = prompt_ref.prompt_img_id;
		let result_img_type = prompt_ref.prompt_img_type;
		return try_fetch_result_img(result_img_id, result_img_type);
	}

	// initial data
	const set_init_img = (img: img64) => {
		setInitImg(img);
	}

	const try_fetch_init_img = async (img_id: number) => {
		if (img_id == -1)
			return new Promise<void>((resolve, reject) => resolve());

		return getDBImg(img_id).then((db_img) => set_init_img(db_img.img));
	}

	const try_fetch_initial_data = () : Promise<void> => {
		let init_node_id = data.node_data.initial_node_id;
		if (init_node_id == -1) {
			setInitPrompt(generic_prompt());
			return new Promise<void>((resolve, reject) => resolve());
		}

		return getDBNode(init_node_id)
			.then((db_node) => {
				setInitPrompt(db_node.result_data.prompt);
				return db_node.result_data.prompt_img_id;
			})
			.then((img_id) => try_fetch_init_img(img_id))

	}
	

	useEffect(() => {
		const fetchData = async () => {
			let prompt_ref = data.node_data.result_data;
			await try_fetch_initial_data()
			await try_fetch_result_data(prompt_ref)
		};

		start_chain()
			.then(() => fetchData())
			.then(() => setInited(true))
	}, []);

	useEffect(() => {
		const updateData = async () => {
			let prompt_ref = data.node_data.result_data;
			await try_fetch_result_data(prompt_ref)
		};

		if (!inited)
			return;

		start_chain()
			.then(() => updateData())

	}, [inited, data]);

	const on_prompt_complete = (prompt: promptConfig) => {
		set_result_prompt(prompt, true);
		return result_prompt_save2db(prompt);
	}

	const on_img_complete = async (web_img64: img64, user_id: number, img_type: ImageType) => {
		await result_img_save2db(web_img64, user_id, img_type);
		set_result_img(web_img64, img_type);
		setProgress(0.0);
	}

	const on_progress = (prog_val: number) => {
		setProgress(prog_val);

	}


	//  -----------------  overlay stuff -----------------
	let ShowPromptOverlay = () => {
		setShowOverlay(true);
	}

	let show_btn = !resultPromptFinished
	let oberlay_btn = show_btn ?
		<Button onClick={ShowPromptOverlay} disabled={resultPromptFinished || !edit_cond} rightIcon="edit" intent={Intent.PRIMARY}>
			Describe
		</Button>
		: null


	let overlay_prompt = is_prompt_empty(resultPrompt) ? initPrompt : resultPrompt;
	let prompt_overlay_wrap = showOoverlay ? <RecipeOverlayWrapper
		title={'Image prompt options'}
		on_close={() => setShowOverlay(false)}
		on_progress={on_progress}
		on_img_complete={on_img_complete}
		on_prompt_complete={on_prompt_complete}
		ovelay_prompt={overlay_prompt}
		overlay_img={initImg}
		edit_cond={edit_cond}
	/> : null

	const add_notification = (title: string, msg: string) => {
		const elo = <div><b>{title}</b>: {msg}</div>
		NotificationToster.show({ message: elo, intent: Intent.NONE })
	}

	let help_menu = <MenuTest
		prompt={overlay_prompt}
		copied={add_notification}
		refresh={async () => {
			await try_fetch_initial_data()
		}}
		imgType={resultImgType} />

	let show_progress_bar = resultPromptFinished && !resultImgFinished && edit_cond;
	let progress_bar = show_progress_bar ? <ProgressBar value={progress} /> : null;

	let show_image = resultImgFinished || resultPromptFinished;
	let generated_img_alt = <MySdImg img_64={resultImg} show={show_image} complete={resultImgFinished} />

	let display_content = <div>
		{oberlay_btn}
		{prompt_overlay_wrap}
		{generated_img_alt}
		{progress_bar}
		{help_menu}
	</div>

	const boxClasses = classNames(
		styles.nice_box,
		edit_cond ? styles.this_user_node : styles.other_users_node,
	)
	
	let bigger_handl_style = { background: '#784be8', width: "15px", height: "30px", borderRadius: "3px" };
	return (
		<>
			<Handle
				type="target"
				position={Position.Left}
				style={bigger_handl_style}
				onConnect={(params) => console.log('handle onConnect left', params)}
				isConnectable={true}
			/>
			<div className={boxClasses}>
				Stable diffusion XL
				{display_content}

			</div>
			<Handle
				type="source"
				position={Position.Right}
				id="a"
				style={bigger_handl_style}
				isConnectable={true}
			/>
		</>
	);
}

export const PromptNode = memo(_PromptNode);


