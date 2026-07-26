import re

class QueryParser:
    @staticmethod
    def parse_price_intent(query: str) -> dict:
        """
        Rule-based NLP parser to extract commercial intent, pricing constraints, 
        and promotional expectations from unstructured user queries.
        
        Returns a structured feature payload for downstream recommendation engines.
        """
        # Text Standardization: Lowercase conversion for case-insensitive feature matching
        query = query.lower()
        
        # 1. Promotional Intent Extraction: Isolate explicit discount entities using Regex
        # Captures promotional sensitivity to drive marketing/sales logic
        discount_match = re.search(r'diskon\s*(\d+)', query)
        discount_val = int(discount_match.group(1)) if discount_match else 0
        
        # 2. Lexical Normalization: Map colloquial Indonesian monetary terms to raw quantitative formats
        # Cleansing unstructured text to prevent parsing fragmentation
        query_cleaned = query.replace("ribu", "000").replace("rb", "000")
        query_cleaned = query_cleaned.replace("juta", "000000").replace("jt", "000000")
        query_cleaned = query_cleaned.replace(".", "").replace(",", "")
        
        # 3. Purchasing Power Extraction: Identify numerical entities representing budget constraints
        numbers = re.findall(r'\d+', query_cleaned)
        
        # Heuristic assignment: Assume the first extracted numerical entity represents the budget ceiling
        budget_val = int(numbers[0]) if numbers else 0
        
        # 4. Feature Payload Construction: Route business logic based on extracted constraints
        # Determines if the retrieval system should prioritize discounted items or standard budget limits
        return {
            "operator": "discount" if discount_val > 0 else "lte", # Relational operator for SQL/NoSQL querying
            "budget": budget_val,                                  # Upper-bound price constraint
            "discount": discount_val                               # Promotional target percentage
        }
