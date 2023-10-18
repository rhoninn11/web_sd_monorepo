import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import './index.css';

import '@blueprintjs/core/lib/css/blueprint.css';
import '@blueprintjs/datetime/lib/css/blueprint-datetime.css';
import '@blueprintjs/icons/lib/css/blueprint-icons.css';
import '@blueprintjs/select/lib/css/blueprint-select.css';
import '@blueprintjs/table/lib/css/table.css';
import { init_processors } from './logic/request_processing/00_init';
import { ClientServerBridge } from './logic/ClientServerBridge';

init_processors();
ClientServerBridge.getInstance();
console.log('+++ ClientServerBridge.getInstance()');

ReactDOM.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>,
    document.getElementById('root') as HTMLElement,
);


