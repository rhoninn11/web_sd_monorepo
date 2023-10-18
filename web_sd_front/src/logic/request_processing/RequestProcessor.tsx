import { serverRequest } from "web_sd_shared_types/02_serv_t";
import { ClientServerBridge } from "../ClientServerBridge";
import { v4 as uuid } from 'uuid';


export type FinishCB<T> = (data: T) => void;

export class RequestProcessor<T> {
    protected type: string = '';
    protected on_finish_dict: { [key: string]: FinishCB<T>} = {};

    public show_type() {
        console.log('+++ show_type', this.type);
    }

    public match_type(type: string): boolean {
        return this.type === type;
    }

    public bind_fn(on_finish: FinishCB<T>, id?: string) {
        let uniq_id = id ? id : uuid();
        this.on_finish_dict[uniq_id] = on_finish;

        return this;
    }

    public unbind_fn(id: string) {
        if (id in this.on_finish_dict)
            delete this.on_finish_dict[id];
    }

    public execute_fn(id: string, data: T) {
        // console.log('+++ execute_fn', id);
        if (id in this.on_finish_dict) {
            let on_finish = this.on_finish_dict[id];
            on_finish(data);
        }
    }

    public to_server(input: T, id?: string) {
    }

    public from_server(req: serverRequest) {
    }

    public input_to_server(input: T, id?: string) {
        let uniq_id = id ? id : uuid();

        let serv_req: serverRequest = {
            id: uniq_id,
            data: JSON.stringify(input),
            type: this.type,

        }

        ClientServerBridge.getInstance()
            .sendRequest(serv_req);
    }
}

export class ProcessorRepository {
    protected processors: RequestProcessor<any>[] = [];
    private static instance: ProcessorRepository;

    private constructor() {
    }

    public register_processor(processor: RequestProcessor<any>) {
        this.processors.push(processor);
        processor.show_type();
        return this;
    }
    public static getInstance(): ProcessorRepository {
        if (!ProcessorRepository.instance) {
            ProcessorRepository.instance = new ProcessorRepository();
        }

        return ProcessorRepository.instance;
    }

    public get_processor(type: string): RequestProcessor<any> | undefined {
        let processor = this.processors.find(processor => processor.match_type(type));
        // console.log('+++ get_processor', processor);
        return processor
    }
}

