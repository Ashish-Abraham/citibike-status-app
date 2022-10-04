import streamlit
import pandas as pd
import snowflake.connector
from urllib.error import URLError

streamlit.title('Citibike station')


#Adding Background Image

streamlit.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://bicycle2work.com/wp-content/uploads/2019/03/cycling-in-new-york-city-e1551818622466-1024x650.jpg")
    }
   .sidebar .sidebar-content {
        background: url("https://bicycle2work.com/wp-content/uploads/2019/03/cycling-in-new-york-city-e1551818622466-1024x650.jpg")
    }
    </style>
    """,
    unsafe_allow_html=True
)

# connect to snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()

my_cur.execute("""select * from citibike_status""")
my_catalog = my_cur.fetchall()
df = pd.DataFrame(my_catalog)

#streamlit.write(df)
hdrs = pd.DataFrame(my_cur.description)

id_list = df[0].values.tolist()
#streamlit.write(id_list)

option = streamlit.selectbox('Choose the station id to view the status:', list(id_list))
if streamlit.button('show status'):
          my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
          my_cur = my_cnx.cursor()
          my_cur.execute("""select * from citibike_status where "id" = """ + option + """; """)
          res = my_cur.fetchall()
          df2=pd.DataFrame(res,columns=hdrs['name']).loc[0]
          col1, col2 = streamlit.columns(2)
          for c in hdrs['name']:
                    with col1:
                              streamlit.write(*[x.upper() for x in c.split("_")], ":")
                    with col2:
                              streamlit.write(df2.at[c])
                    
  

