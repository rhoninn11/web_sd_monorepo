import { mtdta_JSON_id } from "web_sd_shared_types/02_serv_t";
import { img2img, img64, promptConfig, txt2img } from "web_sd_shared_types/03_sd_t";

export const prompt_to_txt2img = (prompt: promptConfig, node_db_id: number): txt2img => {

    let txt_to_img: txt2img = {
        txt2img: {
            metadata: { id: JSON.stringify(new mtdta_JSON_id('', -1, node_db_id)) },
            bulk: { img: new img64() },
            config: prompt
        }
    };

    return txt_to_img;
}

export const prompt_to_img2img = (prompt: promptConfig, image_id: number, node_db_id: number): img2img => {

    let ref_img = new img64()
    ref_img.id = image_id;

    let img_to_img: img2img = {
        img2img: {
            metadata: { id: JSON.stringify(new mtdta_JSON_id('', -1, node_db_id))},
            bulk: { img: ref_img },
            config: prompt
        }
    };

    return img_to_img;
}


export const is_prompt_empty = (prompt: promptConfig): boolean => {
    return prompt.prompt === '' && prompt.prompt_negative === '';
}

export const start_chain = () => {
    return new Promise<void>((resolve, reject) => resolve())
}

export const generic_prompt = () => {
    let sample_prompt = new promptConfig();
    sample_prompt.prompt = "Cozy italian vilage";
    sample_prompt.prompt_negative = "Boring sky";
    return sample_prompt;
}
