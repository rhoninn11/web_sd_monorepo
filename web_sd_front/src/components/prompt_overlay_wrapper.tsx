import styles from "./prompt_overlay.module.scss"
import styles_shered from "./shered_styles.module.scss"
import { Classes, Slider } from "@blueprintjs/core";
import { Button, TextArea, Label, NumericInput, Switch } from "@blueprintjs/core";
import { Overlay, H3, PortalProvider, Intent } from "@blueprintjs/core";
import { Code } from "@blueprintjs/icons";
import classNames from "classnames";
import { useState } from "react";

import { textAreaEditor } from "../logic/editor-helper";
import { PromptOverlay } from "./prompt_overlay";
import { ClientServerBridge } from "../logic/ClientServerBridge";
import { prompt_to_img2img, prompt_to_txt2img } from "../logic/dono_utils";

import { ImageType } from "web_sd_shared_types/01_node_t";
import { mtdta_JSON_id, progress } from "web_sd_shared_types/02_serv_t";
import { img2img, img64, promptConfig, txt2img } from "web_sd_shared_types/03_sd_t";

interface RecipeOverlayWrapperProps {
    className?: string;
    children?: React.ReactNode;
    title: string;
    on_close: () => void;
    on_progress: (prog_val: number) => void;
    on_img_complete: (web_img64: img64, user_id: number, img_type: ImageType) => void;
    on_prompt_complete: (prompt: promptConfig) => Promise<number>;
    ovelay_prompt: promptConfig;
    overlay_img: img64;
    edit_cond: boolean;
}

export const RecipeOverlayWrapper = ({
    className,
    children,
    title,
    on_close,
    on_progress,
    on_img_complete,
    on_prompt_complete,
    ovelay_prompt,
    overlay_img,
    edit_cond
}: RecipeOverlayWrapperProps) => {

    
	const on_generation_progress = (progr: progress) => {
		on_progress(progr.progress.value);
	}

	const on_txt2img_generation_finish = (result: txt2img) => {
		let web_img64 = result.txt2img.bulk.img;
        let metadata_id = result.txt2img.metadata.id;
        let decoded: mtdta_JSON_id = JSON.parse(metadata_id);
		on_img_complete(web_img64, decoded.user_id, ImageType.TXT2IMG)
	}
	const on_img2img_generation_finish = (result: img2img) => {
		let web_img64 = result.img2img.bulk.img;
        let metadata_id = result.img2img.metadata.id;
        let decoded: mtdta_JSON_id = JSON.parse(metadata_id);
		on_img_complete(web_img64, decoded.user_id, ImageType.IMG2TXT)
    }

	let startTxt2img = async (prompt: promptConfig) => {
		on_close();
		if (!edit_cond)
			return
		
		let node_db_id = await on_prompt_complete(prompt)
		ClientServerBridge.getInstance()
			.send_txt2img(prompt_to_txt2img(prompt, node_db_id), on_generation_progress, on_txt2img_generation_finish)
	}

	let startImg2img = async (prompt: promptConfig, img_id: number) => {
		on_close();
		if (!edit_cond)
			return

        let node_db_id = await on_prompt_complete(prompt)
		ClientServerBridge.getInstance()
			.send_img2img(prompt_to_img2img(prompt, img_id, node_db_id), on_generation_progress, on_img2img_generation_finish)
	}


    return (
        <div>
            <PromptOverlay
                onClose={on_close}
                onTxt2img={startTxt2img}
                onImg2img={startImg2img}
                title={'Image prompt options'}
                init_cfg={ovelay_prompt}
                img_cfg={overlay_img}
            />
        </div>
    );
};
