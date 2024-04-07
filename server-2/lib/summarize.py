from transformers import pipeline

def summarize_email(str):
    summarizer = pipeline('summarization', model="sshleifer/distilbart-cnn-6-6")
    summary = summarizer(str, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']