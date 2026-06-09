from langchain_core.prompts import ChatPromptTemplate

QUERY_REWRITER_PROMPT = ChatPromptTemplate.from_template("""
You are a search query optimizer.

Rewrite the user's question into a concise search query
that will retrieve the most relevant documents.
and identify user asking about which company(among Emirates,Air India,Spicejet,Gofirst).
Do not guess the company if it is not explicitly mentioned in the question. If you cannot identify any company, return the original question as the rewritten query.
            
If there are random question then give as it is.  
                                                                  
User Question:
{question}

Rewritten Query:
""")