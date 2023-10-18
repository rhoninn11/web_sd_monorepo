// import styles from "./prompt_overlay.module.scss"
import { Classes, Menu, MenuItem } from "@blueprintjs/core";
import { promptConfig } from "web_sd_shared_types/03_sd_t";
import { ImageType } from "web_sd_shared_types/01_node_t";

interface MenuTestProps {
    className?: string;
    children?: React.ReactNode;
    refresh: () => void;
    copied: (title: string, msg: string) => void;
    prompt: promptConfig;
    imgType: ImageType
}

export const MenuTest = ({
    className,
    children,
    refresh,
    copied,
    prompt,
    imgType
}: MenuTestProps) => {

    let copy_prompt = () => {
        navigator.clipboard.writeText(prompt.prompt)
        copied("Copied prompt", prompt.prompt);
    }

    let copy_neg_prompt = () => {
        navigator.clipboard.writeText(prompt.prompt_negative)
        copied("Copied negative prompt", prompt.prompt_negative);
    }

    let img_type = null;
    if (imgType != ImageType.NONE)
        img_type = <MenuItem disabled={true} icon="info-sign" text={`Result of: \"${imgType}\"`} onClick={() => {}} />

    let img_power = null;
    if (imgType == ImageType.IMG2TXT)
        img_power = <MenuItem disabled={true} icon="info-sign" text={`Image power: \"${(1-prompt.power).toFixed(2)}\"`} onClick={() => {}} />


    return (
        <Menu className={Classes.ELEVATION_1}>
            <MenuItem
                icon={"applications"}
                text="Image"
                children={(
                    <>
                        {/* <MenuItem icon="add" text="Add new" />
                        <MenuItem icon="remove" text="Remove" /> */}
                        <MenuItem icon="clipboard" text={`Prompt: \"${prompt.prompt}\"`} onClick={copy_prompt} />
                        <MenuItem icon="clipboard" text={`Negative prompt: \"${prompt.prompt_negative}\"`} onClick={copy_neg_prompt} />
                        {img_type}
                        <MenuItem disabled={true} icon="info-sign" text={`Seed: \"${prompt.seed}\"`} onClick={() => {}} />
                        {img_power}
                        <MenuItem icon="refresh" text="Refresh initial data" onClick={refresh} />
                    </>
                )}
            />
        </Menu>
    );
};
