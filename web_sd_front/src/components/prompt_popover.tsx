import { Button, Classes, Popover } from "@blueprintjs/core";
import { promptConfig } from "web_sd_shared_types/03_sd_t";



interface PromptInfoProps {
    className?: string;
    children?: React.ReactNode;
    init_cfg: promptConfig;
}

export const PromptInfoProps = ({
    className,
    children,
    init_cfg,
}: PromptInfoProps) => {
    return (

        <Popover
            interactionKind="click"
            popoverClassName={Classes.POPOVER_CONTENT_SIZING}
            placement="bottom"
            isOpen={true}
            content={
                <div>
                    <h5>Popover title</h5>
                    <p>...</p>
                    <Button className={Classes.POPOVER_DISMISS} text="Dismiss" />
                </div>
            }
            renderTarget={() => (
                <Button intent="primary" text="Popover target" />
            )}
        />
    )
};