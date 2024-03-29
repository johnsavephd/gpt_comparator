
#-------------------------Import libraries-------------------------

import streamlit as st
import openai
import psycopg2 as pg
import matplotlib.pyplot as plt

#--------------------------OpenAI API Key--------------------------

openai.api_key = st.secrets.openai_key

#------------------------Page configuration------------------------

st.set_page_config(page_title="GPT Comparator", page_icon="🤖", layout="wide")

#------------------------Model Selection----------------------

model_1 = "gpt-3.5-turbo-0125"
model_2 = "gpt-4"
model_3 = "gpt-4-0125-preview"

cost_vector = [0.0015, 0.06, 0.03] #https://openai.com/pricing

#------------------------Function Definition-----------------------

def ask_function(model, context, prompt, temperature, top_p, max_tokens):
  
  completion = openai.ChatCompletion.create(
      model = model,
      temperature = temperature,
      top_p = top_p ,
      max_tokens = max_tokens,
      messages=[
      {"role": "system", "content": context},
      {"role": "user", "content": prompt}
    ]
  )

  return completion

def set_up_values():
    st.session_state.context = "You are an helpful assistant"
    st.session_state.prompt = ""
    st.session_state.temperature = 0.8
    st.session_state.top_p = 1
    st.session_state.max_tokens = 1024

def write_postgres(user_query, system_role, temperature, top_p, max_tokens, model_1, model_2, model_3, answer_1, answer_2, answer_3, token_1, token_2, token_3, love_1, love_2, love_3):

  try:
    conn = pg.connect(
      host=st.secrets.host,
      database=st.secrets.database,
      user=st.secrets.user,
      password=st.secrets.mypassword
  )
    cur = conn.cursor()

    # Esecuzione della query SQL per l'inserimento
    query = f"""INSERT INTO streamlit_gpt_comparator (
      user_query,
      system_role,
      temperature,
      top_p,
      max_tokens,
      model_1, 
      model_2, 
      model_3,
      answer_1,
      answer_2,
      answer_3,
      token_1,
      token_2,
      token_3,
      love_1,
      love_2,
      love_3,
      create_time
    
      ) 
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)"""
    
    data = (user_query, system_role, temperature, top_p, max_tokens, model_1, model_2, model_3, answer_1, answer_2, answer_3, token_1, token_2, token_3, love_1, love_2, love_3)
    
    cur.execute(query, data)
    conn.commit()
    
    st.toast('Thank you! Your feedback has been saved', icon="✅")

  except Exception as e:
          print(f"Si è verificato un errore: {e}")
  
  finally:
    cur.close()
    conn.close()
    
  st.session_state['love_1_list'] += [love_1]
  st.session_state['love_2_list'] += [love_2]
  st.session_state['love_3_list'] += [love_3]

  st.session_state['token_1_list'] += [token_1]
  st.session_state['token_2_list'] += [token_2]
  st.session_state['token_3_list'] += [token_3]
  
  st.session_state.gpt35love = False
  st.session_state.gpt40love = False
  st.session_state.gpt41love = False
  st.session_state.prompt = ""
  #st.session_state.context = "You are an helpful assistant"

def plot_average(lists, cost_vector,model_1, model_2, model_3):

    weighted_averages = [sum(lst) / len(lst) * cost for lst, cost in zip(lists, cost_vector)]


    fig, ax = plt.subplots()
    bars = ax.bar(range(len(lists)), weighted_averages, tick_label=[model_1, model_2, model_3])


    for bar, value in zip(bars, weighted_averages):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{value:.2f} $', ha='center', va='bottom')


    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    plt.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
    
    # Display the plot
    st.pyplot(fig)

#--------------------------Temporaty Storing-------------------------

if 'love_1_list' not in st.session_state:
  st.session_state['love_1_list'] = [0]

if 'love_2_list' not in st.session_state:
  st.session_state['love_2_list'] = [0]

if 'love_3_list' not in st.session_state:
  st.session_state['love_3_list'] = [0]

if 'token_1_list' not in st.session_state:
  st.session_state['token_1_list'] = [0]

if 'token_2_list' not in st.session_state:
  st.session_state['token_2_list'] = [0]

if 'token_3_list' not in st.session_state:
  st.session_state['token_3_list'] = [0]


#--------------------------Sidebar Section-------------------------

def main():
  with st.sidebar:  
      
      with st.form(key='gpt_parameters', border = False):
        
        st.header(" GPT Parameters Set-up")
        st.markdown("Please fill in the following fields to configure GPT parameters and compare the results.")
        #api_key = st.text_input(label = ":key: **OpenAI API Key**", value="", placeholder= "Insert here your API Key", type = "password")
        
        context = st.text_area(label = "🤖 **Role of the system**", key = "context", value="You are an helpful assistant", max_chars=250, placeholder= "You are an helpful assistant", help = "Set the role of the system. If you want, specify also the personality (ex: irriverent, funny ...)")
        prompt = st.text_area(label = ":question: **Your Prompt**", key = "prompt", value="", max_chars=500, placeholder= "Insert here your prompt", help = "Type here an instruction in natural language" )
        temperature = st.slider(":thermometer: **Temperature**", key = "temperature", min_value=0.0, max_value=2.0, value=0.8, help = "Higher values, such as 0.8, will result in more random output, while lower values, like 0.2, will make it more focused and deterministic")
        top_p = st.slider(":bar_chart: **Top-P**", key = "top_p", min_value=0.01, max_value=1.0, value=1.0, help = "An **alternative** to sampling with temperature where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. Do not use combined with high temperature")
        max_tokens = st.slider(":scroll: **Max Tokens**", key = "max_tokens", min_value= 32, max_value= 1024, value = 1024, help = "The maximum number of tokens that can be generated. In this application they will be limited to 1024 for cost savings and performance reasons")
        
        co10, col11, col12, col9,col8 = st.columns([1,1,1,1,1])

        with col9: 
          submit_button = st.form_submit_button(label=':heavy_check_mark:')
        with col8:
          clear_button = st.form_submit_button(label=':x:', on_click = set_up_values)
          
  #--------------------------Title--------------------------
      
  col1, col2 = st.columns([30,10])
  with col1:
    st.title('Which GPT should I use in my application?')
  with col2:
    "#"
    with st.spinner("Generating with gpt-3.5-turbo-0125 ..."):
      gpt35 = ask_function(model_1, context, prompt, temperature, top_p, max_tokens)
      answer_gpt35 = gpt35.choices[0].message
      tokens_gpt35 = gpt35["usage"]["completion_tokens"]
     

    with st.spinner("Generating with gpt-4 ..."):
      gpt40 = ask_function(model_2, context, prompt, temperature, top_p, max_tokens)
      answer_gpt40 = gpt40.choices[0].message
      tokens_gpt40 = gpt40["usage"]["completion_tokens"]

    with st.spinner("Generating with gpt-4-0125-preview..."):
      gpt40_125 = ask_function(model_3, context, prompt, temperature, top_p, max_tokens)
      answer_gpt40_125 = gpt40_125.choices[0].message
      tokens_gpt40_125 = gpt40_125["usage"]["completion_tokens"]



  #-------------------------Main Section-------------------------
      
  tabMain, tabStat, tabInfo = st.tabs(["Main", "Stat", "Info"])

  with tabMain:
    
    
    col1, col2, col3 = st.columns(3)

    with col1:
      st.header("**gpt-3.5-turbo-0125**")
      ":boom: 16.385 Tokens | :calendar: Up to Sep 2021"

      st.markdown("The latest GPT-3.5 Turbo model with higher accuracy at responding in requested formats an completing tasks")
      st.link_button("Model", url="https://platform.openai.com/docs/models/gpt-3-5", help=None, type="secondary", disabled=False, use_container_width=False)

      cola, colb, colc = st.columns(3)
      with cola:
        st.metric(":boom: Tokens", value = str(tokens_gpt35)+"T", help = "Tokens can be thought of as pieces of words. This number refers to *completion tokens*. You should be aware also of *prompt tokens* when evaluating full costs")
      with colb:
        st.metric(":money_with_wings: Cost", value = str(round(tokens_gpt35*cost_vector[0],2))+"$", help ="Cost in $ per 1 thousand operations")
      with colc:
        "#"
      
      st.info(answer_gpt35['content'], icon=None)
      st.checkbox(key = "gpt35love", label="I prefer gpt-3.5-turbo answer", on_change = write_postgres, args=(prompt, context, temperature, top_p, max_tokens, model_1, model_2, model_3, answer_gpt35['content'], answer_gpt40['content'], answer_gpt40_125['content'], tokens_gpt35, tokens_gpt40, tokens_gpt40_125, True, False, False,))
      
    with col2:
      st.header("**gpt-4**")
      ":boom: 8.192 Tokens | :calendar: Up to Sep 2021"
    
      st.markdown("GPT-4 is a large multimodal model optimized for chat and completions tasks with advanced reasoning capabilities")
      st.link_button("Model", url="https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo", help=None, type="secondary", disabled=False, use_container_width=False)
      colg, colh, coli = st.columns(3)
      with colg:
        st.metric(":boom: Tokens", value = str(tokens_gpt40)+"T", help = "Tokens can be thought of as pieces of words. This number refers to *completion tokens*. You should be aware also of *prompt tokens* when evaluating full costs")
      with colh:
        st.metric(":money_with_wings: Cost", value =str(round(tokens_gpt40*cost_vector[1],2))+"$", help ="Cost in $ per 1 thousand operations")
      with coli:
        "#"  
      st.info(answer_gpt40['content'], icon=None)
      st.checkbox(key = "gpt40love", label="I prefer gpt-4 answer", on_change = write_postgres, args=(prompt, context, temperature, top_p, max_tokens, model_1, model_2, model_3, answer_gpt35['content'], answer_gpt40['content'], answer_gpt40_125['content'], tokens_gpt35, tokens_gpt40, tokens_gpt40_125, False, True, False,))

    with col3:
      st.header("**gpt-4-0125-preview**")
      ":boom: 128.000 Tokens | :calendar: Up to Dec 2023"
    
      st.markdown("GPT-4 model with reduced cases of laziness and extended context window, where the model doesn't complete the task")
      st.link_button("Model", url="https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo", help=None, type="secondary", disabled=False, use_container_width=False)
      cold, cole, colf = st.columns(3)
      with cold:
        st.metric(":boom: Tokens", value = str(tokens_gpt40_125)+"T", help = "Tokens can be thought of as pieces of words. This number refers to *completion tokens*. You should be aware also of *prompt tokens* when evaluating full costs")
      with cole:
        st.metric(":money_with_wings: Cost", value =str(round(tokens_gpt40_125*cost_vector[2],2))+"$", help ="Cost in $ per 1 thousand operations")
      with colf:
        "#"  
      st.info(answer_gpt40_125['content'], icon=None)
      st.checkbox(key = "gpt41love", label="I prefer gpt-4-0125-preview answer", on_change = write_postgres, args=(prompt, context, temperature, top_p, max_tokens, model_1, model_2, model_3, answer_gpt35['content'], answer_gpt40['content'], answer_gpt40_125['content'], tokens_gpt35, tokens_gpt40, tokens_gpt40_125, False, False, True,))

      with tabStat:
        love_1_perc = sum(st.session_state['love_1_list']) 
        love_2_perc = sum(st.session_state['love_2_list']) 
        love_3_perc = sum(st.session_state['love_3_list']) 

        
        colm, coln = st.columns(2)
        with colm:
          st.subheader("Average cost for 1.000 query :money_with_wings:", help = "Here you can compare costs you will sustain for 1.000 API calls")
          if love_1_perc + love_2_perc + love_3_perc > 0:
            plot_average([st.session_state['token_1_list'],st.session_state['token_2_list'],st.session_state['token_3_list']], cost_vector, model_1, model_2, model_3)
          
        with coln:
         st.subheader("Your preferences :thumbsup::thumbsdown:", help="Here you can see your model selections")

         labels = "gpt-3.5-turbo-0125", "gpt-4", "gpt-4-0125-preview"
         sizes = [float(love_1_perc), float(love_2_perc), float(love_3_perc)]

         filtered_labels = [label for label, size in zip(labels, sizes) if size > 0]
         filtered_sizes = [size for size in sizes if size > 0]

         if sum(filtered_sizes) > 0:
            fig1, ax1 = plt.subplots()
            ax1.pie(filtered_sizes, labels=filtered_labels, autopct='%1.1f%%',
                    shadow=False, startangle=90)
            ax1.axis('equal')  
        
            st.pyplot(fig1)

      with tabInfo:
        c1, c2 = st.columns(2)
        with c1:
          st.subheader("Why this application :question:")
          st.markdown("Are you a **developer** looking for **integrating a GPT model** in your application? Have you ever wondered what the main differences are among them? Choosing the right model can be a bit overwhelming. Use this application to compare the results from different models and see the differences for yourself. Yes, but **make sure to check out the documentation** afterward! 😊")
          st.subheader("Pay attention to this :zap:")
          st.markdown("Please be mindful of the fact that **any queries you submit will be stored** in an anonymized manner, exclusively for research and training purposes. It is imperative to note that under no circumstances should you incorporate or divulge any **confidential or sensitive information** in your interactions. Your cooperation in this regard ensures the integrity of our commitment to privacy and data security")
          st.subheader("Send me feedbacks :exclamation:")
          st.markdown("Please fell free to send me feedbacks or ideas to improve the app. You can find me on [linkedin](https://www.linkedin.com/in/giovanni-salvi-5aa278158/) 😊")
          
        with c2:
        #st.info("Please be aware that your queries will be stored anonymously for research and training purposes. Under no circumstances should you insert confidential information.", icon = "⚠️")
          st.subheader("The process :three_button_mouse:")
          st.image("processes.png")
          

if __name__ == '__main__':
    main()
