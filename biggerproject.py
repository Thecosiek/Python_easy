""" Project is centered around creating statistics, data frames and charts base on databank of drugs """


import xml.etree.ElementTree as ET
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib.patches as mpatches
import random
from fastapi import FastAPI
import requests

# os.chdir('C:/Users/monik/OneDrive/Pulpit') # do kompilacji na moim laptopie


""" Zadanie1 """

tree = ET.parse("drugbank_partial.xml")
root = tree.getroot()
ns = {"drugbank": "http://www.drugbank.ca"}
data = []

for drug in root.findall("drugbank:drug", ns):
    
    drug_id = drug.find("drugbank:drugbank-id", ns).text
    
    name = drug.find("drugbank:name", ns).text
    
    drug_type = drug.get("type")  
    
    description = drug.find("drugbank:description", ns)
    description = description.text if description is not None else "Brak danych"

    dosage_form = drug.find("drugbank:dosages/drugbank:dosage/drugbank:form", ns)
    dosage_form = dosage_form.text if dosage_form is not None else "Brak danych"

    indications = drug.find("drugbank:indication", ns)
    indications = indications.text if indications is not None else "Brak danych"

    mechanism = drug.find("drugbank:mechanism-of-action", ns)
    mechanism = mechanism.text if mechanism is not None else "Brak danych"

    food_interactions = drug.findall("drugbank:food-interactions/drugbank:food-interaction", ns)
    food_interactions = "; ".join([fi.text for fi in food_interactions]) if food_interactions else "Brak danych"

    data.append([drug_id, name, drug_type, description, dosage_form, indications, mechanism, food_interactions])



df = pd.DataFrame(data, columns=[
    "DrugBank_ID", "Nazwa", "Typ", "Opis", "Postać", "Wskazania", "Mechanizm_działania", "Interakcje_z_pokarmami"
])

# df.to_csv("Zaliczeniowe1.csv", index=False, encoding="utf-8")

""" Zadanie2 """

tree = ET.parse("drugbank_partial.xml")  
root = tree.getroot()
ns = {"drugbank": "http://www.drugbank.ca"}
data = []

for drug in root.findall("drugbank:drug", ns):
    
    drug_id = drug.find("drugbank:drugbank-id", ns).text
    name = drug.find("drugbank:name", ns).text
    
    synonyms = drug.findall("drugbank:synonyms/drugbank:synonym", ns)
    synonym_list = [syn.text for syn in synonyms] if synonyms else []

    for synonym in synonym_list:
        data.append([drug_id, name, synonym])

df_synonyms = pd.DataFrame(data, columns=["DrugBank_ID", "Nazwa", "Synonim"])

# df_synonyms.to_csv("Zaliczeniowe2.csv", index=False, encoding="utf-8")

def create_synonym_graph(drugbank_id):
    
    df = df_synonyms[df_synonyms['DrugBank_ID'] == drugbank_id]
    G = nx.Graph()
    
    main_drug_name = df['Nazwa'].iloc[0]
    G.add_node(main_drug_name)
    
    for _, row in df.iterrows():
        synonym = row['Synonim']
        G.add_node(synonym)
        G.add_edge(main_drug_name, synonym)
    
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='red', edge_color='blue', node_size=2000, font_size=10, font_weight='bold')
    plt.title(f"Graf synonimów dla {main_drug_name} (DrugBank ID: {drugbank_id})")
    plt.show()

# create_synonym_graph("DB00001")

""" Zadanie3 """

tree = ET.parse("drugbank_partial.xml")
root = tree.getroot()
ns = {"drugbank": "http://www.drugbank.ca"}
data = []

for drug in root.findall("drugbank:drug", ns):
    
    drug_id = drug.find("drugbank:drugbank-id", ns).text
    
    for product in drug.findall("drugbank:products/drugbank:product", ns):
        
        product_name = product.find("drugbank:name", ns).text
        manufacturer = product.find("drugbank:labeller", ns).text
        ndc_elem = product.find("drugbank:ndc-product-code", ns)
        ndc = ndc_elem.text.strip() if ndc_elem is not None and ndc_elem.text else "Brak NDC"
        dosage_form = product.find("drugbank:dosage-form", ns).text
        route = product.find("drugbank:route", ns).text
        dosage = product.find("drugbank:strength", ns).text
        country = product.find("drugbank:country", ns).text
        registering_agency = product.find("drugbank:source", ns).text

        data.append([drug_id, product_name, manufacturer, ndc, dosage_form, route, dosage, country, registering_agency])


df_products = pd.DataFrame(data, columns=[
    "DrugBank_ID", "Nazwa produktu", "Producent", 
    "National Drug Code (NDC)", "Postać", "Sposób aplikacji", "Dawka", 
    "Kraj", "Agencja rejestrująca"
])

# df_products.to_csv("Zaliczeniowe3.csv", index=False, encoding="utf-8")


""" Zadanie4 """

tree = ET.parse("drugbank_partial.xml")
root = tree.getroot()
ns = {"drugbank": "http://www.drugbank.ca"}
data = []

for drug in root.findall("drugbank:drug", ns):

    for pathway in drug.findall("drugbank:pathways/drugbank:pathway", ns):
        pathway_id = pathway.find("drugbank:smpdb-id", ns).text
        pathway_name = pathway.find("drugbank:name", ns).text
        category = pathway.find("drugbank:category", ns).text

        data.append([pathway_id, pathway_name, category])

df = pd.DataFrame(data, columns=["Pathway_ID", "Nazwa szlaku", "Kategoria"])

total_unique_pathways = df["Pathway_ID"].nunique()


# df.to_csv("Zaliczeniowe4.csv", index=False, encoding="utf-8")

""" Zadanie5 """

tree = ET.parse("drugbank_partial.xml")
root = tree.getroot()
ns = {"drugbank": "http://www.drugbank.ca"}
data = []

for drug in root.findall("drugbank:drug", ns):

    for pathway in drug.findall("drugbank:pathways/drugbank:pathway", ns):
        pathway_name = pathway.find("drugbank:name", ns).text
        
        for pathway_drugs in pathway.findall("drugbank:drugs/drugbank:drug", ns):
            drug_name = pathway_drugs.find("drugbank:name", ns).text
            
            data.append([pathway_name, drug_name])


df = pd.DataFrame(data, columns=["Pathway_Name", "Drug_Name"])
# df.to_csv("Zaliczeniowe5.csv", index=False, encoding="utf-8")

def draw_pathway_graph(df):
    G = nx.Graph()

    pathways = df["Pathway_Name"].unique()
    drugs = df["Drug_Name"].unique()

    G.add_nodes_from(pathways, bipartite=0) 
    G.add_nodes_from(drugs, bipartite=1) 
    
    for _, row in df.iterrows():
        G.add_edge(row["Pathway_Name"], row["Drug_Name"])

    pos = {}
    left_x = -1 
    right_x = 1  

    for i, pathway in enumerate(pathways):
        pos[pathway] = (left_x, i * 2)

    for i, drug in enumerate(drugs):
        pos[drug] = (right_x, i * 2)

    node_colors = ["red" if node in pathways else "blue" for node in G.nodes()]

    plt.figure(figsize=(14, 8))
    nx.draw(G, pos, with_labels=True, node_size=3000, 
            node_color=node_colors, edge_color="gray", 
            font_size=12, font_weight="bold")
    
    x_min, x_max = -1.5, 1.5  
    y_min, y_max = -2, max(len(pathways), len(drugs)) * 2  
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    plt.title("Graf interakcji leków ze szlakami", fontsize=14)
    plt.show()

# draw_pathway_graph(df)

""" Zadanie6 """

tree = ET.parse("drugbank_partial.xml")
root = tree.getroot()
ns = {"drugbank": "http://www.drugbank.ca"}
data = []


for drug in root.findall("drugbank:drug", ns):

    drug_name1 = drug.find("drugbank:name", ns).text
    
    pathway_count = 0

    for pathway in drug.findall("drugbank:pathways/drugbank:pathway", ns):
        
        for pathway_drugs in pathway.findall("drugbank:drugs/drugbank:drug", ns):
            drug_name = pathway_drugs.find("drugbank:name", ns).text
            
            if drug_name == drug_name1 :
                pathway_count += 1
    
    data.append([drug_name1, pathway_count])
                    
df = pd.DataFrame(data, columns=["Drug_Name", "Pathway_Count"])

# df.to_csv("Zaliczeniowe6.csv", index=False, encoding="utf-8")

plt.figure(figsize=(12, 6))
bins = np.arange(df["Pathway_Count"].min(), df["Pathway_Count"].max() + 2) 
plt.hist(df["Pathway_Count"], bins=bins, edgecolor="black", alpha=0.7)

plt.xticks(bins)  

plt.xlabel("Liczba szlaków, z którymi lek wchodzi w interakcje", fontsize=12)
plt.ylabel("Liczba leków", fontsize=12)
plt.title("Histogram liczby szlaków interakcji dla leków", fontsize=14)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# plt.show()

""" Zadanie7 """

tree = ET.parse("drugbank_partial.xml")
root = tree.getroot()
ns = {"drugbank": "http://www.drugbank.ca"}
data = []

for drug in root.findall("drugbank:drug", ns):
    
    drugbank_id = drug.find("drugbank:drugbank-id", ns).text

    for target in drug.findall("drugbank:targets/drugbank:target", ns):
        target_id = target.find("drugbank:id", ns).text
        source = target.find("drugbank:polypeptide", ns).get("source") if target.find("drugbank:polypeptide", ns) is not None else None 
        ext_id = target.find("drugbank:polypeptide", ns).get("id") if target.find("drugbank:polypeptide", ns) is not None else None
        polypeptide_name = target.find("drugbank:polypeptide/drugbank:name", ns).text if target.find("drugbank:polypeptide/drugbank:name", ns) is not None else None
        gene_name = target.find("drugbank:polypeptide/drugbank:gene-name", ns).text if target.find("drugbank:polypeptide/drugbank:gene-name", ns) is not None else None
        genatlas_id = None
        
        for ext in target.findall("drugbank:polypeptide/drugbank:external-identifiers/drugbank:external-identifier", ns):
            if ext.find("drugbank:resource", ns).text == "GenAtlas":
                genatlas_id = ext.find("drugbank:identifier", ns).text
                break
        
        chromosome = target.find("drugbank:polypeptide/drugbank:chromosome-location", ns).text if target.find("drugbank:polypeptide/drugbank:chromosome-location", ns) is not None else None
        cell_location = target.find("drugbank:polypeptide/drugbank:cellular-location", ns).text if target.find("drugbank:polypeptide/drugbank:cellular-location", ns) is not None else None

        data.append([drugbank_id, target_id, source, ext_id, polypeptide_name, gene_name, genatlas_id, chromosome, cell_location])

df = pd.DataFrame(data, columns=["DrugBank ID", "Target ID", "Source", "External ID", "Polypeptide Name", "Gene Name", "GenAtlas ID", "Chromosome", "Cellular Location"])

# df.to_csv("Zaliczeniowe7.csv", index=False, encoding="utf-8")

""" Zadanie8 """

cell_location_counts = df["Cellular Location"].value_counts()
total = cell_location_counts.sum() 
legend_labels = [f"{loc} ({count/total:.1%})" for loc, count in zip(cell_location_counts.index, cell_location_counts)]
colors = plt.colormaps["tab20"](range(len(cell_location_counts)))

plt.figure(figsize=(9, 9))
wedges, _ = plt.pie(
    cell_location_counts, labels=[None] * len(cell_location_counts),
    startangle=140, colors=colors, wedgeprops={'edgecolor': 'black'}
)

plt.legend(wedges, legend_labels, title="Lokalizacja w komórce", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.title("Procentowy udział targetów w różnych częściach komórki")
plt.tight_layout()
# plt.show()

""" Zadanie9 """

tree = ET.parse("drugbank_partial.xml")
root = tree.getroot()
ns = {"db": "http://www.drugbank.ca"}

statuses = {
    "approved": 0,
    "withdrawn": 0,
    "experimental": 0,
    "investigational": 0,
    "veterinary": 0
}

approved_not_withdrawn = 0
for drug in root.findall("db:drug", ns):
    drug_status_list = [cat.text.lower() for cat in drug.findall("db:groups/db:group", ns)]
    if "approved" in drug_status_list:
        statuses["approved"] += 1
    if "withdrawn" in drug_status_list:
        statuses["withdrawn"] += 1
    if "experimental" in drug_status_list:
        statuses["experimental"] += 1
    if "investigational" in drug_status_list:
        statuses["investigational"] += 1
    if "vet_approved" in drug_status_list:
        statuses["veterinary"] += 1
    if "approved" in drug_status_list and "withdrawn" not in drug_status_list:
        approved_not_withdrawn += 1

df_status = pd.DataFrame(statuses.items(), columns=["Status", "Count"])
# df_status.to_csv("Zaliczeniowe9.csv", index=False, encoding="utf-8")

# print(f"Liczba zatwierdzonych leków, które nie zostały wycofane: {approved_not_withdrawn}")

plt.figure(figsize=(9, 9))
colors = plt.colormaps["Set2"](range(len(df_status))) 

wedges, texts, autotexts = plt.pie(
    df_status["Count"], labels=df_status["Status"],
    autopct='%1.1f%%', startangle=140, colors=colors, wedgeprops={'edgecolor': 'black'}
)

for text in texts + autotexts:
    text.set_fontsize(10)

plt.title("Liczba leków według statusu")
plt.tight_layout()
# plt.show()

""" Zadanie10 """

tree = ET.parse("drugbank_partial.xml")
root = tree.getroot()
ns = {"db": "http://www.drugbank.ca"}
interactions = []

for drug in root.findall("db:drug", ns):
    drugbank_id = drug.find("db:drugbank-id", ns).text
    
    for interaction in drug.findall("db:drug-interactions/db:drug-interaction", ns):
        interacting_id = interaction.find("db:drugbank-id", ns).text 
        description = interaction.find("db:description", ns).text  
        interactions.append([drugbank_id, interacting_id, description])

df_interactions = pd.DataFrame(interactions, columns=["DrugBank ID", "Interacting DrugBank ID", "Description"])
# df_interactions.to_csv("Zaliczeniowe10.csv", index=False, encoding="utf-8")

""" Zadanie11 """

def generate_graph_for_gene(gene_name, xml_file="drugbank_partial.xml"):
    tree = ET.parse("drugbank_partial.xml")
    root = tree.getroot()
    ns = {"db": "http://www.drugbank.ca"}

    G = nx.Graph()

    colors = {
        "gene": "red",
        "drug": "blue",
        "product": "green"
    }

    nodes = set()
    edges = []

    for drug in root.findall("db:drug", ns):
        drug_name = drug.find("db:name", ns).text
        drug_id = drug.find("db:drugbank-id", ns).text 

        for target in drug.findall("db:targets/db:target", ns):
            gene = target.find("db:polypeptide/db:gene-name", ns)
            if gene is not None and gene.text == gene_name:
                nodes.add((gene_name, gene_name, "gene"))
                nodes.add((drug_name, drug_name, "drug"))
                edges.append((gene_name, drug_name)) 

                for product in drug.findall("db:products/db:product", ns):
                    product_name = product.find("db:name", ns).text
                    nodes.add((product_name, product_name, "product")) 
                    edges.append((drug_name, product_name)) 

    for node in nodes:
        G.add_node(node[1], type=node[2], color=colors[node[2]])

    G.add_edges_from(edges)

    plt.figure(figsize=(12, 10))
    
    node_colors = [G.nodes[node]["color"] for node in G.nodes]

    pos = nx.spring_layout(G, seed=42, k=0.3, iterations=50)

    nx.draw(G, pos, with_labels=True, node_size=2000, node_color=node_colors, edge_color="gray", font_size=10, font_weight="bold")


    gene_patch = mpatches.Patch(color='red', label='Gen')
    drug_patch = mpatches.Patch(color='blue', label='Substancja lecznicza')
    product_patch = mpatches.Patch(color='green', label='Produkt farmaceutyczny')

    plt.legend(handles=[gene_patch, drug_patch, product_patch], loc='best')

    plt.title(f"Relacje dla genu: {gene_name} - substancje lecznicze i produkty farmaceutyczne", fontsize=16)
    plt.tight_layout()
    plt.show()

# generate_graph_for_gene("F2")

""" Zadanie12 """

url = "https://www.proteinatlas.org/ENSG00000134057.xml"
response = requests.get(url)

if response.status_code == 200:
    tree = ET.ElementTree(ET.fromstring(response.content))
    root = tree.getroot()

    patients_data = []
    
    patients = root.findall('.//patient')
    
    for patient in patients:
        age = patient.find('.//age')
        age_text = age.text if age is not None else "Brak danych"

        gender = patient.find('.//sex')
        gender_text = gender.text if gender is not None else "Brak danych"

        snomed_tissues = patient.findall('.//snomed')
        for tissue in snomed_tissues:
            tissue_description = tissue.attrib.get('tissueDescription', 'Brak opisu')
            tissue_code = tissue.attrib.get('snomedCode', 'Brak kodu')

            tissue_data = [age_text, gender_text, tissue_description, tissue_code]
            patients_data.append(tissue_data)

    df = pd.DataFrame(patients_data, columns=["Age", "Gender", "Tissue_Description", "SNOMED_Code"])

    # df.to_csv("Zaliczeniowe12_Pacjenci.csv", index=False)


""" Zadanie13 """

input_file = "drugbank_partial.xml"
output_file = "drugbank_partial_and_generated.xml"

tree = ET.parse(input_file)
root = tree.getroot()
ns = {'db': 'http://www.drugbank.ca'}

existing_drugs = []
for drug in root.findall("db:drug", ns):
    drug_id = drug.find("db:drugbank-id", ns).text
    existing_drugs.append(drug)

new_drugs = []

for i in range(101, 20001): 
    new_drug = random.choice(existing_drugs) 
    new_drug_copy = ET.Element("drug")

    for element in new_drug:
        new_elem = ET.Element(element.tag)
        if element.tag == "drugbank-id":
            new_elem.text = f"DB{i:05d}"
        else:
            new_elem.text = element.text
        new_drug_copy.append(new_elem)

    new_drugs.append(new_drug_copy)

for new_drug in new_drugs:
    root.append(new_drug)

# tree.write(output_file, encoding="utf-8", xml_declaration=True)


""" Zadanie14 """

# Brak

""" Zadanie15 """

app = FastAPI()
tree = ET.parse("drugbank_partial.xml")
root = tree.getroot()
ns = {'db': 'http://www.drugbank.ca'}

drug_pathways = {}
for drug in root.findall("db:drug", ns):
    drug_id = drug.find("db:drugbank-id", ns).text
    pathways = drug.findall(".//db:pathway", ns) 
    drug_pathways[drug_id] = len(pathways)

@app.get("/")

@app.post("/get_pathway_count/")
async def get_pathway_count(drug_id: str):
    count = drug_pathways.get(drug_id, 0) 
    return {"drug_id": drug_id, "pathway_count": count}

# w terminalu: python -m uvicorn ZadanieZaliczeniowe:app --reload
# serwer ma działać pod http://127.0.0.1:8000/docs
