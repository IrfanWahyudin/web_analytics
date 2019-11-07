from app.models import Titanic
from app import db
import pandas as pd

class Upload:
    def __init__(self):
        return
    
    def upload_to_db(self, filename):
        df = pd.read_csv(filename)
        bulk = list()
        for idx, rows in df.iterrows():
            titanic = Titanic(PassengerId=rows['PassengerId'],\
                            Survived=rows['Survived'],\
                            Pclass=rows['Pclass'],\
                            Name=rows['Name'],\
                            Sex=rows['Sex'],\
                            Age=rows['Age'],\
                            SibSp=rows['SibSp'],\
                            Parch=rows['Parch'],\
                            Ticket=rows['Ticket'],\
                            Fare=rows['Fare'],\
                            Cabin=rows['Cabin'],\
                            Embarked=rows['Embarked'])

            db.session.add(titanic)
        
        db.session.commit()

class TitanicChart():
    def __init__(self):
        return
    
    def titanic_chart1(self):
        titanic = pd.read_sql_query(db.session.query(Titanic).statement, db.session.bind)
        df_group_survived = pd.DataFrame(titanic.groupby(by=['Survived', 'Sex'])['PassengerId'].count())

        df_group_survived = df_group_survived.reset_index()
        name1 = 'Not Survived'
        xtrace1 = df_group_survived.loc[(df_group_survived['Survived']==0),['Sex']]
        ytrace1 = df_group_survived.loc[(df_group_survived['Survived']==0),['PassengerId']]
        xtrace1 = xtrace1.Sex.tolist()
        ytrace1 = ytrace1.PassengerId.tolist()

        name2 = 'Survived'
        xtrace2 = df_group_survived.loc[(df_group_survived['Survived']==1),['Sex']]
        ytrace2 = df_group_survived.loc[(df_group_survived['Survived']==1),['PassengerId']]
        xtrace2 = xtrace2.Sex.tolist()
        ytrace2 = ytrace2.PassengerId.tolist()

        print(ytrace1, xtrace1)
        return xtrace1, ytrace1, xtrace2, ytrace2, name1, name2

    def titanic_chart2(self):
        return
