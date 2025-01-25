
import torch
from transformers import pipeline
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes
from telegram.ext.filters import TEXT

API_TOKEN = 'Enter your API token here'
print("Loading TinyLlama model...")
pipe = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    torch_dtype=torch.float32,
)
def generate_pirate_response(user_message: str) -> str:
    messages = [
        {"role": "user", "content": user_message},
    ]
    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipe(prompt, max_new_tokens=200, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    generated_text = outputs[0]["generated_text"]
    print(generated_text)
    # Remove the system/user tokens and <|assistant|> for clean output
    response = generated_text.split("</s>")[-1].replace("<|assistant|>", "").strip()
    return response

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I am your AI Assistant. How can I help you today?")

async def process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    try:
        static_message = "Received your message: \"{}\"".format(user_message)
        await update.message.reply_text(static_message)
        
        pirate_response = generate_pirate_response(user_message)
        await update.message.reply_text(pirate_response)
    except Exception as e:
        await update.message.reply_text("Arrr, there be an issue! Try again later!")

def main():
    app = ApplicationBuilder().token(API_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(TEXT, process))
    print("Bot is running.")
    app.run_polling()

if __name__ == "__main__":
    main()
