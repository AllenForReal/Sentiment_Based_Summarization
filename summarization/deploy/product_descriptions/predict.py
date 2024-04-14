import runpod
from transformers import BartForConditionalGeneration, AutoTokenizer
import torch

model_name = "saichandrapandraju/bart-summarization-amazon-product-info"

if torch.cuda.is_available():
    device = "cuda"
elif torch.backends.mps.is_available():
    device = "mps"
else:
    device = "cpu"

print(f"DEVICE - {device}")

model = BartForConditionalGeneration.from_pretrained(model_name).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_name)


def summarize_product_description(job):

    job_input = job["input"]
    text = job_input["text"].strip()

    if not isinstance(text, str):
        return {"error": "Input must be a string."}

    inputs = tokenizer([text], max_length=1024, return_tensors="pt").to(device)
    summary_ids = model.generate(inputs["input_ids"], max_length=512).detach().cpu()
    summary = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

    return summary


runpod.serverless.start({"handler": summarize_product_description})
