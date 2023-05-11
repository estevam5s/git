import pandas as pd
from deta import Deta
import streamlit as st
import plotly.express as px


DETA_KEY = "e0u31gqkqju_2Ps7fJD5a1kAKF2Rr4Y31ASSdvUUeX8Y"
deta = Deta(DETA_KEY)


db_deta_lucrobruto = deta.Base("lucrobruto")


def fetch_all_items(db):
  items = []
  result = db.fetch()
  for item in result.items:
      items.extend(item)
  return items

def analyse_and_add_gross_profit():
  # Fetch all items from the Deta Base
  items = fetch_all_items(db_deta_lucrobruto)

  # Convert the items into a DataFrame
  df = pd.DataFrame(items)

  # Calculate the gross profit
  df['lucro_bruto'] = df['venda'] - df['custo']

  # Plot the gross profit
  fig = px.line(df, x="data", y="lucro_bruto", title="Lucro Bruto ao Longo do Tempo")
  # st.plotly_chart(fig)

  # Ask the user if they want to add a new sale
  data = st.date_input("Data da venda:")
  venda = st.number_input("Valor da venda:")
  custo = st.number_input("Custo da venda:")

  # Add a submit button
  if st.button("Enviar"):
    # Add the new sale to the Deta Base
    db_deta_lucrobruto.put({
        "data": str(data),
        "venda": venda,
        "custo": custo
    })

    st.success("Venda adicionada com sucesso!")