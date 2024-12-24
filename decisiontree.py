import streamlit as st

solution_copilot = "Recommendation: Copilot license / Amazon Q for Business, please connect your supervisor for futher details."

solution_custom_genai_solution = "Recommendation: Custom GenAI Solution, please contact BA8000's sales team for support."

solution_customized_copilot = "Recommendation: Customized Copilot / Amazon Q, please contact BA6000 team for support."

solution_ask_your_document = "Recommendation: Ask Your Document Solution Accelerator, please contact BA8000's Sales team for support."


def handle_decision_tree(user_input):
    context = st.session_state.decision_tree_context
    if st.session_state.decision_tree_state == "choice":
        if user_input == "1":
            st.session_state.decision_tree_context = "Do you want to search within many documents? (yes/no)"
            st.session_state.decision_tree_choices = "yes/no"
            st.session_state.decision_tree_state = "many_docs"
        elif user_input == "2":
            st.session_state.decision_tree_context = solution_copilot
            st.session_state.decision_tree_state = "end"
        elif user_input == "3":
            st.session_state.decision_tree_context = "Do your users want to generate 1 page at a time? (yes/no)"
            st.session_state.decision_tree_choices = "yes/no"
            st.session_state.decision_tree_state = "one_doc"
        elif user_input == "4":
            st.session_state.decision_tree_context = "Do you want to automatically extract data from multiple pages ? (yes/no)"
            st.session_state.decision_tree_choices = "yes/no"
            st.session_state.decision_tree_state = "auto_extract"
        elif user_input == "5":
            st.session_state.decision_tree_context = solution_custom_genai_solution
            st.session_state.decision_tree_state = "end"
        elif user_input == "6":
            st.session_state.decision_tree_context = "Do you want to compare documents at scale? (yes/no)"
            st.session_state.decision_tree_choices = "yes/no"
            st.session_state.decision_tree_state = "compare_docs"
        else:
            st.session_state.decision_tree_context = "Invalid choice. Please restart and try again."
            st.session_state.decision_tree_state = "end"
    elif st.session_state.decision_tree_state == "many_docs":
        if user_input.lower() == "yes":
            st.session_state.decision_tree_context = "Where are the documents stored? (sharepoint/others)"
            st.session_state.decision_tree_choices = "sharepoint/others"
            st.session_state.decision_tree_state = "storage"
        else:
            st.session_state.decision_tree_context = solution_copilot
            st.session_state.decision_tree_state = "end"
    elif st.session_state.decision_tree_state == "storage":
        if user_input.lower() == "sharepoint":
            st.session_state.decision_tree_context = solution_copilot
            st.session_state.decision_tree_state = "end"
        else:
            st.session_state.decision_tree_context = "Do you need to prioritize searches or persist search results? (yes/no)"
            st.session_state.decision_tree_choices = "yes/no"
            st.session_state.decision_tree_state = "persist_results"
    elif st.session_state.decision_tree_state == "persist_results":
        if user_input.lower() == "yes":
            st.session_state.decision_tree_context = solution_custom_genai_solution
            st.session_state.decision_tree_state = "end"
        else:
            st.session_state.decision_tree_context = solution_ask_your_document
            st.session_state.decision_tree_state = "end"
    elif st.session_state.decision_tree_state == "one_doc":
        if user_input.lower() == "yes":
            st.session_state.decision_tree_context = solution_copilot
            st.session_state.decision_tree_state = "end"
        else:
            st.session_state.decision_tree_context = solution_custom_genai_solution
            st.session_state.decision_tree_state = "end"
            # st.session_state.decision_tree_context = "Must the output adhere to specific policies, standards, or include content moderation? (yes/no)"
            # st.session_state.decision_tree_choices = "yes/no"
            # st.session_state.decision_tree_state = "standards"
    # elif st.session_state.decision_tree_state == "standards":
    #     if user_input.lower() == "yes":
    #         st.session_state.decision_tree_context = solution_custom_genai_solution
    #         st.session_state.decision_tree_state = "end"
    #     else:
    #         st.session_state.decision_tree_context = solution_copilot
    #         st.session_state.decision_tree_state = "end"
    elif st.session_state.decision_tree_state == "auto_extract":
        if user_input.lower() == "yes":
            st.session_state.decision_tree_context = solution_customized_copilot
            st.session_state.decision_tree_state = "end"
        else:
            st.session_state.decision_tree_context = "Are the documents residing or generated in M365 or SharePoint? (yes/no)"
            st.session_state.decision_tree_choices = "yes/no"
            st.session_state.decision_tree_state = "ms_word"
    elif st.session_state.decision_tree_state == "ms_word":
        if user_input.lower() == "yes":
            st.session_state.decision_tree_context = "Do you want to store the output of the extraction automatically? (yes/no)"
            st.session_state.decision_tree_choices = "yes/no"
            st.session_state.decision_tree_state = "store_output"
        else:
            st.session_state.decision_tree_context = solution_copilot
            st.session_state.decision_tree_state = "end"
    elif st.session_state.decision_tree_state == "store_output":
        if user_input.lower() == "yes":
            st.session_state.decision_tree_context = solution_copilot
            st.session_state.decision_tree_state = "end"
        else:
            st.session_state.decision_tree_context = solution_custom_genai_solution
            st.session_state.decision_tree_state = "end"
    elif st.session_state.decision_tree_state == "compare_docs":
        if user_input.lower() == "yes":
            st.session_state.decision_tree_context = solution_custom_genai_solution
            st.session_state.decision_tree_state = "end"
        else:
            st.session_state.decision_tree_context = "Does the outcome of the comparison need to be persisted? (yes/no)"
            st.session_state.decision_tree_choices = "yes/no"
            st.session_state.decision_tree_state = "persist_comparison"
    elif st.session_state.decision_tree_state == "persist_comparison":
        if user_input.lower() == "yes":
            st.session_state.decision_tree_context = solution_custom_genai_solution
            st.session_state.decision_tree_state = "end"
        else:
            st.session_state.decision_tree_context = solution_copilot
            st.session_state.decision_tree_state = "end"
    else:
        st.session_state.decision_tree_context = "Invalid choice. Please restart and try again."
        st.session_state.decision_tree_state = "end"