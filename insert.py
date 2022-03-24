# @app.route('/', methods= ['POST','GET'])
# def Index():
#     try:
#         with sql.connect("thirukuural_1.sqlite") as conn:
#             cursor = conn.cursor()
#             if request.method=='POST':
#                 Title= request.form["section"]
#                 count= request.form["count"]
#                 Table_name="Thirukkural"
#                 cursor.execute(f"SELECT * FROM {Table_name} WHERE sectionname='{Title}'")
#                 Thirukkural=cursor.fetchall()
#                 # if Thirukkural:
#                 #     flash("Duplicate Found!","success")
#                 # else:   
#                 rows=[]
#                 # conn=sql.connect("thirukuural_1.sqlite")
#                 # cursor = conn.cursor()
#                 # cursor.execute(f"SELECT * FROM {Table_name}'")
#                 # Thirukkural_1=cursor.fetchall()
#                 for row in Thirukkural:
#                     rows.append(row[2])
#                 id=rows[-1]
#                 cursor.execute("INSERT INTO Thirukkural VALUES(?,?,?)",(Title,count,id+1))
#                 if request.form.get("submit"):
#                     flash("Insert successfully","success")

#             conn.row_factory =sql.Row
#             cur = conn.cursor()
#             Table_name="Thirukkural"
#             cur.execute(f"SELECT * FROM {Table_name} ORDER BY sectionid DESC")
#             rows = cur.fetchall()
#             conn.commit()
            
#         return render_template("index.html",rows=rows)

#     except Exception as e:
#         conn.rollback()
#         msg="error in insert operation"        
#         return render_template("index.html",rows=e)

import sqlite3 as sql

with sql.connect("thirukuural_1.sqlite") as conn:
        conn.row_factory =sql.Row
        cur = conn.cursor()
        Table_name="Thirukkural"
        cur.execute(f"SELECT * FROM {Table_name}  WHERE sectionid = 20" )
        rows = cur.fetchone()
        conn.commit()


        cur.execute(f"SELECT * FROM {Table_name}  WHERE sectionid = 20" )
        find_duplicate=cur.fetchall()
        conn.commit()
        for i in find_duplicate:
            for y in i:
                print(y)