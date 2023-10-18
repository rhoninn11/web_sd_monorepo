import styles_shered from "./shered_styles.module.scss"
// import styles from "./prompt_overlay.module.scss"
import { Classes, Menu, MenuItem, NumericInput, Position } from "@blueprintjs/core";
import { useEffect, useState } from "react";
import { UserModule } from "../logic/UserModule";

interface InfoPanelProps {
    className?: string;
    children?: React.ReactNode;
}

export const InfoPanel = ({
    className,
    children,
}: InfoPanelProps) => {

    const { isAuthenticated, isConnected, isSynced, isSyncing, userId } = useServerContext();

    let auth_text = isAuthenticated ? 'Authenticated' : 'Not authenticated'
    let auth_class = isAuthenticated ? styles_shered.grean_text : styles_shered.red_text;

    let connect_text = isConnected ? 'Connected' : 'Not connected'
    let connect_class = isConnected ? styles_shered.grean_text : styles_shered.red_text;

    let sync_text = isSynced ? 'Synec' : isSyncing ? 'Syncing...' : 'Not synced'
    let syncc_class = isSynced ? styles_shered.grean_text : isSyncing ? styles_shered.yellow_text : styles_shered.red_text;

    let user_id_text = isAuthenticated ? userId : '---'

    const login = (password: string) => {
        if (!isConnected) {
            return;
        }

        UserModule.getInstance().setPasswd(password)
        UserModule.getInstance().askForAuth()
    };
    let dev = import.meta.env.DEV;
    let login_option = dev
        ? <DevPasswordInput on_login={login} />
        : <PasswordInput on_login={login} isAuthenticated={isAuthenticated}/>

    return (
        <div className={Classes.ELEVATION_1} style={{ padding: "10px" }}>
            <div className={connect_class}>{connect_text}</div>
            <div className={auth_class}>{auth_text}</div>
            <div className={syncc_class}>{sync_text}</div>
            <div>User id: {user_id_text}</div>
            {login_option}




        </div>
    );
};

import { OverlayToaster } from "@blueprintjs/core";
import { ClientServerBridge } from "../logic/ClientServerBridge";
import { useServerContext } from "./SocketProvider";
import { DevPasswordInput } from "./pass/password_dev";
import { PasswordInput } from "./pass/password";


export const NotificationToster = OverlayToaster.create({
    className: "recipe-toaster",
    position: Position.BOTTOM,
});


export const SyncInfoToster = OverlayToaster.create({
    className: "recipe-toaster",
    position: Position.TOP,
});

