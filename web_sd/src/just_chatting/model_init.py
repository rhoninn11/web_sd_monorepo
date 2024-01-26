import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer
from transformers import BitsAndBytesConfig


def llm_init():
    
    models = {
        "notus": { "name": "argilla/notus-7b-v1", "type": "dpo", "comment": "sometimes omits important information of systytm" },
        "solar": { "name": "upstage/SOLAR-10.7B-Instruct-v1.0", "type": "sft", "comment": "totally ignore system" },
        "starling": { "name": "berkeley-nest/Starling-LM-7B-alpha", "type": "dpo", "comment": "hmm" },
        "zephyr": { "name": "HuggingFaceH4/zephyr-7b-beta", "type": "dpo", "comment": "not follow system i think" },
        "neurocoro": { "name": "mlabonne/NeuralMarcoro14-7B", "type": "dpo?", "comment": "not tested a lot" },
        "dolphin": { "name": "cognitivecomputations/dolphin-2.6-mistral-7b", "type": "dpo", "comment": "not tested a lot" },
        "daredevil": { "name": "mlabonne/NeuralDaredevil-7B", "type": "dpo" , "comment": "not tested a lot" },
    }
    id_select = "notus"
    model_id = models[id_select]["name"]
    type_select = models[id_select]["type"]

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    streamer = TextStreamer(tokenizer)
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )

    model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=bnb_config)

    return model, tokenizer, streamer, type_select