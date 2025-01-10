from flask import Flask,request,jsonify
from tabula import read_pdf
import csv

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
        
        # Add password while reading the PDF file
        # reading the PDF file
        tables = read_pdf(pdf_file,pages="all",multiple_tables=True,output_format="dataframe")
        # print(type(tables))
        if tables:
            # pd.DataFrame.to_csv(self=tables)
            csv_file_path = "name.csv"
            with open(csv_file_path, 'w', newline='') as file:
                csv_writer = csv.writer(file)
                # print(tables)
                # Excpet header all hte other lines are not shown in csv file
                csv_writer.writerows(tables)

            print(f"Data has been written to {csv_file_path}")
            return jsonify({"message":"sucesss"}),200
        else: 
            raise ValueError("No table found from PDF.")
        
    except ValueError as e:
        return jsonify({"error":str(e)}),400
    except TypeError as e:
        return jsonify({"error":str(e)}),400
    except Exception as e:
        return jsonify({"error":str(e)}),500

if __name__ == '__main__':
    app.run() 
    # Use Gunicorn and docker for deploying 
