
import React, { useState } from "react";

interface DevPasswordProps {
    on_login: (password: string) => void;
}

export const DevPasswordInput = ({
    on_login
}:DevPasswordProps) => {

    const try_to_login = (event: React.ChangeEvent<HTMLSelectElement>) => {
        let password = event.target.value;
        on_login(password)
    };

    return (
        <select onChange={try_to_login}>
            <option value="none">none</option>
            <option value="policjantZawodLaskowy51+">usr_0</option>
            <option value="myszKsztalcenieAgrest80-">usr_1</option>
            <option value="zukInternetBak39.">usr_2</option>
            <option value="muzeumRurkaPapier40,">usr_3</option>
            <option value="filmMyszkaKomputer18+">usr_4</option>
            <option value="uczenJeziorakKoce36,">usr_5</option>
        </select>
    )


}