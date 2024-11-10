from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import language_tool_python
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"


def summary_maker(text):
    tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
    model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6")

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    summary_ids = model.generate(inputs["input_ids"])
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    tool = language_tool_python.LanguageTool('en-US')
    corrected_text = tool.correct(summary)
    return corrected_text
