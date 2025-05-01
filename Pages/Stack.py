import streamlit as st
import graphviz

# Page Configuration
st.set_page_config(page_title="Stack Visualizer", layout="wide", page_icon="📚")
st.title("📚 Stack Operations Visualizer")

# Custom CSS for better styling
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    .stSelectbox>div>div>select {
        border-radius: 5px;
    }
    .section {
        padding: 15px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin-bottom: 20px;
    }
    .result-box {
        padding: 10px;
        border-radius: 5px;
        background-color: #e6f7ff;
        border-left: 4px solid #1890ff;
    }
    .stack-container {
        margin-top: 20px;
        padding: 15px;
        border-radius: 10px;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .steps-container {
        padding: 15px;
        background-color: #f9f9f9;
        border-radius: 8px;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'stack' not in st.session_state:
    st.session_state.stack = []
if 'eval_steps' not in st.session_state:
    st.session_state.eval_steps = []

# Stack visualization function
def visualize_stack(stack, title="Stack"):
    if not stack:
        st.info("Stack is empty")
        return
    
    dot = graphviz.Digraph()
    dot.attr(rankdir='TB', size='3,5', margin='0.1')
    
    # Add nodes (stack elements)
    for i, val in enumerate(reversed(stack)):
        dot.node(str(i), str(val), shape='box', style='filled', 
                fillcolor='#1890ff', fontcolor='white',
                width='0.8', height='0.5', fixedsize='true',
                fontsize='14')
    
    # Add invisible edges to enforce order
    for i in range(len(stack)-1):
        dot.edge(str(i), str(i+1), style='invis')
    
    st.graphviz_chart(dot, use_container_width=False)

# Polish Notation Functions
def infix_to_postfix(expression):
    precedence = {'+':1, '-':1, '*':2, '/':2, '^':3}
    stack = []
    postfix = []
    
    for char in expression:
        if char.isalnum():
            postfix.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
            stack.pop()  # Remove '(' from stack
        else:  # Operator
            while stack and stack[-1] != '(' and precedence.get(char, 0) <= precedence.get(stack[-1], 0):
                postfix.append(stack.pop())
            stack.append(char)
    
    while stack:
        postfix.append(stack.pop())
    
    return ' '.join(postfix)

def infix_to_prefix(expression):
    reversed_expr = expression[::-1].replace('(', 'temp').replace(')', '(').replace('temp', ')')
    postfix = infix_to_postfix(reversed_expr)
    prefix = postfix[::-1]
    return prefix

# Evaluation Functions
def evaluate_postfix_with_stack(expression):
    stack = []
    steps = []
    tokens = expression.split()
    
    if not tokens:
        raise ValueError("Empty expression")
    
    for token in tokens:
        if token.isdigit():
            stack.append(token)
            steps.append(f"Push {token}: Stack = {stack}")
        else:
            if len(stack) < 2:
                raise ValueError(f"Not enough operands for operator '{token}'")
            b = stack.pop()
            a = stack.pop()
            
            # Perform the operation
            if token == '+': res = str(float(a) + float(b))
            elif token == '-': res = str(float(a) - float(b))
            elif token == '*': res = str(float(a) * float(b))
            elif token == '/': res = str(float(a) / float(b))
            elif token == '^': res = str(float(a) ** float(b))
            else:
                raise ValueError(f"Unknown operator '{token}'")
            
            stack.append(res)
            steps.append(f"Apply {token} to {a} and {b}: Push {res}, Stack = {stack}")
    
    if len(stack) != 1:
        raise ValueError("Invalid expression - operands and operators don't match")
    
    st.session_state.eval_steps = steps
    return stack[0]

def evaluate_postfix_without_stack(expression):
    tokens = expression.split()
    steps = []
    
    if not tokens:
        raise ValueError("Empty expression")
    
    while len(tokens) > 1:
        for i in range(len(tokens)):
            if tokens[i] in '+-*/^':
                if i < 2:
                    raise ValueError("Not enough operands for operator")
                
                a = tokens[i-2]
                b = tokens[i-1]
                op = tokens[i]
                
                # Perform the operation
                if op == '+': res = str(float(a) + float(b))
                elif op == '-': res = str(float(a) - float(b))
                elif op == '*': res = str(float(a) * float(b))
                elif op == '/': res = str(float(a) / float(b))
                elif op == '^': res = str(float(a) ** float(b))
                else:
                    raise ValueError(f"Unknown operator '{op}'")
                
                steps.append(f"Apply {op} to {a} and {b}: Replace with {res}")
                tokens = tokens[:i-2] + [res] + tokens[i+1:]
                steps.append(f"Current expression: {' '.join(tokens)}")
                break
    
    st.session_state.eval_steps = steps
    return float(tokens[0])

def evaluate_prefix_with_stack(expression):
    stack = []
    steps = []
    tokens = expression.split()[::-1]  # Reverse for processing
    
    if not tokens:
        raise ValueError("Empty expression")
    
    for token in tokens:
        if token.isdigit():
            stack.append(token)
            steps.append(f"Push {token}: Stack = {stack}")
        else:
            if len(stack) < 2:
                raise ValueError(f"Not enough operands for operator '{token}'")
            a = stack.pop()
            b = stack.pop()
            
            # Perform the operation
            if token == '+': res = str(float(a) + float(b))
            elif token == '-': res = str(float(a) - float(b))
            elif token == '*': res = str(float(a) * float(b))
            elif token == '/': res = str(float(a) / float(b))
            elif token == '^': res = str(float(a) ** float(b))
            else:
                raise ValueError(f"Unknown operator '{token}'")
            
            stack.append(res)
            steps.append(f"Apply {token} to {a} and {b}: Push {res}, Stack = {stack}")
    
    if len(stack) != 1:
        raise ValueError("Invalid expression - operands and operators don't match")
    
    st.session_state.eval_steps = steps
    return stack[0]

# Main Content
operation_type = st.selectbox(
    "Select Operation Type",
    ["Basic Stack Operations", "Polish Notation Conversion", "Expression Evaluation"],
    index=0
)

if operation_type == "Basic Stack Operations":
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Stack Controls")
        with st.container():
            value = st.text_input("Enter value:")
            col1_1, col1_2 = st.columns(2)
            with col1_1:
                if st.button("Push", key="push"):
                    if value:
                        st.session_state.stack.append(value)
                        st.success(f"Pushed {value}")
                    else:
                        st.warning("Enter a value first")
            with col1_2:
                if st.button("Pop", key="pop"):
                    if st.session_state.stack:
                        popped = st.session_state.stack.pop()
                        st.success(f"Popped {popped}")
                    else:
                        st.warning("Stack is empty")
            
            if st.button("Clear Stack", type="primary"):
                st.session_state.stack = []
                st.success("Stack cleared")
    
    with col2:
        st.subheader("Stack Visualization")
        visualize_stack(st.session_state.stack)

elif operation_type == "Polish Notation Conversion":
    st.subheader("Notation Conversion")
    notation_option = st.radio(
        "Select conversion type:",
        ["Infix to Postfix", "Infix to Prefix"],
        horizontal=True
    )
    
    expression = st.text_input(f"Enter infix expression (e.g., A+B*C):")
    
    if st.button("Convert"):
        if expression:
            try:
                if notation_option == "Infix to Postfix":
                    result = infix_to_postfix(expression)
                else:
                    result = infix_to_prefix(expression)
                
                st.markdown(f"""
                <div class="result-box">
                    <strong>Result:</strong> {result}
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Conversion Error: {str(e)}")
        else:
            st.warning("Please enter an expression")

elif operation_type == "Expression Evaluation":
    st.subheader("Expression Evaluation")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        eval_option = st.radio(
            "Select evaluation type:",
            ["Postfix Evaluation", "Prefix Evaluation"],
            horizontal=False
        )
        
        method_option = st.radio(
            "Select evaluation method:",
            ["With Stack", "Without Stack"],
            horizontal=True
        )
        
        example = "3 4 2 * 1 5 - 2 3 ^ ^ / +" if eval_option == "Postfix Evaluation" else "+ / * 4 2 - 1 5 ^ 2 3"
        expression = st.text_input(f"Enter {eval_option.split()[0].lower()} expression (space separated):", 
                                 placeholder=f"e.g., {example}")
    
    with col2:
        if st.button("Evaluate"):
            if expression:
                try:
                    if eval_option == "Postfix Evaluation":
                        if method_option == "With Stack":
                            result = evaluate_postfix_with_stack(expression)
                        else:
                            result = evaluate_postfix_without_stack(expression)
                    else:
                        if method_option == "With Stack":
                            result = evaluate_prefix_with_stack(expression)
                        else:
                            st.warning("Prefix evaluation without stack is not implemented")
                            result = "N/A"
                    
                    st.markdown(f"""
                    <div class="result-box">
                        <strong>Result:</strong> {result}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show evaluation steps
                    if st.session_state.eval_steps:
                        with st.expander("Show Evaluation Steps"):
                            for step in st.session_state.eval_steps:
                                st.write(step)
                
                except Exception as e:
                    st.error(f"Evaluation Error: {str(e)}")
            else:
                st.warning("Please enter an expression")

# Information Section
st.markdown("---")
with st.expander("ℹ️ About This Tool"):
    st.markdown("""
    **Stack Operations Visualizer** provides interactive visualization of:
    - Basic stack operations (push/pop)
    - Notation conversions (infix to postfix/prefix)
    - Expression evaluation (postfix/prefix) with and without stack
    
    Features:
    - Clean, professional interface
    - Interactive stack visualization
    - Step-by-step evaluation explanations
    - Error handling for invalid inputs
    
    **Examples:**
    - Infix: A+B*C
    - Postfix: 3 4 2 * 1 5 - 2 3 ^ ^ / +
    - Prefix: + / * 4 2 - 1 5 ^ 2 3
    
    **Evaluation Methods:**
    - With Stack: Traditional stack-based evaluation
    - Without Stack: Alternative evaluation method (only for postfix)
    """)