import json
import re
from flask import Flask,render_template,request,redirect, url_for, flash
import sqlite3 as sql

app=Flask(__name__)
app.secret_key="123"

conn=sql.connect("thirukuural_1.sqlite")
cursor = conn.cursor()
Table_name="Thirukkural"
Thirukkural=cursor.fetchall()

@app.route('/', methods= ['POST','GET'])
def Index():
    # try:a
        with sql.connect("thirukuural_1.sqlite") as conn:
            cursor = conn.cursor()
            if request.method=='POST':
                Title= request.form["section"]   
                count= request.form["count"]
            
                Table_name="Thirukkural"
                cursor.execute(f"SELECT * FROM {Table_name} WHERE sectionname='{Title}' and sectioncount='{count}'")
                Thirukkural=cursor.fetchall()
                
                cursor.execute(f"SELECT * FROM {Table_name}")
                Thirukkural_1=cursor.fetchall()
                rows=[]
                for row in Thirukkural_1:
                    rows.append(row[2])
                id=rows[-1]
                if Thirukkural:
                    flash("Duplicate Found!","success")
                else:
                    cursor.execute("INSERT INTO Thirukkural VALUES(?,?,?)",(Title,count,id+1))
                    if request.form.get("submit"):
                        flash("Insert successfully","success")

            conn.row_factory =sql.Row
            cur = conn.cursor()
            Table_name="Thirukkural"
            cur.execute(f"SELECT * FROM {Table_name} ORDER BY sectionid DESC")
            rows = cur.fetchall()
            conn.commit()
                
        return render_template("index.html",rows=rows)

    # except Exception as e:
    #     conn.rollback()
    #     msg="error in insert operation"           
    #     return render_template("index.html",rows=e)
    

@app.route('/adhigaram', methods= ['POST','GET'])
def adhigaram():
    try:
        with sql.connect("thirukuural_1.sqlite") as conn:
            cursor = conn.cursor()
            if request.method=='POST':
                Title= request.form["adhigaram"]
                section = request.form["section"]
                Table_name="adhigaram"
                cursor.execute(f"SELECT * FROM {Table_name} WHERE adhigaram ='{Title}' and section='{section}'")
                Thirukkural=cursor.fetchall()
                cursor.execute(f"SELECT * FROM {Table_name}")
                Thirukkural_1=cursor.fetchall()
                rows=[]
                for row in Thirukkural_1:
                    rows.append(row[2])
                id=rows[-1]
                if Thirukkural:
                    flash("Duplicate Found!","success")
                else:
                    cursor.execute("INSERT INTO adhigaram VALUES(?,?,?)",(Title,section,id+1))
                    if request.form.get("submit"):
                        flash("Insert successfully","success")

            conn.row_factory =sql.Row
            cur = conn.cursor()
            Table_name="adhigaram"
            cur.execute(f"SELECT * FROM {Table_name} ORDER BY adhigaramid DESC")
            rows = cur.fetchall()
            conn.commit()
            Table_name_1="Thirukkural"
            cur.execute(f"SELECT * FROM {Table_name_1}")
            rows_1 = cur.fetchall()
            conn.commit()

        return render_template("adhigaram.html",rows={
            "rows":rows,
            "rows_1":rows_1
        })

    except Exception as e:
        conn.rollback()
        msg="error in insert operation"
        return render_template("adhigaram.html",rows=e)

    
@app.route('/<int:id>', methods= ['POST','GET'])
def update(id):
    with sql.connect("thirukuural_1.sqlite") as conn:
        conn.row_factory =sql.Row
        cur = conn.cursor()
        Table_name="Thirukkural"
        cur.execute(f"SELECT * FROM {Table_name}  WHERE sectionid = {id}")
        rows = cur.fetchone()
        conn.commit()
        
        cur.execute(f"SELECT * FROM {Table_name} ORDER BY sectionid DESC")
        another_row=cur.fetchall()
        conn.commit()

        if request.method == 'POST':
            update_name= request.form["section"]
            update_count= request.form["count"]
            

# remove_dublicate
            conn= sql.connect("thirukuural_1.sqlite")
            cur = conn.cursor()
            Table_name="Thirukkural"
            cur.execute(f"SELECT * FROM {Table_name}  WHERE sectionname = '{update_name}' and sectioncount='{update_count}'  and  sectionid != {id}")
            find_duplicate=cur.fetchall()
            conn.commit()

            if find_duplicate:
                flash("Duplicate found","success")
            
            else:
                cur.execute(f"UPDATE Thirukkural SET sectionname='{update_name}' , sectioncount='{update_count}' WHERE sectionid = {id}",)
                conn.commit()
                if request.form.get("update"):
                    flash("Updated successfully","success")
            return redirect (url_for("Index"))

    return render_template("edit.html",rows_1=dict(rows),rows=another_row)

@app.route('/adhigaram/<int:id>', methods= ['POST','GET'])
def update_1(id):
    output = {}
    with sql.connect("thirukuural_1.sqlite") as conn:
        conn.row_factory =sql.Row
        cur = conn.cursor()
        if request.method == 'POST':
            update_name= request.form["adhigaram"]
            update_section= request.form["section"]
            conn= sql.connect("thirukuural_1.sqlite")
            cur = conn.cursor()
            Table_name="adhigaram "
            cur.execute(f"SELECT * FROM {Table_name}  WHERE adhigaram = '{update_name}' and section= '{update_section}' and  adhigaramid != {id}")
            find_duplicate=cur.fetchall()
            conn.commit()
            if find_duplicate:
                flash("Duplicate found","success")
            else:
                cur.execute(f"UPDATE adhigaram SET adhigaram='{update_name}' , section='{update_section}' WHERE adhigaramid = {id}")
                conn.commit()
                if request.form.get("update"):
                    flash("Updated successfully","success")
            
            return redirect (url_for("adhigaram"))

        Table_name="adhigaram"
        cur.execute(f"SELECT * FROM {Table_name}  WHERE adhigaramid = {id}")
        athigaram_data = cur.fetchone()
        conn.commit()

        Table_name_1="Thirukkural"
        cur.execute(f"SELECT * FROM {Table_name_1}")
        thirukkural_results = cur.fetchall()
        conn.commit()

        cur.execute(f"SELECT * FROM {Table_name} ORDER BY adhigaramid DESC")
        adhigaram_results = cur.fetchall()
        conn.commit()

        output.update({'page_data': dict(athigaram_data)})
        output.update({'thirukkural_results': thirukkural_results})
        output.update({'adhigaram_results': adhigaram_results})
    
    return render_template("edit_1.html",data=output)

@app.route('/delete/<int:id>', methods= ['POST','GET'])
def delete(id):
    
    with sql.connect("thirukuural_1.sqlite") as conn:
        cur = conn.cursor()
        cur.execute(f"DELETE FROM Thirukkural WHERE sectionid = {id}")
        conn.commit()
        return redirect (url_for("Index"))

@app.route('/adhigaram/deleted/<int:id>', methods= ['POST','GET'])
def deleted(id):
    with sql.connect("thirukuural_1.sqlite") as conn:
        cur = conn.cursor()
        cur.execute(f"DELETE FROM adhigaram WHERE adhigaramid = {id}")
        conn.commit()
        return redirect (url_for("adhigaram"))

if __name__== "__main__":
    app.run(debug=True)
