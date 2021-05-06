import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import requests

base_url='https://jobs.github.com/positions.json?description={}&location={}'



JOB_HTML_TEMPLATE = """
<div style="width:100%;height:100%;margin:1px;padding:5px;position:relative;border-radius:5px;border-bottom-right-radius: 10px;box-shadow:0 0 1px 1px #f79292;background-color: #e9f0f2;
  border-left: 5px solid #e9f0f2;color:red;">
<label>Post Date</label>
<h6>{}</h6>
<label>Company</label>
<h4>{}</h4>
<br>
<label>Job Title</label>
<h5>{}</h5>
<br>
<label>Location</label>
<h5>{}</h5>
<br>
<label>Company URL</label>
<h6>{}</h6>
<br>
</div>
"""


def get_data(url):
    resp = requests.get(url)
    return resp.json()

def main():
    menu = ['Home','About']
    choice = st.sidebar.selectbox("Menu",menu)

    st.title('Developers.search Jobs')

    if choice =="Home":
        st.subheader('Home')

        #Nav search form
        with st.form(key = 'searchform'):
            nav1,nav2,nav3 = st.beta_columns([3,2,1])
            with nav1:
                search_term = st.text_input("Search Job")
            with nav2:
                location = st.text_input('Location')
            with nav3:
                st.text('Search Job')
                submit_search = st.form_submit_button(label='Search')

        st.success('You searched for {} in {}'.format(search_term,location))    


        #Results
        col1, col2 = st.beta_columns([2,1])

        with col1:
            if submit_search:
                #Create Search Query
                search_url = base_url.format(search_term,location)
                data = get_data(search_url)
                number_of_results = len(data)
                st.header('Showing {} jobs'.format(number_of_results))

                for i in data:
                    job_post_date = i['created_at']
                    job_company = i['company']
                    job_title = i['title']
                    job_location = i['location']
                    job_company_url = i['company_url']
                    job_dec = i['description']
                    job_howtoapply = i['how_to_apply']

                    st.markdown(JOB_HTML_TEMPLATE.format(job_post_date,
                                                        job_company,
                                                        job_title,
                                                        job_location,
                                                        job_company_url), unsafe_allow_html=True)
                    #Description
                    st.subheader('Discription')
                    with st.beta_expander('Description'):
                        stc.html(job_dec,scrolling=True)  

                    st.subheader('How to Apply')
                    with st.beta_expander('How To Apply'):
                        stc.html(job_howtoapply,scrolling=True) 
                    st.write("")     
                    st.write("")     
                    st.write("")

        with col2:
            with st.form(key='email_form'):
                st.write('Be The First to get new Job info')
                email = st.text_input('Email')
                sumbit_email = st.form_submit_button(label='Subscribe')

                if sumbit_email:
                    st.success("The message sent to {}".format(email))



    else:
        st.subheader('About')    


if __name__ == '__main__':
    main()