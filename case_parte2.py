import zipfile
import pdfplumber
import pandas as pd
from io import BytesIO

def extract_tables_from_pdf(zip_path, pdf_filename):
    with zipfile.ZipFile(zip_path, 'r') as z:
        with z.open(pdf_filename) as pdf_file:
            pdf_bytes = BytesIO(pdf_file.read())
            
            all_tables = []
            with pdfplumber.open(pdf_bytes) as pdf:
                for page_num in range(2, 181):  # Páginas 3 a 181 (índices base 0)
                    tables = pdf.pages[page_num].extract_tables()
                    for table in tables:
                        df = pd.DataFrame(table)
                        all_tables.append(df)
            
            final_df = pd.concat(all_tables, ignore_index=True)
            final_df.columns = final_df.iloc[0].str.replace('\n', ' ', regex=True)  # Remove quebras de linha
            final_df = final_df[1:].reset_index(drop=True)  # Remove a primeira linha dos dados
            return final_df

# Exemplo de uso
zip_path = "C:/Users/My/Desktop/teste de nivelamento 2/anexos_ans.zip"
pdf_filename = "Anexo_1_Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
output_csv = "tabelas_extraidas.csv"

df = extract_tables_from_pdf(zip_path, pdf_filename)
df = df.rename(columns={"OD": "Seg.Odontologica",
                        "AMD": "Seg.Ambulatorial"})
df.to_csv(output_csv, index=False)

