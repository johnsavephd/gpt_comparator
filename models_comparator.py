import streamlit as st
import os
import openai

st.set_page_config(layout="wide")

with st.sidebar:
    
    st.header(" GPT Parameters Set-up")
    st.markdown("Please, fulfill the following fields to compare GPTs' results and costs and choose the right models.")
    #api_key = st.text_input(label = ":key: **OpenAI API Key**", value="", placeholder= "Insert here your API Key", type = "password")
    prompt = st.text_area(label = ":question: **Your Prompt**", value="", max_chars=250, placeholder= "Insert here your prompt")
    temperature = st.slider(":thermometer: **Temperature**", min_value=0.0, max_value=2.0, value=0.8, help = "Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.")
    top_p = st.slider(":bar_chart: **Top-P**", min_value=0.01, max_value=1.0, value=1.0, help = "An **alternative** to sampling with temperature where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. Do not use combined with high temperature.")
    max_tokens = st.slider(":scroll: **Max Tokens**", min_value= 32, max_value= 4096, value =1024, help = "The maximum number of tokens that can be generated.")

openai.api_key = st.secrets.openai_key

st.title("💬 Which GPT Model should I use? (Beta)")
"#"
with st.expander("How it works :question:"):
    st.write("Choose the right model can be a messy. Use this application to **compare the outcomes** of different OpenAI Models from ChatCompletion API.")
    #st.write(":one: Insert your **OpenAI API Key**")
    st.write(":one: **Type prompt** you want to test")
    st.write(":two: Set-up prompt **parameters**")
    st.write(":three: **Compare results** in term of quality and costs")
    st.write(":four: **Iterate** the process")
    

#OpenAI API Calling

completion_gpt35 = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature = temperature,
    top_p = top_p ,
    max_tokens = max_tokens,
    messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
  ]
)
answer_gpt35 = completion_gpt35.choices[0].message

completion_gpt35_1106 = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-1106",
    temperature = temperature,
    top_p = top_p ,
    max_tokens = max_tokens,
    messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
  ]
)
answer_gpt35_1106 = completion_gpt35_1106.choices[0].message

completion_gpt40 = openai.ChatCompletion.create(
    model="gpt-4",
    temperature = temperature,
    top_p = top_p ,
    max_tokens = max_tokens,
    messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
  ]
)
answer_gpt40 = completion_gpt40.choices[0].message

## give_a_score35 = openai.Completion.create(
##    model="gpt-3.5-turbo-instruct",
##    prompt = f"""Give me a number between 1 and 5 rating the following answer in terms of coherence with the query, completeness of the answer, grammary Spelling. I want just 1 number as output. Example of answer: 4
##                 This is the query: {prompt}. This is the answer {answer_gpt35}.""")

## give_a_score351106 = openai.Completion.create(
##    model="gpt-3.5-turbo-instruct",
##    prompt = f"""Give me a number between 1 and 5 rating the following answer in terms of coherence with the query, completeness of the answer, grammary Spelling. I want just 1 number as output. Example of answer: 4
##                 This is the query: {prompt}. This is the answer {answer_gpt35_1106}.""")

##give_a_score_40 = openai.Completion.create(
##    model="gpt-3.5-turbo-instruct",
##    prompt = f"""Give me a number between 1 and 5 rating the following answer in terms of coherence with the query, completeness of the answer, grammary Spelling. I want just 1 number as output. Example of answer: 4
##                 This is the query: {prompt}. This is the answer {answer_gpt40}.""")



col1, col2, col3 = st.columns(3)

with col1:
  st.header("**gpt-3.5-turbo**")
  
  st.markdown("Snapshot of **GPT-3.5-turbo** from **June 13th 2023**. Best in terms of performance / cost ratio for simple textual tasks (**4,096 tokens** as context window).")
  st.link_button("Model", url="https://platform.openai.com/docs/models/gpt-3-5", help=None, type="secondary", disabled=False, use_container_width=False)
  cola, colb, colc = st.columns(3)
  with cola:
    st.metric(":boom: Tokens", value = str(completion_gpt35["usage"]["completion_tokens"])+"T", help = "Tokens can be thought of as pieces of words. This number refers to *completion tokens*. You should be aware also of *prompt tokens* when evaluating full costs.")
  with colb:
    st.metric(":money_with_wings: Cost", value = str(round(completion_gpt35["usage"]["completion_tokens"]*0.002,2))+"$", help ="Cost in $ per 1 thousand operations.")
  with colc:
    "#"
 
  st.info(answer_gpt35['content'], icon=None)
  ##score_gpt35="⭐"*int(give_a_score35.choices[0].text)
  ##st.markdown(f'<div style="text-align: right;">{score_gpt35}</div>', unsafe_allow_html=True)
  
with col2:
  st.header("**gpt-3.5-turbo-1106**")
  st.markdown("**GPT-3.5 Turbo** model with **improved instruction following**, JSON mode, reproducible outputs, parallel function calling (**16,385 tokens** as context window).")
  st.link_button("Model", url="https://platform.openai.com/docs/models/gpt-3-5", help=None, type="secondary", disabled=False, use_container_width=False)
  cold, cole, colf = st.columns(3)
  with cold:
    st.metric(":boom: Tokens", value = str(completion_gpt35_1106["usage"]["completion_tokens"])+"T", help = "Tokens can be thought of as pieces of words. This number refers to *completion tokens*. You should be aware also of *prompt tokens* when evaluating full costs.")
  with cole:
    st.metric(":money_with_wings: Cost", value =str(round(completion_gpt35_1106["usage"]["completion_tokens"]*0.002,2))+"$", help ="Cost in $ per 1 thousand operations.")
  with colf:
    "#"  
  st.info(answer_gpt35_1106['content'], icon=None)
  ##score_gpt_351106="⭐"*int(give_a_score351106.choices[0].text)
  ##st.markdown(f'<div style="text-align: right;">{score_gpt_351106}</div>', unsafe_allow_html=True)

with col3:
  st.header("**gpt-4**")
  st.markdown("GPT-4 is a **large multimodal model** optimized for chat but works well for traditional completions tasks with advanced reasoning capabilities (**8,192 tokens** as context window).")
  st.link_button("Model", url="https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo", help=None, type="secondary", disabled=False, use_container_width=False)
  colg, colh, coli = st.columns(3)
  with colg:
    st.metric(":boom: Tokens", value = str(completion_gpt40["usage"]["completion_tokens"])+"T", help = "Tokens can be thought of as pieces of words. This number refers to *completion tokens*. You should be aware also of *prompt tokens* when evaluating full costs.")
  with colh:
    st.metric(":money_with_wings: Cost", value =str(round(completion_gpt40["usage"]["completion_tokens"]*0.006,2))+"$", help ="Cost in $ per 1 thousand operations.")
  with coli:
    "#"  
  st.info(answer_gpt40['content'], icon=None)
  ##score_gpt40="⭐"*int(give_a_score_40.choices[0].text)
  ##st.markdown(f'<div style="text-align: right;">{score_gpt40}</div>', unsafe_allow_html=True)


