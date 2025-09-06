import asyncio
from googletrans import Translator

# Input file (one English word per line)
input_file = "wordlist.txt"
# Output file (Chinese translation + English word)
output_file = "wordlist-zh.txt"

async def translate_word(translator, word):
    """Asynchronously translates a single word and handles errors."""
    try:
        # The `translate` method needs to be awaited
        translation_obj = await translator.translate(word, src="en", dest="zh-cn")
        translated_text = translation_obj.text
        
        print(f"Translated: {word} -> {translated_text}")
        return f"{translated_text} {word}"
    except Exception as e:
        print(f"Could not translate '{word}'. Error: {e}")
        return f"(Translation failed) {word}"

async def main():
    """The main asynchronous routine."""
    translator = Translator()
    
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            words = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: The input file '{input_file}' was not found.")
        # Create a dummy file for demonstration purposes
        with open(input_file, "w", encoding="utf-8") as f:
            f.write("hello\nworld\npython")
        print(f"A sample '{input_file}' has been created. Please run the script again.")
        return

    # Create a list of translation tasks (coroutines)
    tasks = [translate_word(translator, word) for word in words]
    
    # Run all tasks concurrently and wait for them to complete
    results = await asyncio.gather(*tasks)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(results))

    print(f"\nTranslation complete. Results saved to {output_file}")


if __name__ == "__main__":
    # This command starts the asyncio event loop and runs the main() coroutine
    asyncio.run(main())