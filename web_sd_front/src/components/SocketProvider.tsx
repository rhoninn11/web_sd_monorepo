import React, { createContext, useContext, useEffect, useState } from 'react';
import { UserModule } from '../logic/UserModule';
import { ClientServerBridge } from '../logic/ClientServerBridge';

export interface ServerContextType {
	isAuthenticated: boolean;
	isConnected: boolean;
	isSynced: boolean;
	isSyncing: boolean;
	setSynced: (synced: boolean) => void;
	setSyncing: (syncing: boolean) => void;
	userId: number;
}

const ServerContext = createContext<ServerContextType | undefined>(undefined);

export const ServerContextProvider: React.FC = ({ children }) => {
	const [isAuthenticated, setIsAuthenticated] = useState(false);
	const [isConnected, setIsConnected] = useState(false);
	const [isSynced, setSynced] = useState(false);
	const [isSyncing, setSyncing] = useState(false);
	const [userId, setUserId] = useState<number>(-1)

	useEffect(() => {
		const user_module_instance = UserModule.getInstance();
		user_module_instance.setAuthenticatedSetter(setIsAuthenticated);
		user_module_instance.setUserId(setUserId);

		const bridge_instance = ClientServerBridge.getInstance();
		bridge_instance.setConnectedSetter(setIsConnected);
	}, []);

	return (
		<ServerContext.Provider value={{isAuthenticated, userId, isConnected, isSynced, isSyncing, setSynced, setSyncing}}>
			{children}
		</ServerContext.Provider>
	);
};

export const useServerContext = () => {
	const context = useContext(ServerContext);
	if (!context) {
		throw new Error('useSocket must be used within a SocketProvider');
	}

	return context;
}
