from flask import Flask, render_template, jsonify, request, Response, url_for, redirect
import pandas as pd
import os
from jinja2 import Template
import pymysql
import numpy as np
import csv
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')


@app.route('/funding-allocation/', methods=['GET','POST'])
def funding_allocation():

  if 'submit_button3' in request.form:
      if request.method == 'POST':
          if os.path.exists("update.csv"):
              os.remove("update.csv")
          try:
              f = request.files['file']
              #print(f.filename)
              f.save(f.filename)
          except:
              return render_template('index.html', result=None)


  # # ÷if 'submit_button1' in request.form or 'submit_button2' in request.form:
  #     if request.method == 'POST':
  #         budget_input = float(request.form['budget_input'])
  #     print(budget_input, "+++++++++++++++++++++++++++++")
  #     ###Input stop file and budget
  #     if os.path.exists("/home/atldotbus/WebModel/input.csv"):
  #         df = pd.read_csv("/home/atldotbus/WebModel/input.csv")
  #     else:
  #         print("No file found")
  #     if budget_input>0:
  #         budget1 = budget_input
  #     else:
  #         budget1 = 0
  #     print(budget1, "===========================================")
  #     # Data pre-processing

      #Checking for errors in input file
       #column name
      df = pd.read_csv("update.csv")
      headerlist=list(df.columns.values)
      try:
          df['StopAbbr'].tolist()
      except:
          return render_template('index.html', errortype='StopAbbr column name')
      try:
          df['StopName'].tolist()
      except:
          return render_template('index.html', errortype='StopName column name')
      try:
          df['FacingDir'].tolist()
      except:
          return render_template('index.html', errortype='FacingDir column name')

      try:
         df['ADA_ACCESS'].tolist()
      except:
          return render_template('index.html', errortype='ADA_ACCESS column name')

      try:
          df['BASE'].tolist()
      except:
          return render_template('index.html', errortype='BASE column name')

      try:
          x=''
          for n in headerlist:
              if n[0:3]=='Ons':
                  x=n
          df[x].tolist()
      except:
          return render_template('index.html', errortype='Ons column name')


      try:
          df['Position'].tolist()
      except:
          return render_template('index.html', errortype='Position column name')




      #column name
      StopAbbr = df['StopAbbr'].tolist()
      ADA_ACCESS = df['ADA_ACCESS'].tolist()
      BASE = df['BASE'].tolist()
      x = ''
      for n in headerlist:
          if n[0:3] == 'Ons':
              x = n
      Ons = df[x].tolist()
      Stop_Type = df['Stop_Type'].tolist()
      Poss = df['Position'].tolist()


      #data type
      remove_row = []
      for i in range(0,len(StopAbbr)):
          if (type(StopAbbr[i]) != int) and (type(StopAbbr[i] != str)):
              remove_row.append(i)
              #return render_template('index.html', errortype='StopAbbr datatype')
      #print(remove_row)
      for i in range(0,len(ADA_ACCESS)):
          if (ADA_ACCESS[i] != "Y") and (ADA_ACCESS[i] != "N"):
              remove_row.append(i)
              #return render_template('index.html', errortype='ADA_ACCESS datatype')
      #print(remove_row)
      for i in range(0,len(BASE)):
          if (BASE[i] != "DIRT") and (BASE[i] != "CONC"):
              remove_row.append(i)
              #return render_template('index.html', errortype='BASE datatype')
      #print(remove_row)
      for i in range(0,len(Ons)):
          try:
              float(Ons[i])
          except:
              remove_row.append(i)
              #return render_template('index.html', errortype='Ons column name')
      #print(remove_row)
      for i in range(0,len(Stop_Type)):
          if (Stop_Type[i] != 'Sign') and (Stop_Type[i] != 'Simme Seat') and (Stop_Type[i] != 'MARTA Bench') and (Stop_Type[i] != 'MARTA Shelter') and (Stop_Type[i] != 'Other Shelter') and (Stop_Type[i] != 'Other Bench') and (Stop_Type[i] != 'Station'):
              remove_row.append(i)
              #return render_template('index.html', errortype='Stop_Type column name'



      remove_row = list(dict.fromkeys(remove_row))
      #print(remove_row)

      remove_row_message = []
      for i in remove_row:
          remove_row_message.append(i + 2)


      # MARTA Stop Data
      Stops1 = df['StopAbbr'].drop(remove_row,axis=0).tolist()
      x = ''
      for n in headerlist:
          if n[0:3] == 'Ons':
              x = n
      ridership1 = df[x].drop(remove_row,axis=0).tolist()
      numStops1 = len(df['StopAbbr'].drop(remove_row,axis=0).tolist())
      n1 = range(numStops1)

      x = ''
      for n in headerlist:
          if n[0:3] == 'Ons':
              x = n
      ridership2 = df[x].drop(remove_row,axis=0).tolist()
      percentile1 = np.percentile(ridership2, 20)
      percentile2 = np.percentile(ridership2, 40)
      percentile3 = np.percentile(ridership2, 60)
      percentile4 = np.percentile(ridership2, 80)
      percentile5 = np.percentile(ridership2, 100)

      for i in range(len(ridership1)):
        if(ridership1[i] >= percentile4): 
          ridership2[i] = 5
        else: 
          if ridership1[i] >= percentile3:
            ridership2[i] = 4
          else: 
            if ridership1[i] >= percentile2:
              ridership2[i] = 3
            else: 
              if ridership1[i] >= percentile1:
                ridership2[i] = 2
              else: 
                ridership2[i] = 1

      




      # Existing amenity score calculation
      amenityscore = []
      for i in n1:
          if df['BASE'].drop(remove_row,axis=0).tolist()[i] == 'DIRT' and df['Stop_Type'].drop(remove_row,axis=0).tolist()[i] == 'Sign':
              amenityscore.append(1)
          elif (df['BASE'].drop(remove_row,axis=0).tolist()[i] == 'CONC' and df['Stop_Type'].drop(remove_row,axis=0).tolist()[i] == 'Sign'):
              amenityscore.append(2)
          elif df['Stop_Type'].drop(remove_row,axis=0).tolist()[i] == 'MARTA Bench' or df['Stop_Type'].drop(remove_row,axis=0).tolist()[i] == 'Other Bench' or \
                  df['Stop_Type'].drop(remove_row,axis=0).tolist()[i] == 'Simme Seat':
              amenityscore.append(3)
          elif (df['Stop_Type'].drop(remove_row,axis=0).tolist()[i] == 'MARTA Shelter' or df['Stop_Type'].drop(remove_row,axis=0).tolist()[i] == 'Other Shelter') and \
                  df['ADA_ACCESS'].drop(remove_row,axis=0).tolist()[i] != 'Y':
              amenityscore.append(4)
          elif (df['Stop_Type'].drop(remove_row,axis=0).tolist()[i] == 'MARTA Shelter' or df['Stop_Type'].drop(remove_row,axis=0).tolist()[i] == 'Other Shelter') and \
                  df['ADA_ACCESS'].drop(remove_row,axis=0).tolist()[i] == 'Y' or df['Stop_Type'].drop(remove_row,axis=0).tolist()[i] == 'Station':
              amenityscore.append(5)
      # Amenity Costs
      # simmeseat_cost = 500
      # simmeseat_install_np_tc = 5500
      # simmeseat_install_sw = 700

      # bench_cost = 5000  # survey and design + bench kit
      # bench_install_sw = 1000  # installation cost on existing sidewalk
      # bench_install_np = 3000  # installation cost on new pad

      # shelter_cost = 13000  # survey and design + shelter kit
      # shelter_install_sw = 6000  # installation cost on existing sidewalk
      # shelter_install_np = 10000  # installation cost on new pad

      # # Calculating cost of amenity needs for each stop
      # need = [[0, 0, 0] for i in n1]
      # for i in n1:
      #     if amenityscore[i] < 3:
      #         if df['BASE'].drop(remove_row,axis=0).tolist()[i] == 'CONC':
      #             ss_cost = simmeseat_cost + simmeseat_install_sw
      #             b_cost = bench_cost + bench_install_sw
      #         else:
      #             ss_cost = simmeseat_cost + simmeseat_install_np_tc
      #             b_cost = bench_cost + bench_install_np
      #         need[i][0] = ss_cost
      #         need[i][1] = b_cost
      #     if amenityscore[i] < 4:
      #         if df['BASE'].drop(remove_row,axis=0).tolist()[i] == 'CONC':
      #             sh_cost = shelter_cost + shelter_install_sw
      #         else:
      #             sh_cost = shelter_cost + shelter_install_np
      #         need[i][2] = sh_cost

      # # Calculation of equity score
      # #equityscore1 = []
      # #for i in range(0, len(Stops1)):
      # #    equityscore1.append(incomeweight * (1 - avgincome1[i] / max(avgincome1)) + nocarweight * (
      # #            nocar1[i] / max(nocar1)) + populationweight * ((population1[i]) / max(population1)))
      # # Greedy heuristic
      # funding = [0] * numStops1
      # fincost = [0] * numStops1
      # indexList=[i[0] for i in sorted(enumerate(ridership1), key=lambda k: k[1], reverse=True)]
      # # indexList = [i[0] for i in sorted(enumerate([a * b for a, b in zip(ridership1, equityscore1)]),
      # #                                   key=lambda k: k[1], reverse=True)]

      # forvars = [
      #     # [need vector, unsolvable included, lower acceptable score, upper acceptable score, ROW not included, need position in list]
      #     [need, False, 0, 4, True, 2],
      #     [need, False, 0, 4, False, 2],
      #     [need, False, 0, 3, True, 1],
      #     [need, False, 0, 3, False, 1],
      #     [need, True, 0, 3, True, 0],
      #     [need, True, 0, 3, False, 0]
      # ]

      # for f in forvars:
      #     for x in n1:
      #         s=indexList[x]
      #         if f[0][s][f[5]] > 0 and budget1 >= f[0][s][f[5]] + row[s] and funding[s] == 0 and (
      #                 f[1] or amenityscore[s] > f[2]) and amenityscore[s] < f[3] and (row[s] != 0 or f[4]):
      #             funding[s] = f[0][s][f[5]] + row[s]
      #             fincost[s] = f[0][s][f[5]]
      #             budget1 -= f[0][s][f[5]] + row[s]


      # for i in n1:
      #     if poss1[i]==0 and amenityscore[i]>=3:
      #         funding[i]=0
      #         fincost[i]=0


      # # Amenity Recommendation
      # amenitytype = []
      # for s in n1:
      #     if fincost[s] == 19000 or fincost[s] == 23000:
      #         amenitytype.append("Shelter")
      #     if fincost[s] == 8000 or (fincost[s] == 6000 and df['BASE'].tolist()[s] == 'CONC'):
      #         amenitytype.append("Bench")
      #     if fincost[s] == 1200 or (fincost[s] == 6000 and df['BASE'].tolist()[s] != 'CONC'):
      #         amenitytype.append("Simme Seat")
      #     if fincost[s] == 0:
      #         amenitytype.append('None')

      # # New amenity score calculation
      # newscore = []
      # for i in n1:
      #     if amenitytype[i] == 'Shelter' and df['ADA_ACCESS'].tolist()[i] != 'Y':
      #         newscore.append(4)
      #     if amenitytype[i] == 'Shelter' and df['ADA_ACCESS'].tolist()[i] == 'Y':
      #         newscore.append(5)
      #     if amenitytype[i] == 'Simme Seat' or amenitytype[i] == 'Bench':
      #         newscore.append(3)
      #     if amenitytype[i] == 'None':
      #         newscore.append(amenityscore[i])

      # Output exporting to CSV
      ridershipcsv = [int(float(n)) for n in ridership1]

      try:
          connection = pymysql.connect(host='database-2.c690vw2rmxwz.us-east-2.rds.amazonaws.com',
                             user='root',
                             password='qjfwk100djr!',
                             charset='utf8mb4',
                             database='atldotmarta',
                             port=3306,
                             cursorclass=pymysql.cursors.DictCursor)
      except:
          return render_template('index.html', errors='connection')


      df=df.drop(remove_row,axis=0)
      df2=pd.DataFrame()
      df2['ADA_ACCESS']=df['ADA_ACCESS']
      df2['StopAbbr']=df['StopAbbr']
      df2['StopName']=df['StopName']
      df2['FacingDir']=df['FacingDir']
      df2['Position']=df['Position']
      csv_data = df2.values.tolist()
      with connection.cursor() as cursor: 
        for index, row in enumerate(csv_data):

          # update ATLDOT table
          sql_select = "SELECT 1 FROM atldot_bus_table WHERE stop_id = " + str(row[1])
          cursor.execute(sql_select)
          result = cursor.fetchall()
          if len(result)!=0:
              sql_update = "UPDATE atldot_bus_table SET ada_access = '"+ str(row[0])+ "', facing_dir = '"+ str(
                  row[3])+"', position = '"+ str(row[4])+"', ridership_data = "+str(
                  ridershipcsv[index])+", ridership_quintile = "+str(ridership2[index])+", stop_name = '"+str(
                  row[2])+"', tier = "+str(amenityscore[index])+" WHERE stop_id = "+str(row[1])
              cursor.execute(sql_update)
          else:
              sql_insert = "INSERT INTO atldot_bus_table (ada_access, facing_dir, position, ridership_data, ridership_quintile, stop_name, tier, stop_id) VALUES ('"+str(row[0])+"', '"+str(row[3])+"', '"+str(row[4])+"', "+str(ridershipcsv[index])+", "+str(ridership2[index])+", '"+str(row[2])+"', "+str(amenityscore[index])+", "+str(row[1])+")"
              cursor.execute(sql_insert)

          # update MARTA table
          sql_select = "SELECT 1 FROM marta_bus_table WHERE stop_id = " + str(row[1])
          cursor.execute(sql_select)
          result = cursor.fetchall()
          if len(result) != 0:
              sql_update = "UPDATE marta_bus_table SET ada_access = '" + str(row[0]) + "', facing_dir = '" + str(
                  row[3]) + "', position = '" + str(row[4]) + "', ridership_data = " + str(
                  ridershipcsv[index]) + ", ridership_quintile = " + str(
                  ridership2[index]) + ", stop_name = '" + str(
                  row[2]) + "', tier = " + str(amenityscore[index]) + " WHERE stop_id = " + str(row[1])
              cursor.execute(sql_update)
          else:
              sql_insert = "INSERT INTO marta_bus_table (ada_access, facing_dir, position, ridership_data, ridership_quintile, stop_name, tier, stop_id) VALUES ('" + str(
                  row[0]) + "', '" + str(row[3]) + "', '" + str(row[4]) + "', " + str(
                  ridershipcsv[index]) + ", " + str(ridership2[index]) + ", '" + str(row[2]) + "', " + str(
                  amenityscore[index]) + ", " + str(row[1]) + ")"
              cursor.execute(sql_insert)

              #sql2= "INSERT INTO atldot_bus_table (ada_access, facing_dir, position, ridership_data, ridership_quintile, stop_name, tier, stop_id) VALUES ('"+str(row[0])+"', '"+str(row[3])+"', '"+str(row[4])+"', "+str(ridershipcsv[index])+", "+str(ridership2[index])+", '"+str(row[2])+"', "+str(amenityscore[index])+", "+str(row[1])+")"


        # df2['da_access'] = csv_data[4]
        # ##isthisright
        # #df2['create_by'] = 'gt'
        # df2['facing_dir'] = csv_data[2]
        # #df2['modify'] = 
        # #df2['pk'] = 
        # df2['position'] = csv_data[11]
        # df2['ridership_data'] = [int(float(n)) for n in ridership1]
        # df2['ridership_quintile'] = 
        # df2['Stop_ID'] = Stops1;
        # df2['stop_name'] = csv_data[1];
        # df2['tier'] = amenityscore
      connection.commit()
      cursor.close()

      if os.path.exists("update.csv"):
          os.remove("update.csv")


        # cursor.execute('INSERT INTO testcsv(names, \
        #   classes, mark )' \
        #   'VALUES("%s", "%s", "%s")', 




      # df2['Stop_ID'] = Stops1
      # df2['Funding'] = funding
      # df2['Amenity_Type'] = amenitytype
      # df2['Current_Score'] = amenityscore
      # df2['New_Score'] = newscore
      # df2['Daily_Ridership'] = [int(float(n)) for n in ridership1]

      ###### Summary ######
      #total ridership impacted, #total funding, #average new amenity score
      



      #print(remove_row_message)

  
      return render_template('index.html',row_list=remove_row_message,result=1)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
if __name__ == '__main__':
  app.run(debug=True)