import { OverlayToaster, Position } from "@blueprintjs/core";


export const SyncInfoToster = OverlayToaster.create({
	className: "recipe-toaster",
	position: Position.TOP,
});

export class TosterHOme {

	private static instance: TosterHOme;

    constructor() {
        
    }

	public static getInstance(): TosterHOme {
		if (!TosterHOme.instance) {
			TosterHOme.instance = new TosterHOme();
		}

		return TosterHOme.instance;
	}
}

