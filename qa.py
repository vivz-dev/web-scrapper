from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

chrome_options = Options()
chrome_options.add_argument("--headless")  # Ejecutar sin interfaz
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

base_url = "URLBASEDELABUSQUEDA"

def obtener_texto(url):
    resultado = ''
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)  
        driver.get(url)
        elementos = driver.find_elements(By.CSS_SELECTOR, "a.results-list-item-link")
        elemento = elementos[0]
        link = elemento.get_attribute('href') 
        driver.get(link)
        elementos2 = driver.find_elements(By.CSS_SELECTOR, "div.article-body")
        texto = ""
        for x in elementos2:
            # print(x.text)
            texto = texto + x.text + " "
        driver.quit()
        texto = texto.replace("\n", " ")
        resultado = texto
        # print(texto)
    except Exception as e:
        print(e)
    return resultado

def convertir_xlsx_a_csv(archivo_xlsx, archivo_csv):
    df = pd.read_excel(archivo_xlsx, engine="openpyxl")
    #preguntas = df['pregunta']
    data = {
        "pregunta": [],
        "respuesta": [],
        "respuesta_llm": []
    }

    for index, row in df.iterrows():
        pregunta = row["pregunta"]
        respuesta = row["respuesta"]
        respuesta_llm = row["respuesta_llm"]
        query = str(pregunta).strip().replace("¿", "%C2%BF").replace("?", "%3F").replace(" ", "+")
        URL_CONSULTA = base_url + query
        respuesta = obtener_texto(URL_CONSULTA)
        data["pregunta"].append(pregunta)
        data["respuesta"].append(respuesta)
        data["respuesta_llm"].append(respuesta_llm)

    nuevo_df = pd.DataFrame(data)
    nuevo_df.to_csv(archivo_csv, index=False, encoding="utf-8")

convertir_xlsx_a_csv("human_feedback (1).xlsx", "human_feedback.csv")