import json
import sys
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevance
from langchain_ollama import ChatOllama
from agent.odds_agent import analyze_sports_market

eval_llm = ChatOllama(model="llama3.2", temperature=0.0)

def run_sports_eval():
    print("Running RAGAS Evaluation for Lone Star Showdown Agent...")
    
    with open("evals/golden_dataset.json", "r") as f:
        benchmark_data = json.load(f)
    
    questions, answers, contexts, ground_truths = [], [], [], []
    
    for item in benchmark_data:
        print(f"Testing market query: {item['question']}...")
        result = analyze_sports_market(item["question"])
        
        questions.append(result.target_event)
        answers.append(f"{result.fair_line_recommendation} - {result.risk_assessment}")
        contexts.append(result.retrieved_context)
        ground_truths.append([item["ground_truth"]])

    eval_dataset = Dataset.from_dict({
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    })
    
    print("\nComputing RAGAS Scores (Faithfulness & Answer Relevance)...")
    results = evaluate(
        dataset=eval_dataset,
        metrics=[faithfulness, answer_relevance],
        llm=eval_llm
    )
    
    print("\n================ RAGAS METRICS RESULTS ================")
    print(results)
    print("=======================================================\n")
    
    # CI/CD Quality Gate Threshold
    if results["faithfulness"] < 0.80 or results["answer_relevance"] < 0.80:
        print("QUALITY GATE FAILED: Risk of hallucinated odds or inaccurate stat lines!")
        sys.exit(1)
    
    print("QUALITY GATE PASSED: Model safe for production deployment.")
    sys.exit(0)

if __name__ == "__main__":
    run_sports_eval()