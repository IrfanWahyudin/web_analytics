from app.models import Titanic
from app import db
import pandas as pd

class Upload:
    def __init__(self):
        return

    def upload_to_db(self, filename):
        df = pd.read_csv(filename)
    #     ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp',
    #    'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked'
        for idx, rows in df.iterrows():
            titanic = Titanic(PassengerId=rows['PassengerId'],\
                                Survived=rows['Survived'],\
                                Pclass=rows['Pclass'],\
                                Name=rows['Name'],\
                                Sex=rows['Sex'],\
                                Age=rows['Age'],\
                                Parch=rows['Parch'],\
                                Ticket=rows['Ticket'],\
                                Fare=rows['Fare'],\
                                Cabin=rows['Cabin'],\
                                Embarked=rows['Embarked'])
            db.session.add(titanic)
        db.session.commit()

class TitanicChart:
    def __init__(self):
        pass

    def titanic_chart(self):
        #Bar Chart
        titanic = pd.read_sql_query(db.session.query(Titanic).statement, db.session.bind)
        df_group_survived = pd.DataFrame(titanic.groupby(by=['Survived', 'Sex'])['PassengerId'].count())
        df_group_survived = df_group_survived.reset_index()
        df_group_survived = df_group_survived.rename(columns={'PassengerId':'Count'})

        name1 = 'Not Survived'
        x_trace1 = df_group_survived.loc[(df_group_survived['Survived']==0),['Count']]
        y_trace1 = df_group_survived.loc[(df_group_survived['Survived']==0),['Sex']]
        x_trace1 = x_trace1.Count.tolist()
        y_trace1 = y_trace1.Sex.tolist()

        name2 = 'Survived'
        x_trace2 = df_group_survived.loc[(df_group_survived['Survived']==1),['Count']]
        y_trace2 = df_group_survived.loc[(df_group_survived['Survived']==1),['Sex']]
        x_trace2 = x_trace2.Count.tolist()
        y_trace2 = y_trace2.Sex.tolist()

        #Pie Chart
        df_group_class = titanic.groupby(['Pclass'])['PassengerId'].count()
        df_group_class = pd.DataFrame(df_group_class).reset_index().rename(columns={'PassengerId':'Count'})
        labels = df_group_class.Pclass.tolist()
        count = df_group_class.Count.tolist()


        return x_trace1, y_trace1, x_trace2, y_trace2, name1, name2,\
                labels, count


