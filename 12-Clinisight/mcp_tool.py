from mcp.server.fastmcp import FastMCP 
from functions.symptom_extractor import extract_symptoms
from functions.diagnosis_symptoms import get_diagnosis
from functions.pubmed_articles import fetch_pubmed_articles_with_metadata
from functions.summerize_pubmed import summarize_text

mcp = FastMCP("Clinisight AI")


@mcp.tool()
async def clinisight_ai(symptom_text):
    symptom = extract_symptoms(symptom_text)
    diagnosis_result = get_diagnosis(symptom)
    pubmed_article = fetch_pubmed_articles_with_metadata(" ".join(symptom))
    summary = summarize_text(pubmed_article[:3000])

    return {
        "symptom":symptom,
        "diagnosis":diagnosis_result,
        "pubmed_summary" :summary
    }





if __name__ == "__main__":
    mcp.run(transport = "stdio")