import requests
import pandas as pd
import streamlit as st
from helpers import *
from ref import *


# Initiate Data App
st.title("Plan Quoting Tool")

st.markdown('')

#Set-up drag & drop input for csv upload into dataframe
file = st.file_uploader("Drop your census file here to load", type={"csv"})

#Upload file and return message when complete
try:
    inputs = pd.read_csv(file)
    st.text("Upload success!")
except ValueError:
    st.text("Waiting for file...")


#Run Batch
@st.cache(suppress_st_warning=True)
def get_data(x, rm, url, headers): #(x, rm, url, headers, threads)
    req = to_json(x, rm)
    print(req)
    #store = threaded_process_range(req, url, headers, threads, range(threads))
    store = asyncio.run(async_batch_call(url, headers, req))
    z = write_results(store)
    return z

try:
    res = get_data(inputs, request_meta, url, headers)
    res_df = pd.json_normalize(res)
    premium = res_df['Premium'].sum()
    st.subheader('Annual Premium: :blue[${:0,.0f}]'.format(premium).replace('$-','-$'))

except:
    pass


