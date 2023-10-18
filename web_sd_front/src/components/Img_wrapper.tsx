import classNames from "classnames";
import { img64 } from "web_sd_shared_types/03_sd_t";
import { Classes } from "@blueprintjs/core";

import styles_shered from "./shered_styles.module.scss"


interface MySdImgProps {
    className?: string;
    children?: React.ReactNode;
    show: boolean;
    complete: boolean;
    img_64: img64;
}

export const MySdImg = ({
    className,
    children,
    show,
    complete,
    img_64
}: MySdImgProps) => {

    const classes_img_preview = classNames(
        styles_shered.smaller_img,
        Classes.SKELETON,
    )
    const classes_img = classNames(
        styles_shered.smaller_img,
        styles_shered.prettier_img,
    );

    let img_render = complete ? <img className={classes_img} src={img_64.img64} /> : <div className={classes_img_preview} />
    let my_img = show ? img_render : null;
    
    return my_img;
};
