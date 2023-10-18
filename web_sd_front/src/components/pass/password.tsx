

import React, { useState } from "react";

interface PasswordProps {
    on_login: (password: string) => void;
    isAuthenticated: boolean;
}

export const PasswordInput = ({
        on_login,
        isAuthenticated
    }: PasswordProps )=> {
    const [isPasswordVisible, setPasswordVisible] = useState(false);
    const [password, setPassword] = useState("");

    return (
        <div style={{display: "flex", flexDirection: "column"}}>
            <input
                type={isPasswordVisible && !isAuthenticated ? "text" : "password"}
                placeholder="Your Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={isAuthenticated}
            />
            <label>
                Show password
                <input 
                type="checkbox" 
                checked={isPasswordVisible} 
                onChange={() => setPasswordVisible(!isPasswordVisible)}
                disabled={isAuthenticated}
                />
            </label>
            <button disabled={isAuthenticated}
                onClick={() => on_login(password)}>
                {"Login"}
            </button>
        </div>
    )

}