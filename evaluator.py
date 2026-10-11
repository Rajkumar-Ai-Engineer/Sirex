"""Run a LangSmith evaluation of a Groq-backed Q&A target on the Sirex dataset.

Env (.env): LANGSMITH_API_KEY, DATASET_NAME, GROQ_API_KEY

Usage:
    python evaluator.py --limit 5      # quick smoke test on 5 examples
    python evaluator.py                # full dataset
"""

import argparse
import os
import re
import string

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langsmith import Client, evaluate, traceable
from pydantic import BaseModel, Field

load_dotenv()

DATASET_NAME = os.environ["DATASET_NAME"]
DEFAULT_MODEL = "openai/gpt-oss-120b"

SYSTEM_PROMPT = (
    "You are a trivia expert. Answer the question with only the answer itself "
    "(a word or short phrase). No explanation, no punctuation, no full sentence."
)


# The dataset's reference key is misspelled "Ouptut"; accept the correct spelling too.
def _reference(reference_outputs: dict) -> str:
    return str(reference_outputs.get("Output", reference_outputs.get("Ouptut", "")))


def _normalize(text: str) -> str:
    text = text.lower().translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\b(a|an|the)\b", " ", text)
    return " ".join(text.split())


def make_target(model: str):
    llm = ChatGroq(model=model, temperature=0)

    @traceable(name="sirex_qa")
    def target(inputs: dict) -> dict:
        msg = llm.invoke(
            [("system", SYSTEM_PROMPT), ("user", inputs["Input"])]
        )
        return {"Output": msg.content.strip()}

    return target


# ---- evaluators: (inputs, outputs, reference_outputs) -> {"key", "score", ...} ----
def exact_match(outputs: dict, reference_outputs: dict) -> dict:
    ok = _normalize(outputs["Output"]) == _normalize(_reference(reference_outputs))
    return {"key": "exact_match", "score": int(ok)}


def contains_reference(outputs: dict, reference_outputs: dict) -> dict:
    ref = _normalize(_reference(reference_outputs))
    ok = bool(ref) and ref in _normalize(outputs["Output"])
    return {"key": "contains_reference", "score": int(ok)}


class Verdict(BaseModel):
    correct: bool = Field(description="True if the answer is semantically the same as the reference")
    reasoning: str = Field(description="One short sentence")


def make_llm_judge(judge_model: str):
    judge = ChatGroq(model=judge_model, temperature=0).with_structured_output(Verdict)

    def correctness(inputs: dict, outputs: dict, reference_outputs: dict) -> dict:
        v = judge.invoke(
            f"Question: {inputs['Input']}\n"
            f"Reference answer: {_reference(reference_outputs)}\n"
            f"Model answer: {outputs['Output']}\n\n"
            "Is the model answer correct (same meaning as the reference, ignoring "
            "casing, spelling variants and extra wording)?"
        )
        return {"key": "correctness", "score": int(v.correct), "comment": v.reasoning}

    return correctness


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=None, help="only evaluate N examples")
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--judge-model", default=DEFAULT_MODEL)
    p.add_argument("--concurrency", type=int, default=2)
    args = p.parse_args()

    client = Client()
    data = (
        client.list_examples(dataset_name=DATASET_NAME, limit=args.limit)
        if args.limit
        else DATASET_NAME
    )

    results = evaluate(
        make_target(args.model),
        data=data,
        evaluators=[exact_match, contains_reference, make_llm_judge(args.judge_model)],
        experiment_prefix=f"sirex-{args.model}",
        description="Sirex Q&A baseline",
        max_concurrency=args.concurrency,
        client=client,
        metadata={"model": args.model, "judge_model": args.judge_model},
    )

    df = results.to_pandas()
    score_cols = [c for c in df.columns if c.startswith("feedback.")]
    print(f"\nExamples evaluated: {len(df)}")
    print(df[score_cols].mean().round(3).to_string())


if __name__ == "__main__":
    main()
