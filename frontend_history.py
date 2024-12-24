    """
    This is to create an history conversation with some sidebar, and to show the conversation history in the sidebar.
    """

import streamlit as st
import time
import backend
import decisiontree as dt

# Can consider changing to React for frontend instead of Streamlit, but POC this is good.
def response_generator(prompt):
    response = backend.get_ai_recommendation(context=prompt)
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

st.title("CoPilot for CoPilot")
st.write("Welcome to CoPilot for CoPilot! Please breakdown your use case and we will recommend the best solution for each individual use cases.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "decision_tree_state" not in st.session_state:
    st.session_state.decision_tree_state = "choice"
if "decision_tree_context" not in st.session_state:
    st.session_state.decision_tree_context = "What do your client want to do? 1. Search and Q&A in document(s)\n2. Visualize text as a table or presentation\n3. Generate text in document(s)\n4. Extract data from document(s)\n5. Summarize content or analyze sentiment in document(s)\n6. Compare documents"
    st.session_state.decision_tree_choices = "1/2/3/4/5/6/none of the above"

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can we help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    print("Context ->"+st.session_state.decision_tree_context)
    print("Possible Outcome ->"+st.session_state.decision_tree_choices)
    print("Prompt ->"+prompt)
    ai_recommendation = backend.get_ai_recommendation(context=st.session_state.decision_tree_context,user_prompt=prompt,  choices=st.session_state.decision_tree_choices)


    dt.handle_decision_tree(ai_recommendation)

    with st.chat_message("assistant"):
        response = st.session_state.decision_tree_context
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})