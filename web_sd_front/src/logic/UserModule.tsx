

import { ProcessorRepository } from './request_processing/RequestProcessor';
import { serverRequest, authData } from 'web_sd_shared_types/02_serv_t';
import { v4 as uuid } from 'uuid';

export class UserModule {

	private static instance: UserModule;

	private req_proc: ProcessorRepository;

	private auth_try_num: number = 4;
	private auth: boolean = false;
	private user_id: number = -1;
	private password: string = '';
	private allow_to_login: boolean = true;

	private constructor() {
		this.req_proc = ProcessorRepository.getInstance();
	}

	public static getInstance(): UserModule {
		if (!UserModule.instance) {
			UserModule.instance = new UserModule();
		}

		return UserModule.instance;
	}

	public setPasswd(passwd: string) {
		this.password = passwd;
	}

	getRandomInt(max: number) {
		return Math.floor(Math.random() * max);
	}

	private _pass_gen() {
		// random int from 48 to 55
		let int_value = this.getRandomInt(2) + 50;
		let password = 'pulsary' + int_value + '.';

		if (this.password.length > 0){
			password = this.password;
		}
		console.log("generated password: ", password)
		return password
	}

	// internals
	public askForAuth() {
		if (!this.allow_to_login)
			return;
		this.allow_to_login = false;

		let auth = new authData();
		auth.password = this._pass_gen()


		let on_finish = (authData: authData) => {
			this._setIsAuthenticated(authData.auth);
			this._setUSerId(authData.user_id);

			if (!authData.auth && this.auth_try_num > 0) {
				setTimeout(() => this.allow_to_login = true, 1000);
				this.auth_try_num--;
			}
		}

		let unique_id = uuid()
		this.req_proc.get_processor('auth')
			?.bind_fn(on_finish, unique_id)
			.to_server(auth, unique_id)
	}

	// to communicate with react
	public isAuthenticated = () => {
		return this.auth;
	};

	public getUserId = () => {
		return this.user_id;
	}

	private isAuthenticatedSetter: (suth: boolean) => void = () => { };
	private userIdSetter: (suth: number) => void = () => { };

	public setAuthenticatedSetter = (setter: (suth: boolean) => void) => {
		this.isAuthenticatedSetter = setter;
		this.isAuthenticatedSetter(this.auth);
	}

	public setUserId = (setter: (suth: number) => void) => {
		this.userIdSetter = setter;
	}

	private _setIsAuthenticated = (isAuthenticated: boolean) => {
		this.auth = isAuthenticated;
		this.isAuthenticatedSetter(isAuthenticated);
	}

	private _setUSerId = (user_id: number) => {
		this.user_id = user_id;
		this.userIdSetter(user_id);
	}

}

