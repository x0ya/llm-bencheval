import re
from concurrent.futures import ThreadPoolExecutor, as_completed

from models import MODELS, ask_model, OutOfCreditError
from search import search_web, build_prompt


def cited_numbers(text, how_many):
    # finds [1], [2][5] and [1, 2, 3] style citations
    found = set()
    for group in re.findall(r"\[(\d+(?:\s*,\s*\d+)*)\]", text):
        for part in group.split(","):
            n = int(part.strip())
            if 1 <= n <= how_many:
                found.add(n)
    return sorted(found)


def run_one(label, prompt):
    try:
        return label, ask_model(label, prompt, max_tokens=500), None
    except OutOfCreditError:
        return label, None, "OUT OF CREDIT"
    except Exception as e:
        return label, None, str(e)[:150]


def main():
    while True:
        question = input("\nQuestion (or 'quit'): ").strip()
        if question.lower() in ("quit", "exit", ""):
            break

        print("Searching the web...")
        try:
            sources = search_web(question)
        except Exception as e:
            print("Search failed, asking without sources:", str(e)[:100])
            sources = []
        prompt = build_prompt(question, sources)

        print("Asking all models...\n")
        with ThreadPoolExecutor(max_workers=len(MODELS)) as pool:
            futures = [pool.submit(run_one, label, prompt) for label in MODELS]
            for f in as_completed(futures):
                label, result, error = f.result()
                print("=" * 60)
                if error:
                    print(label.upper(), "-> ERROR:", error)
                    continue

                print(label.upper(), "(" + str(result["seconds"]) + "s,",
                      result["tokens"], "tokens)")
                print(result["text"])

                used = cited_numbers(result["text"], len(sources))
                print("\nSources cited by " + label + ":")
                if not used:
                    print("  (none cited)")
                for n in used:
                    s = sources[n - 1]
                    print("  [" + str(n) + "]", s["title"])
                    print("      " + s["url"])

        print("\n" + "=" * 60)
        print("ALL SOURCES RETRIEVED")
        for i, s in enumerate(sources, 1):
            print("[" + str(i) + "]", s["title"])
            print("    " + s["url"])


main()
