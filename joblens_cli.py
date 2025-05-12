#!/usr/bin/env python

import argparse
import os
import sys

from dotenv import load_dotenv
import openai

# ————————————————
# Load .env and API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    sys.exit("❌ ERROR: OPENAI_API_KEY not found. Please set it in your .env file or environment variables.")

# ————————————————
# Automatically pick the best available model
try:
    available_models = [m.id for m in openai.Model.list().data]
except Exception as e:
    sys.exit(f"❌ Could not retrieve model list. Check your API key.\n{e}")

for candidate in ("gpt-4", "gpt-3.5-turbo"):
    if candidate in available_models:
        chosen_model = candidate
        break
else:
    sys.exit("❌ No supported models available (gpt-4 or gpt-3.5-turbo).")

# ————————————————
# Core functions
def load_file(path: str) -> str:
    """Read and return the contents of a UTF-8 text file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        sys.exit(f"❌ ERROR reading '{path}': {e}")

def rewrite_resume(job_desc: str, resume: str, model: str) -> str:
    """Call the OpenAI API with the given model and prompt."""
    prompt = (
        "You are a career coach. Rewrite the resume below to match this job description, "
        "optimizing for ATS and personalization.\n\n"
        f"Job Description:\n{job_desc}\n\n"
        f"Resume:\n{resume}\n\n"
        "Output only the rewritten resume."
    )
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1600
        )
        return response.choices[0].message.content.strip()
    except openai.error.InvalidRequestError:
        sys.exit(f"❌ The model '{model}' is not available for your key.")
    except Exception as e:
        sys.exit(f"❌ API error: {e}")

# ————————————————
# CLI entrypoint
def main():
    parser = argparse.ArgumentParser(
        prog="joblens-cli",
        description="GPT-powered CLI to rewrite resumes to match job descriptions"
    )
    parser.add_argument("resume_path", help="Path to the resume text file")
    parser.add_argument("job_desc_path", help="Path to the job description text file")
    parser.add_argument(
        "-o", "--output",
        help="Output file (default: rewritten_resume.txt)",
        default="rewritten_resume.txt"
    )
    args = parser.parse_args()

    resume = load_file(args.resume_path)
    job_desc = load_file(args.job_desc_path)
    rewritten = rewrite_resume(job_desc, resume, model=chosen_model)

    try:
        with open(args.output, "w", encoding="utf-8") as out_f:
            out_f.write(rewritten)
        print(f"✅ Rewritten resume saved to {args.output}")
    except Exception as e:
        sys.exit(f"❌ ERROR writing output file: {e}")

if __name__ == "__main__":
    main()
