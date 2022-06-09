from msilib.schema import MsiAssemblyName
from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import MinMaxScaler
app = Flask(__name__)
model = pickle.load(open('house_price_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = MinMaxScaler()
@app.route("/predict", methods=['POST'])
def predict():
    
    if request.method == 'POST':
        mssub = request.form['MSSubclass']
        if(mssub=="1-STORY 1946 & NEW ALL"):
            mssub=20
        elif(mssub=="1-STORY 1945 & OLDER"):
            mssub=30
        elif(mssub=="1-STORY W/FINISHED ATTIC ALL"):
            mssub=40
        elif(mssub=="1-1/2 STORY-UNFINISHED ALL AGES"):
            mssub=45
        elif(mssub=="1- 1/2 STORY FINISHED ALL AGES"):
            mssub=50
        elif(mssub=="2-STORY 1946 & NEWER"):
            mssub=60
        elif(mssub=="2-STORY 1945 & OLDER"):
            mssub=70
        elif(mssub=="2-1/2 STORY ALL AGES"):
            mssub=75
        elif(mssub=="SPLIT OR MULTI-LEVEL"):
            mssub=80
        elif(mssub=="SPLIT FOYER"):
            mssub=85
        elif(mssub=="DUPLEX - ALL STYLES AND AGES"):
            mssub=90
        elif(mssub=="1-STORY PUD Planned unit development-1946 & NEWER"):
            mssub=120
        elif(mssub=="1-1/2 STORY PUD -ALL AGES"):
            mssub= 150  
        elif(mssub=="2-STORY PUD-1946 & NEWER"):
            mssub=160
        elif(mssub=="PUD-MULTILEVEL-INCL SPLIT LEV/FOYER"):
            mssub=180
        elif(mssub=="2 FAMILY CONVERSION -ALL AGES"):
            mssub=190
        # convert mssub to scaled value
        mssub_scale=(mssub-20)/170

        mszone=request.form["MSZoning"]
        if(mszone=="Commercial"):
            mszone= 4
        elif(mszone=="Floating Village Residential"):
            mszone=0
        elif(mszone=="Residential High Density"):
            mszone=1

        elif(mszone=="Residential Low Density"):
            mszone=2

        elif(mszone=="Residential Medium Density"):
            mszone=3
        # convert mszone to scale value
        msz_scale=(mszone)/4

        niegh=request.form['Niegbourhood']
        if(niegh=="Blmngtn"):
             neigh=0
        elif(niegh=="BrDale"):
             neigh=1
        elif(niegh=="Brkside"):
             neigh=2
        elif(niegh=="ClearCr"):
             neigh=3
        elif(niegh=="Collgcr"):
             neigh=4
        elif(niegh=="Crawfor"):
             neigh=5
        elif(niegh=="Edwards"):
             neigh=6
        elif(niegh=="Gilbert"):
             neigh=7
        elif(niegh=="IDOT"):
             neigh=8
        elif(niegh=="MeadowV"):
             neigh=9
        elif(niegh=="Mitchel"):
             neigh=10
        elif(niegh=="NoRidge"):
             neigh=13
        elif(niegh=="Nwames"):
             neigh=12
        elif(niegh=="OldTown"):
             neigh=15
        elif(niegh=="SWISU"):
             neigh=17
        elif(niegh=="Sawyer"):
             neigh=18
        elif(niegh=="SawyerW"):
             neigh=19
        elif(niegh=="Somerst"):
             neigh=20
        elif(niegh=="StoneBr"):
             neigh=21
        elif(niegh=="vnk"):
             neigh=16
        elif(niegh=="timb"):
             neigh=22
        elif(niegh=="Nridht"):
             neigh=14
        else:
             neigh=11
        neigh_scale=neigh/22
        
        
        overallqual=request.form['OverallQual']
        if(overallqual=="ten"):
           overallqual=10
        elif(overallqual=="nine"):
           overallqual=9
        elif(overallqual=="eight"):
               overallqual=8
        elif(overallqual=="sev"):
           overallqual=7
        elif(overallqual=="six"):
           overallqual=6
        elif(overallqual=="five"):
           overallqual=5
        elif(overallqual=="four"):
           overallqual=4
        elif(overallqual=="three"):
           overallqual=3
        elif(overallqual=="two"):
           overallqual=2
        else:
           overallqual=1
        # set overallquality to scaled value
        overq_scale=(overallqual-1)/(9)

            

        YearRemod=int(request.form['YearRemoAdd'])
        yearremodel_s = YearRemod/58

        roofsty=request.form['RoofStyle']
        
     # set conditional for roofstyle
        if(roofsty=="gable"):
             roofsty=0
             
        elif(roofsty=="Hip"):
             roofsty=1
        else:
             roofsty=2
        roof_scale=roofsty/2



        bstq=request.form['BsmtQual']
        if(bstq=="ex"):
             bstq=0
        elif(bstq=="Gd"):
             bstq=2
        elif(bstq=="TA"):
             bstq=4
        
        elif(bstq=="Fa"):
             bstq=1
        else:
             bstq=3
        bstscale=bstq/4
       
       
        #basement exposure  
        bste=request.form['BsmtExposure']
        if(bste=="gd"):
             bste=1
        elif(bste=="Av"):
             bste=0
        elif(bste=="mn"):
             bste=3
        
        elif(bste=="No"):
             bste=4
        else:
             bste=2
        bste_scale=bste/4
       

        # heating quality
        heatqc=request.form['HeatingQC']
        if(heatqc=="Exc"):
             heatqc=0
        elif(heatqc=="Good"):
             heatqc=2
        elif(heatqc=="Ta"):
             heatqc=4
        
        elif(heatqc=="Fair"):
             heatqc=1
        else:
             heatqc=3
        heatqcscale=bstq/4
       
        # central air conditioning
        centralair=request.form['CentraAir']
        if(centralair=="Y"):
             centralair=1
        else:
              centralair=0 
        # First floor is square feet   
        firsflr=float(request.form['1stFlrSF'])
        firlog=np.log(firsflr)
        firf_s=(firlog-5.8)/(8.5-5.8)
        grliv=float(request.form['GrLivArea'])
        grlivlog=np.log(grliv)
        grliv_s=(grlivlog-5.8)/(8.6-5.8)
        bsmtfullb=int(request.form['BsmtFullBath'])
        bsf_scale=bsmtfullb/3
        # kitchen quality
        kitchenq=request.form['kitcheQual']
        if(kitchenq=="Goodd"):
             kitchenq=2
        elif(kitchenq=="Exce"):
             kitchenq=1
        elif(kitchenq=="Tav"):
             kitchenq=3
        else:
             kitchenq=0
        kitchenq_scale=kitchenq/3
         
        # no of fireplaces
        fireplc=int(request.form['Fireplaces'])
        fireplc_scale=fireplc/3
        # fire place quality
        fireplcq=request.form['FireplaceQu']
        if(fireplcq=="Exce"):
             fireplcq=0
        
        elif(fireplcq=="Goodd"):
             fireplcq=2
        
        elif(fireplcq=="Tav"):
             fireplcq=5
        elif(fireplcq=="fair"):
             fireplcq=1
        elif(fireplcq=="Po"):
             fireplcq=4
        else:
             fireplcq=3
        fireq_scale=fireplcq/5 
        # garage type
        garagtype=request.form['GarageType']
        if(garagtype=="attchd"):
             garagtype=0
         
        elif(garagtype=="Basment"):
             garagtype= 1
        elif(garagtype=="Detchd"):
             garagtype=3
        elif(garagtype=="builtIn"):
             garagtype=2
        else:
             garagtype=4
        garatype_scale=garagtype/4

        garagfini=request.form['GarageFinish']
        if(garagfini=="Fin"):
             garagfini=0
        elif(garagfini=="RF"):
             garagfini=1
        elif(garagfini=="UF"):
             garagfini=3
        else:
             garagfini= 2
        garagf_scale=garagfini/3 

        garagcar=int(request.form['GarageCars'])
        garagecar_scale=garagcar/3

        pavdrive=request.form['PavedDrive']
        if(pavdrive=="Y"):
             pavdrive=2
        
        elif(pavdrive=="N"):
             pavdrive=0
        else:
             pavdrive=1
        pave_drive_s=pavdrive/2
        # sale condition
        salecondi=request.form['SaleCondition']
        if(salecondi=="normal"):
             salecondi=2
        elif(salecondi=="Abnormal"):
             salecondi=0
        elif(salecondi=="Partial"):
             salecondi=3
        elif(salecondi=="Family"):
             salecondi=1
        else:
             salecondi=4
        salecon_scale=salecondi/4
        prediction=model.predict([[mssub_scale,msz_scale,neigh_scale,overq_scale,yearremodel_s,roof_scale,
        bstscale,bste_scale,heatqcscale,centralair,firf_s,grliv_s,bsf_scale,kitchenq_scale,
        fireplc_scale,fireq_scale,garatype_scale,garagf_scale,garagecar_scale,
        pave_drive_s,salecon_scale]])
        output=np.exp(round(prediction[0],3))
        if output < 0:
             return render_template("index.html",prediction_text="Sorry price is not available")
        else:
             return render_template("index.html",prediction_text="The price of this house is around ${}".format(output))
    else:
         return render_template("index.html")
     

        
if __name__=="__main__":
    app.run(debug=True)

