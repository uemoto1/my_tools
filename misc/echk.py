import litellm
import asyncio
import difflib
from prompt_toolkit import prompt
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText

MODEL, API_BASE = "ollama/gemma3:latest", "http://localhost:11434"

PROMPT = """以下の英文を、校閲・修正してください。
修正点はメモとして含めないで、必ず修正後の英文のみを返してください。 
理工系学術雑誌に掲載する英文原稿として適切なよう、文法、スペル、句読点のミスを修正し、
より自然で読みやすい表現になるように調整してください。"""

async def chat(msg, verbose=True):
    response = await litellm.acompletion(
        model=MODEL,
        api_base=API_BASE,
        messages=msg,
        stream=True
    )
    buf = []
    async for chunk in response:
        tmp = chunk['choices'][0]['delta'].content
        if tmp:
            print(tmp, end="", flush=True)
            buf.append(tmp)
    print("")
    return "".join(buf)

def show_diff(original, modidied):
    for item in difflib.ndiff(original.split(), modidied.split()):
        if item[0] == "+":
            print_formatted_text(FormattedText([("blue",item[1:] )]), end="")
        elif item[0] == "-":
            print_formatted_text(FormattedText([("red",item[1:] )]), end="")
        elif item[0] == "?":
            pass
        else:
            print_formatted_text(FormattedText([("",item[1:] )]), end="")
    print("")


while True:
    text = prompt(">>> ")
    if not text.strip():
        continue
    msg = [
        {"role": "system", "content": PROMPT},
        {"role": "user", "content": text},
    ]
    result = asyncio.run(chat(msg))
    print("-"*16)
    show_diff(text, result)
    print("-"*16)
