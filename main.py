import streamlit as st
import yaml
import os
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document as LangchainDoc
from langchain.prompts import PromptTemplate
import tempfile
import shutil

# Load API Key
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

if not openai_key:
    st.error("⚠️ OpenAI API key not found! Please set OPENAI_API_KEY in your .env file")
    st.stop()

@st.cache_data
def load_yaml_as_text(path):
    """Load YAML data and convert to structured text"""
    try:
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        
        def format_section(key, value, indent=0):
            text = ""
            spacing = "  " * indent
            
            if isinstance(value, dict):
                text += f"{spacing}{key.title()}:\n"
                for k, v in value.items():
                    text += format_section(k, v, indent + 1)
            elif isinstance(value, list):
                text += f"{spacing}{key.title()}:\n"
                for item in value:
                    if isinstance(item, dict):
                        for k, v in item.items():
                            text += f"{spacing}  • {k}: {v}\n"
                    else:
                        text += f"{spacing}  • {item}\n"
            else:
                text += f"{spacing}{key.title()}: {value}\n"
            
            return text
        
        formatted_text = ""
        for key, value in data.items():
            formatted_text += format_section(key, value) + "\n"
        
        return formatted_text
    except Exception as e:
        st.error(f"Error loading YAML file: {e}")
        return ""

@st.cache_resource
def setup_qa_system():
    """Initialize the QA system with caching"""
    # Load and prepare documents
    text_data = load_yaml_as_text("data/sehaj_profile.yaml")
    if not text_data:
        return None
    
    docs = [LangchainDoc(page_content=text_data)]
    
    # Split text into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " "]
    )
    split_docs = splitter.split_documents(docs)
    
    # Create vector store with temporary directory
    temp_dir = tempfile.mkdtemp()
    embedder = OpenAIEmbeddings(openai_api_key=openai_key)
    vectorstore = Chroma.from_documents(
        split_docs, 
        embedder,
        persist_directory=temp_dir
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    # Custom prompt template
    template = """You are Sehaj Malhotra's personal AI assistant. Use the following information about Sehaj to answer questions accurately and helpfully.

Context: {context}

Question: {question}

Answer as if you are representing Sehaj professionally but in a friendly, conversational tone. If the question is about something not covered in the context, politely say that information isn't available in your knowledge base about Sehaj.

Answer:"""
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )
    
    # LLM and QA Chain
    llm = OpenAI(
        openai_api_key=openai_key, 
        temperature=0.3,
        max_tokens=500
    )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )
    
    return qa_chain

# Streamlit UI Configuration
st.set_page_config(
    page_title="Ask Sehaj Anything",
    page_icon="🤖",
    layout="wide"
)

# Header
st.title("🤖 Ask Sehaj Anything")
st.markdown("*Your personal AI assistant to learn about Sehaj Malhotra's background, skills, and experience*")

# Initialize QA system
qa_chain = setup_qa_system()

if not qa_chain:
    st.error("Failed to initialize the QA system. Please check your data file.")
    st.stop()

# Sidebar with example questions
with st.sidebar:
    st.header("💡 Example Questions")
    example_questions = [
        "What is Sehaj's educational background?",
        "What programming languages does Sehaj know?",
        "Tell me about Sehaj's work experience",
        "What are Sehaj's interests outside of work?",
        "What tools and technologies is Sehaj familiar with?",
        "Where did Sehaj complete their Master's degree?"
    ]
    
    for question in example_questions:
        if st.button(question, key=f"btn_{question[:20]}"):
            st.session_state.example_query = question

# Main chat interface
col1, col2 = st.columns([3, 1])

with col1:
    # Use example query if one was clicked
    default_query = st.session_state.get('example_query', '')
    query = st.text_input(
        "Ask me about Sehaj's background, skills, experience, or interests:",
        value=default_query,
        placeholder="e.g., What is Sehaj's educational background?"
    )
    
    # Clear the example query after using it
    if 'example_query' in st.session_state:
        del st.session_state.example_query

with col2:
    ask_button = st.button("Ask", type="primary", use_container_width=True)

# Process query
if (query and ask_button) or (query and st.session_state.get('auto_submit', False)):
    with st.spinner("🤔 Thinking..."):
        try:
            result = qa_chain({"query": query})
            
            # Display response
            st.markdown("### 💬 Response:")
            st.markdown(result['result'])
            
            # Show confidence/source info
            with st.expander("📚 Source Information", expanded=False):
                if result.get('source_documents'):
                    st.write("Response based on:")
                    for i, doc in enumerate(result['source_documents']):
                        st.write(f"**Source {i+1}:**")
                        st.text(doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content)
                        st.write("---")
                else:
                    st.write("No specific source documents found.")
            
        except Exception as e:
            st.error(f"Sorry, I encountered an error: {str(e)}")
            st.write("Please try rephrasing your question or check your OpenAI API key.")

# Footer
st.markdown("---")
st.markdown("*Built with Streamlit, LangChain, and OpenAI • [View Profile Data](data/sehaj_profile.yaml)*")

# Display raw profile data in expander
with st.expander("📄 View Raw Profile Data", expanded=False):
    try:
        with open("data/sehaj_profile.yaml", 'r') as f:
            profile_content = f.read()
        st.code(profile_content, language='yaml')
    except FileNotFoundError:
        st.error("Profile data file not found!")