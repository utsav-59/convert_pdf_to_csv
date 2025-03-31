from flask import Flask,request,jsonify,send_file
import tabula
import re
import pandas as pd
from time import time

app = Flask(__name__)

@app.route('/')
def homepage():
    return 'PDF to CSV converter.'

@app.route("/v1/pdftocsv",methods=["POST"])
def pdf_to_csv():
    try:
        pdf_file = request.files['file']
        if not pdf_file:
            raise ValueError("PDF file is missing!")
        if not pdf_file.filename.endswith(".pdf"):
            raise TypeError("Only PDF file is allowed.")
        
        current_time = time()

        tabula.convert_into(pdf_file, f"{current_time}.csv", pages= "all", output_format="csv")

        data = pd.read_csv(f"{current_time}.csv")

        iterator = 0 
        total_rows = data.shape[0]
        drop_list = []

        index = iterator + 1

        # Loop through the rows and add the narration to trail rows if date is empty
        while (iterator < total_rows-1) and (index < total_rows-1):
            if pd.isna(data['Date'][index]) and not re.search(r'summary|statement', str(data['Narration'][index]), re.IGNORECASE):
                data.loc[iterator, 'Narration'] = str(data.loc[iterator, 'Narration']) + str(data.loc[index, 'Narration'])
            else:
                iterator=index
            index+=1


        # For removing rows which has no value for Date column
        iterator = 0 

        while iterator < total_rows:
            if pd.isna(data['Date'][iterator]):
                drop_list.append(iterator)
            iterator+=1

        data.drop(index=drop_list, inplace = True)
        data.to_csv(f"{current_time}.csv",index=False)
        return send_file(f"{current_time}.csv",as_attachment=True)

    except ValueError as e:
        return jsonify({"error":str(e)}),400
    except TypeError as e:
        return jsonify({"error":str(e)}),400
    except Exception as e:
        return jsonify({"error":str(e)}),500

if __name__ == '__main__':
    app.run() 

