# CriteriaEngine

## Objective
The CriteriaEngine application is designed to determine user eligibility based on various attributes such as age, department, income, and spending. It utilizes an Abstract Syntax Tree (AST) to represent conditional rules, allowing for dynamic creation, combination, and modification of these rules.

## Dependencies
To set up and run the application, ensure you have the following dependencies installed:

- Python 3.8 or higher
- FastAPI
- Uvicorn
- Pydantic
- Pytest
- Motor (for MongoDB)
- MongoDB (for data storage)

You can install the required Python packages using pip:

```bash
pip install fastapi uvicorn pydantic pytest motor
```

## Installation
1. **Clone the repository:**
   ```bash
   git clone git@github.com:NIKHIL0VERMA/CriteriaEngine.git
   cd CriteriaEngine/backend
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate 
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MongoDB:**
   Ensure you have MongoDB installed and running. You can use a local instance or a cloud-based solution like MongoDB Atlas.

5. **Run the application:**
   ```bash
   uvicorn backend.main:app --reload
   ```

6. **In new Terminal:**
    ```
    cd ../frontend
    npm install
    ```
7. **Run the NextJS frontend**
    ```
    npm run dev
    ```

## Data Structure
The primary data structure used to represent the AST is the `Node` class. Each node can represent either an operator (AND/OR) or an operand (conditions).

### Node Structure
```python
class Node:
    def __init__(self, type: str, operator: Optional[str] = None, value: Optional[Any] = None, 
                 left: Optional['Node'] = None, right: Optional['Node'] = None):
        self.type = type  # "operator" or "operand"
        self.operator = operator  # e.g., "AND", "OR", ">"
        self.value = value  # Optional value for operand nodes
        self.left = left  # Reference to left child
        self.right = right  # Reference to right child
```

## Data Storage
The application uses MongoDB for storing rules and application metadata. The schema for storing rules includes the following fields:

### Schema Example
```json
{
    "name": "Test Rule",
    "description": "A rule to test eligibility",
    "rule_string": "age > 30 AND department = 'Sales'",
    "ast": { /* AST representation */ },
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
}
```

## API Design
The API provides the following endpoints:

1. **Create Rule**
   - **Endpoint:** `POST /api/v1/create/`
   - **Description:** Takes a string representing a rule and returns a Node object representing the corresponding AST.

2. **Combine Rules**
   - **Endpoint:** `POST /api/v1/combine/`
   - **Description:** Takes a list of rule strings and combines them into a single AST, returning the root node of the combined AST.

3. **Evaluate Rule**
   - **Endpoint:** `POST /api/v1/evaluate/`
   - **Description:** Takes a JSON representing the combined rule's AST and a dictionary of attributes, evaluating the rule against the provided data.

### Sample Rules
- `rule1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"`
- `rule2 = "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"`

## Test Cases
1. Create individual rules from the examples using `create_rule` and verify their AST representation.
2. Combine the example rules using `combine_rules` and ensure the resulting AST reflects the combined logic.
3. Implement sample JSON data and test `evaluate_rule` for different scenarios.
4. Explore combining additional rules and test the functionality.

## Design Choices
- **AST Representation:** The AST is represented using a tree structure where each node can be an operator or an operand. This allows for flexible rule definitions and evaluations.
- **Database Choice:** MongoDB was chosen for its flexibility in handling JSON-like documents, making it suitable for storing rules and their metadata.
- **API Framework:** FastAPI was selected for its ease of use, performance, and automatic generation of OpenAPI documentation.

## Conclusion
This CriteriaEngine application provides a robust framework for defining, combining, and evaluating rules based on user attributes. The use of an AST allows for efficient rule management and evaluation, making it a powerful tool for eligibility determination.