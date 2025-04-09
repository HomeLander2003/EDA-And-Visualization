import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s [line %(lineno)d] ')

class loadfile:
    
    def __init__(self,file_path):
        self.filepath=file_path
        self.file=None
        
    def load(self):
        
        if os.path.isfile(self.filepath):
            print(f"file executed successfully...........")
            try:
                self.file=pd.read_csv(self.filepath)
                print(self.file)
            
            except Exception as e:
                logging.error(f"error occured: {e}")
                
        else:
            logging.error(f"This {self.filepath} file path not correct")
            

class cleanfile(loadfile):
    
    def clean(self):
        if self.file is not None:
            try:
                print(self.file.isnull().sum())  # no null values found
                print(self.file.duplicated().sum()) # no duplicate found
                
                column_to_drop=["Job_Completed","Job_Duration_Days","Project_Type"]  # dropping column
                
                for col in column_to_drop:
                    if col in self.file.columns:
                        self.file.drop(columns=col,axis=1,inplace=True)
                        logging.info(col + " dropped.........")
                    else:
                        logging.warning("columns not found.......")
                    
                print(self.file.columns)
                
            except Exception as e:
                logging.error(f"error occured: {e}")
                
class savefile(cleanfile):
    
    def save(self,filename):
        
        if self.file is not None:
            try:
                save_path=os.path.join(os.getcwd(),filename)  # saving in current directory but can be save in different dir too
                self.file.to_csv(save_path,index=False)
                logging.info("file saved successfulyy.......")
                
            except Exception as e:
                logging.error(f"error occured{e}")
                
        else:
            logging.error("Unable to save file..........")
            
class analyzefile(cleanfile):
    
    def analyze(self):
        
        if self.file is not None:
            
            try:
                
                print(self.file.describe())
                
                #   Exploratory Data Analysis (EDA)
                
                gr1=self.file.groupby("Job_Category")["Job_Category"].count()
                print(gr1)
                
                gr2=self.file.groupby("Platform")["Job_Category"].value_counts().reset_index()
                print(gr2)
                
                gr3=self.file.groupby("Platform")["Client_Region"].value_counts().reset_index()
                print(gr3)
                
                gr4=self.file.groupby("Job_Category")[["Rehire_Rate","Job_Success_Rate"]].mean()
                print(gr4)
                print(gr4.ndim)
                
                gr5=self.file.groupby("Experience_Level")["Hourly_Rate"].mean().reset_index()
                print(gr5)
                
                cols=self.file[["Earnings_USD","Job_Success_Rate","Client_Rating","Rehire_Rate"]]
                col=cols.corr()
                print(col)
                
                return gr1,gr2,gr3,gr4,gr5,col
            
            except Exception as e:
                logging.error(f"error occured {e}")
        
                     
        else:
            logging.error("Unable to analyze file..........") 
            

class visualizefile(analyzefile):
    
    def pie1(self,gr1):
        
        plt.figure(figsize=(10,6))
        plt.title("JOB CATEGORY",color="purple",weight="bold")
        plt.pie(gr1.values,autopct='%1.1f%%',textprops={"weight":"bold","fontsize":12})
        plt.legend(labels=gr1.index,shadow=True,loc="upper right",bbox_to_anchor=(1.4,1))
        
        plt.savefig(r"pie.png", dpi=300, bbox_inches="tight")

        plt.show()
        
    def subplot1(self,gr2,gr3):
        
        plt.figure(figsize=(14, 5))  

        plt.subplot(1, 2, 1) 
        plt.title("JOB ACC TO PLATFORMS", color="purple", weight="bold")
        sns.barplot(x="Platform", y="count", hue="Job_Category", data=gr2)
        plt.legend(title="Job_Categories", loc="upper left", bbox_to_anchor=(1, 1), shadow=True)

        plt.subplot(1, 2, 2)  
        plt.title("JOB ACC TO REGIONS", color="purple", weight="bold")
        sns.barplot(x="Platform", y="count", hue="Client_Region", data=gr3)
        plt.legend(title="Client_Regions", loc="upper left", bbox_to_anchor=(1, 1), shadow=True)  # Adjusted title
        
        plt.tight_layout()  
        plt.savefig(r"subplot.png", dpi=300, bbox_inches="tight")
        
        plt.show()
    
    def barplot1(self,gr4):
        
        plt.figure(figsize=(10,6))
        
        plt.title("JOB SUCCESS AND REHIRING RATE")
        plt.ylabel("Job_Rate")
        sns.barplot(x="Job_Category",y="Job_Success_Rate",data=gr4,label="Job_Success_Rate")
        sns.barplot(x="Job_Category",y="Rehire_Rate",data=gr4,label="Rehire_Rate")
        plt.legend(shadow=True,loc="upper right",bbox_to_anchor=(1.05,1.1))
        
        plt.tight_layout()
        plt.savefig(r"barplot1.png", dpi=300, bbox_inches="tight")
        
        plt.show()
        
    
    def barplot2(self, gr5):
        plt.figure(figsize=(10,6))  

        sns.barplot(x="Experience_Level", y="Hourly_Rate", data=gr5, palette="crest")

        plt.title("HOURLY RATE BY EXPERIENCE LEVEL")
        plt.ylabel("Job_Rate")

        # Adding vqalues above the Bar
        for i, val in enumerate(gr5["Hourly_Rate"].values):
            plt.text(i, val + 0.5, f"{val:.2f} $", ha="center", va="bottom", fontsize=10, color="black")

        plt.tight_layout()
        plt.savefig(r"barplot2.png", dpi=300, bbox_inches="tight")
        
        plt.show()
        
        
    def heatmap(self,col):
         
        plt.figure(figsize=(10,6))
        plt.title("Correlation Matrix")
        
        sns.heatmap(col,cmap="crest",annot=True,linewidths=0.01)
        plt.tight_layout()
        plt.savefig(r"heatmap.png", dpi=300, bbox_inches="tight")
        
        plt.show()
        
        
    def hist(self):
        column = ["Earnings_USD", "Hourly_Rate"]
        
        plt.figure(figsize=(12, 5))  

        for i, col in enumerate(column):  
            plt.subplot(1, 2, i + 1)  
            sns.histplot(self.file[col], bins=12, color="green", edgecolor="black", linewidth=2, kde=True)
            plt.title(f"Distribution of {col}")
            plt.xlabel(col)
            plt.ylabel("Count")
       
        plt.tight_layout() 
        plt.savefig("hist.png",dpi=300,bbox_inches="tight0") 
        plt.show()

       
c=visualizefile(r"freelancer_earning_mod.csv")
c.load()
c.clean()
# c.save("freelancer_earning_mod.csv")
gr1,gr2,gr3,gr4,gr5,col=c.analyze()
# c.pie1(gr1)
# c.subplot1(gr2,gr3)
c.barplot1(gr4)
# c.barplot2(gr5)
# c.heatmap(col)
# c.hist()
        
